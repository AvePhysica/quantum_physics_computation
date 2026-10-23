"""Clean-run entry point: actual computations, independent checks, then artifacts."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import sys
import json
import platform
import time
from pathlib import Path
import numpy as np
import scipy
from scipy.linalg import eigh
from src import core as c
from src import analysis as a

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output'


def main():
    start=time.perf_counter()
    (OUT/'data').mkdir(parents=True,exist_ok=True)
    checks=[]; cache={}
    data=dict(parameters=dict(j1=1.,delta=1.,sector='Sz_tot=0',entropy_log='natural',
        sweep_definition='centre -> right -> left -> centre',energy_tol=1e-9,
        solver_tol=2e-12,max_sweeps=12),
        environment=dict(python=sys.version,numpy=np.__version__,scipy=scipy.__version__,platform=platform.platform()))

    def check(name,target,expected,measured,tolerance):
        passed=bool(abs(measured-expected)<=tolerance)
        checks.append(dict(name=name,target=target,expected=expected,measured=float(measured),
                           tolerance=tolerance,passed=passed))
        if not passed:
            raise AssertionError(f'{name}: measured {measured}; expected {expected} +/- {tolerance}')

    def save():
        data['checks']=checks
        (OUT/'data'/'results.json').write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8')

    def ed(n,j2=0.,periodic=False):
        key=(n,float(j2),periodic)
        if key not in cache:
            print(f'ED N={n}, J2={j2}, periodic={periodic}',flush=True)
            h,basis=c.ed_hamiltonian(n,j2=j2,periodic=periodic)
            e,v=c.ground(h)
            herm=h-h.T
            check(f'ED Hermitian N={n} J2={j2} P={periodic}','asymmetric matrix elements',0,
                  np.max(np.abs(herm.data),initial=0),1e-14)
            check(f'ED residual N={n} J2={j2} P={periodic}','eigensolver convergence (auxiliary)',0,
                  np.linalg.norm(h@v-e*v),2e-8)
            if n<=8 or n==20:
                full=a.full_state(v,basis,n)
                hv=a.tensor_h_action(full,n,j2=j2,periodic=periodic)
                check(f'ED tensor action N={n} J2={j2} P={periodic}',
                      'wrong bonds, spin normalization, transverse sign, boundary',0,
                      np.linalg.norm(hv-a.full_state(h@v,basis,n)),1e-11)
            cache[key]=(h,basis,e,v)
        return cache[key]

    h2,_=c.ed_hamiltonian(2,full=True)
    check('two-site analytic full spectrum','spin factor and sign',0,
          np.max(np.abs(np.linalg.eigvalsh(h2.toarray())-np.array([-.75,.25,.25,.25]))),1e-14)
    data['small']=[]
    for j2 in (0.,.3,.5):
        for n in (4,6,8,10):
            h,basis,e,v=ed(n,j2)
            block=c.site()
            for _ in range(n//2-2): block=c.enlarge(block,1,j2,1)
            block=c.enlarge(block,1,j2,1)
            sol=c.solve_super(block,block,1,j2,1)
            check(f'untruncated N={n} J2={j2}','missing or duplicated cross-boundary bonds',e,sol['energy'],2e-10)
            expanded=c.to_ed_state(block,block,sol['psi'],basis,n)
            check(f'untruncated physical residual N={n} J2={j2}','edge positions and tensor order',0,
                  np.linalg.norm(h@expanded-e*expanded),2e-9)
            data['small'].append(dict(n=n,j2=j2,ed=e,superblock=sol['energy'],difference=abs(e-sol['energy'])))
    data['boundaries']=[]
    for n in (4,6,8):
        eo=ed(n)[2]; ep=ed(n,periodic=True)[2]
        data['boundaries'].append(dict(n=n,open=eo,periodic=ep,difference=eo-ep))
    h,basis,e,v=ed(12)
    data['projection']=a.compare_truncations(h,basis,v,12,[2,4,6,8,12,16])
    data['projection_e0']=e
    for row in data['projection']:
        for method in ('dm','energy'):
            check(f'projection m={row["m"]} {method}','energy evaluated with wrong H or tensor ordering',0,
                  row[method+'_check'],2e-10)
        check(f'discard norm m={row["m"]}','wrong Schmidt weight sum',row['dm_discard'],1-row['dm_kept_norm'],2e-12)
    data['mg']=[]; data['variance']=[]
    for n in (8,10,12,14,16):
        h,basis,e,v=ed(n,.5); dimer=a.dimer(basis,n); exact=-3*n/8
        residual=float(np.linalg.norm(h@dimer-exact*dimer))
        overlap=float(abs(dimer@v)**2)
        check(f'MG energy N={n}','J2 coefficient, OBC, spin factor',exact,e,2e-10)
        check(f'MG dimer residual N={n}','wrong J2 or crossing bonds (analytic vector)',0,residual,2e-12)
        check(f'MG overlap N={n}','wrong ED ground state or bit order',1,overlap,2e-10)
        full=a.full_state(v,basis,n); ent=a.entropies(full,n)
        ent2=a.entropies(full,n,method='rho')
        expected=np.array([np.log(2) if cut%2 else 0. for cut in range(1,n)])
        check(f'MG entropy analytic N={n}','wrong cut or Schmidt coefficients',0,np.max(abs(ent-expected)),2e-10)
        check(f'MG entropy rho N={n}','entropy algorithm',0,np.max(abs(ent-ent2)),2e-10)
        data['mg'].append(dict(n=n,ed=e,exact=exact,residual=residual,overlap_squared=overlap,entropy=ent[:n//2].tolist()))
    for j2 in (0.,.5):
        h,basis,e,v=ed(12,j2)
        hv=h@v
        variance_sub=float(hv@hv-(v@hv)**2)
        variance_norm=float(np.linalg.norm(hv-e*v)**2)
        other=a.tensor_h_action(a.full_state(v,basis,12),12,j2=j2)
        variance_tensor=float(np.linalg.norm(other-e*a.full_state(v,basis,12))**2)
        check(f'variance tensor J2={j2}','H differs from independent local tensor contractions',0,
              np.linalg.norm(other-a.full_state(hv,basis,12)),2e-11)
        check(f'variance subtract vs norm J2={j2}','catastrophic cancellation or H squared implementation',
              variance_norm,variance_sub,2e-11)
        data['variance'].append(dict(j2=j2,energy=e,variance_subtraction=variance_sub,
                                    variance_residual=variance_norm,variance_tensor=variance_tensor))
    save()

    data['dmrg']=[]
    for j2,chi in [(0.,2),(0.,4),(0.,8),(0.,16),(0.,32),(.3,32)]:
        run=c.dmrg(20,j2=j2,chi=chi,max_sweeps=12,progress=lambda s: print(s,flush=True))
        # Rebuild EVERY reported growth and full-sweep state in the original
        # bit basis. This catches wrong operator renormalization after truncation.
        physical_checks=[]
        for records,snapshots in ((run['growth'],run['growth_snapshots']),
                                  (run['sweeps'],run['sweep_snapshots'])):
            for index,(rec,snap) in enumerate(zip(records,snapshots)):
                aa,bb,psi=snap; n=aa.length+bb.length
                hh,bs,e0,v0=ed(n,j2)
                vec=c.to_ed_state(aa,bb,psi,bs,n)
                measured=float(vec@(hh@vec))
                tag=f'physical N={n} J2={j2} chi={chi} {"growth" if records is run["growth"] else "sweep"} {index}'
                check(tag,'wrong boundary operators, charge sectors, right-block reversal',rec['energy'],measured,2e-9)
                # The exact ED reference is independently validated above.
                if rec['energy']<e0-2e-9: raise AssertionError('Variational energy below exact ground state')
                rec['ed_energy']=e0; rec['ed_error']=abs(rec['energy']-e0)
                physical_checks.append(dict(n=n,energy=measured,difference=abs(measured-rec['energy']),
                    overlap_squared=float(abs(vec@v0)**2),physical_residual=float(np.linalg.norm(hh@vec-measured*vec))))
        check(f'chi cap J2={j2} chi={chi}','per-sector cap erroneously multiplies total dimension',0,
              max(0,max(run['dimensions'])-chi),0)
        check(f'projection loss J2={j2} chi={chi}','discard weight or selected singular vectors',0,
              max(x['difference'] for x in run['trunc_checks']),2e-12)
        check(f'charge retention J2={j2} chi={chi}','mixing charge sectors in truncation',0,
              max(x['charge_leak'] for x in run['trunc_checks']),2e-12)
        check(f'isometry J2={j2} chi={chi}','nonorthogonal projected basis',0,
              max(x['isometry'] for x in run['trunc_checks']),2e-11)
        check(f'local eigensolver J2={j2} chi={chi}','unconverged superblock solver (auxiliary)',0,
              max(x['solver_residual'] for x in run['local']),2e-8)
        if not run['converged']:
            raise AssertionError(f'Increase sweep budget: J2={j2} chi={chi} not converged')
        record={k:run[k] for k in ('energy','growth','sweeps','local','trunc_checks','converged')}
        record.update(j2=j2,chi=chi,physical_checks=physical_checks,
                      ed_energy=ed(20,j2)[2],ed_error=abs(run['energy']-ed(20,j2)[2]))
        aa,bb,psi=run['snapshot']; hh,bs,_,_=ed(20,j2)
        np.savez_compressed(OUT/'data'/f'state_N20_J2_{j2}_chi_{chi}.npz',
            basis=bs,state=c.to_ed_state(aa,bb,psi,bs,20))
        data['dmrg'].append(record); save()

    # Deliberate error injections: original functions/operators remain unchanged.
    data['mutations']=[]
    h,bs,e,v=ed(8,.5); d=a.dimer(bs,8)
    for name,kwargs in [('omit J2',dict(j2=0)),('periodic wrap',dict(j2=.5,periodic=True)),
                        ('wrong J2 sign',dict(j2=-.5))]:
        wrong,_=c.ed_hamiltonian(8,**kwargs)
        if name=='periodic wrap':
            # Dimer is also an eigenstate on the MG ring: energy alone DOES NOT
            # detect this mutation. Use an arbitrary-vector OBC tensor-action check.
            rng=np.random.default_rng(99); probe=rng.normal(size=len(bs)); probe/=np.linalg.norm(probe)
            mismatch=np.linalg.norm(wrong@probe-a.tensor_h_action(a.full_state(probe,bs,8),8,j2=.5)[bs])
        else:
            mismatch=np.linalg.norm(wrong@d+3*d)
        check('mutation caught '+name,'check sensitivity to deliberate Hamiltonian corruption',1,float(mismatch>1e-7),0)
        data['mutations'].append(dict(name=name,mismatch=float(mismatch),caught=bool(mismatch>1e-7)))
    bl=c.enlarge(c.enlarge(c.site(),j2=.3),j2=.3)
    aa=c.enlarge(bl,j2=.3)
    broken=c.Block(aa.length,aa.h,aa.q,(aa.edges[0],tuple(np.zeros_like(x) for x in aa.edges[1])),aa.parent,aa.transform)
    wrong=c.solve_super(broken,aa,j2=.3)['energy']; expected=ed(8,.3)[2]
    check('mutation caught second edge zero','missing second edge operator',1,float(abs(wrong-expected)>1e-7),0)
    data['mutations'].append(dict(name='zero second boundary operators',mismatch=abs(wrong-expected),caught=True))

    # Optional 1: full entanglement profiles and controlled typical states.
    data['profiles']=[]
    for j2 in (0.,.5):
        h,bs,e,v=ed(16,j2); full=a.full_state(v,bs,16)
        ent=a.entropies(full,16); rho=a.entropies(full,16,method='rho')
        check(f'entropy mirror J2={j2}','incorrect left/right partition',0,np.max(abs(ent-ent[::-1])),2e-10)
        check(f'entropy rho J2={j2}','incorrect singular-value weights',0,np.max(abs(ent-rho)),2e-10)
        data['profiles'].append(dict(j2=j2,entropy=ent.tolist(),max_cuts=(np.flatnonzero(abs(ent-ent.max())<1e-9)+1).tolist()))
    data['typical']=[]
    for n in (4,8,12,16):
        dim=1<<n
        product=np.full(dim,1/np.sqrt(dim))
        neel=np.zeros(dim); neel[sum(1<<j for j in range(0,n,2))]=1
        ghz=np.zeros(dim); ghz[[0,-1]]=1/np.sqrt(2)
        rng=np.random.default_rng(20261019+n)
        random=rng.normal(size=dim)+1j*rng.normal(size=dim); random/=np.linalg.norm(random)
        for name,full in (('product',product),('Neel',neel),('GHZ',ghz),('random',random)):
            x=full.reshape((1<<(n//2),-1),order='F')
            p=np.linalg.svd(x,compute_uv=False)**2; p=p[p>1e-15]
            ent=float(-p@np.log(p)); rho=x@x.conj().T
            w=np.maximum(eigh(rho,eigvals_only=True),0); w=w[w>1e-15]
            check(f'typical entropy {name} N={n}','entropy implementation',ent,float(-w@np.log(w)),2e-10)
            if name!='random':
                check(f'typical analytic {name} N={n}','state construction',np.log(2) if name=='GHZ' else 0,ent,2e-12)
            data['typical'].append(dict(n=n,state=name,entropy=ent))
    # Optional 2: literal unweighted linear extrapolation versus 1/chi.
    runs=[r for r in data['dmrg'] if r['j2']==0 and r['chi']>=4]
    x=1/np.array([r['chi'] for r in runs],dtype=float); y=np.array([r['energy'] for r in runs])
    slope,intercept=np.polyfit(x,y,1)
    other=np.linalg.lstsq(np.column_stack([x,np.ones(len(x))]),y,rcond=None)[0]
    check('linear extrapolation independent solve','incorrect fit coordinates or intercept',intercept,other[1],1e-11)
    exact=ed(20)[2]
    data['extrapolation']=dict(slope=float(slope),intercept=float(intercept),exact=exact,
        error=float(abs(intercept-exact)),chi32_error=runs[-1]['ed_error'],
        improved=bool(abs(intercept-exact)<runs[-1]['ed_error']))
    data['runtime_seconds']=time.perf_counter()-start
    save()
    if '--base-only' not in sys.argv:
        from run_optional import extend
        extend(data)
    print(f'COMPLETE: {len(data["checks"])} checks passed; {data["runtime_seconds"]:.1f}s',flush=True)


if __name__=='__main__':
    main()
