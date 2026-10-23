"""Optional 3/4: long-chain DMRG and independently validated dimerization scan."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import json
import time
from pathlib import Path
import numpy as np
from src import core as c
from src import analysis as a
from src import mps_observables as o

ROOT=Path(__file__).resolve().parent
DATA=ROOT/'output'/'data'


def extend(data):
    start=time.perf_counter()
    data['checks']=[r for r in data['checks'] if r.get('section')!='optional34']
    data['optional34_complete']=False
    data['long_chains']=[]; data['dimer_scan']=[]
    data['thermodynamic_energy']=float(.25-np.log(2))
    checks=data['checks']

    def save():
        path=DATA/'results.json'
        temporary=path.with_suffix('.json.tmp')
        temporary.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf8')
        temporary.replace(path)

    def check(name,target,expected,measured,tolerance):
        passed=bool(abs(measured-expected)<=tolerance)
        checks.append(dict(name=name,target=target,expected=float(expected),measured=float(measured),
                           tolerance=tolerance,passed=passed,section='optional34'))
        if not passed:
            raise AssertionError(f'{name}: {measured}; expected {expected} +/- {tolerance}')

    def check_run(run,n,j2,chi):
        tag=f'N={n} J2={j2} chi={chi}'
        check('optional convergence '+tag,'fixed-chi energy iteration not converged',1,float(run['converged']),0)
        check('optional chi cap '+tag,'per-sector chi cap instead of global cap',0,max(0,max(run['dimensions'])-chi),0)
        check('optional truncation '+tag,'Schmidt weights do not equal projection loss',0,
              max(r['difference'] for r in run['trunc_checks']),3e-12)
        check('optional charge '+tag,'charge mixing in selected singular vectors',0,
              max(r['charge_leak'] for r in run['trunc_checks']),2e-12)
        check('optional local residual '+tag,'unconverged local solve (auxiliary)',0,
              max(r['solver_residual'] for r in run['local']),5e-8)
        measurements=[]
        for step,(row,snapshot) in enumerate(zip(run['sweeps'],run['sweep_snapshots']),1):
            measured=o.measure_snapshot(snapshot,j2=j2)
            check(f'optional physical MPS {tag} sweep={step}',
                  'renormalized H/edge errors, right reversal, missing physical bonds',row['energy'],measured['energy'],5e-9)
            check(f'optional MPS norm {tag} sweep={step}',
                  'wrong saved isometries or MPS centre connection',1,measured['norm'],2e-10)
            measurements.append(measured)
        return measurements[-1]

    # Fixed finite lengths: changing N and chi separates the two error sources.
    for n in (40,60):
        for chi in (32,64):
            run=c.dmrg(n,chi=chi,max_sweeps=12,energy_tol=1e-9,
                       progress=lambda s:print(s,flush=True))
            measured=check_run(run,n,0.,chi)
            row=dict(n=n,chi=chi,energy=run['energy'],energy_per_site=run['energy']/n,
                difference_from_infinite=run['energy']/n-data['thermodynamic_energy'],
                eps_max=run['sweeps'][-1]['eps_max'],eps_centre=run['sweeps'][-1]['eps_centre'],
                converged=run['converged'],sweeps=run['sweeps'],growth=run['growth'],
                physical_energy=measured['energy'],norm=measured['norm'],
                nearest=measured['nearest'].tolist(),next_nearest=measured['next_nearest'].tolist(),
                trunc_checks=run['trunc_checks'])
            data['long_chains'].append(row)
            tensors=o.snapshot_mps(run['snapshot'])
            np.savez_compressed(DATA/f'mps_N{n}_J2_0.0_chi_{chi}.npz',**{
                f'tensor_{i:03d}':tensor for i,tensor in enumerate(tensors)})
            save()

    # Dimerization definition uses adjacent bonds with left endpoint N/2-2, N/2-1.
    # Full profiles are kept, including boundaries, rather than only a scalar.
    for j2 in np.linspace(0,1,11):
        j2=float(round(j2,1))
        for n in (12,16,20):
            print(f'Dimer scan ED N={n}, J2={j2}',flush=True)
            h,basis=c.ed_hamiltonian(n,j2=j2); e0,v0=c.ground(h)
            nn=o.bit_bonds(v0,basis,n,1); nnn=o.bit_bonds(v0,basis,n,2)
            indices=(n//2-2,n//2-1)
            check(f'dimer ED energy decomposition N={n} J2={j2}',
                  'incorrect ED couplings or omitted physical bonds',e0,float(nn.sum()+j2*nnn.sum()),2e-10)
            check(f'dimer ED residual N={n} J2={j2}','unconverged exact reference (auxiliary)',0,
                  np.linalg.norm(h@v0-e0*v0),5e-8)
            independent=o.tensor_selected_bonds(a.full_state(v0,basis,n),n,[(i,i+1) for i in indices])
            check(f'dimer central tensor N={n} J2={j2}',
                  'central-bond positions, spin normalization, bit correlation errors',0,
                  np.max(abs(nn[list(indices)]-independent)),2e-11)
            if j2==.5:
                check(f'dimer MG profile N={n}','wrong strong/weak bond placement',0,
                      np.max(abs(nn-np.array([-.75 if i%2==0 else 0 for i in range(n-1)]))),2e-10)
            record=dict(n=n,j2=j2,method='ED',energy=e0,nearest=nn.tolist(),next_nearest=nnn.tolist(),
                central_bonds=list(indices),central_values=nn[list(indices)].tolist(),
                signed_dimer=float(nn[indices[0]]-nn[indices[1]]),
                dimer=float(abs(nn[indices[0]]-nn[indices[1]])))
            data['dimer_scan'].append(record)
            if n==20:
                chi=64
                run=c.dmrg(n,j2=j2,chi=chi,max_sweeps=20,energy_tol=1e-9,
                           progress=lambda s:print(s,flush=True))
                measured=check_run(run,n,j2,chi)
                # Rebuild the same approximate state in independent physical ED basis.
                vec=c.to_ed_state(*run['snapshot'],basis,n)
                same_state_nn=o.bit_bonds(vec,basis,n,1)
                check(f'dimer MPS vs physical bit bonds J2={j2}',
                      'MPS local transfer, operator insertion or physical site ordering',0,
                      np.max(abs(measured['nearest']-same_state_nn)),3e-11)
                check(f'dimer DMRG vs ED energy J2={j2}',
                      'wrong variational ground state or inadequate chi',e0,run['energy'],2e-5)
                check(f'dimer DMRG vs ED all bonds J2={j2}',
                      'incorrect or insufficiently converged dimer correlations',0,
                      np.max(abs(measured['nearest']-nn)),3e-4)
                measured_nn=measured['nearest']
                data['dimer_scan'].append(dict(n=n,j2=j2,method='DMRG',chi=chi,
                    energy=run['energy'],ed_energy=e0,energy_error=abs(run['energy']-e0),
                    nearest=measured_nn.tolist(),next_nearest=measured['next_nearest'].tolist(),
                    central_bonds=list(indices),central_values=measured_nn[list(indices)].tolist(),
                    signed_dimer=float(measured_nn[indices[0]]-measured_nn[indices[1]]),
                    dimer=float(abs(measured_nn[indices[0]]-measured_nn[indices[1]])),
                    bond_error=float(np.max(abs(measured_nn-nn))),
                    dimer_error=abs(float(abs(measured_nn[indices[0]]-measured_nn[indices[1]]))-record['dimer']),
                    eps_max=run['sweeps'][-1]['eps_max'],sweeps=run['sweeps'],converged=run['converged']))
            save()
    # Inject an error into the ACTUAL measurement pipeline, not just a manually
    # written wrong matrix. Double the transverse pair coefficient on a singlet.
    original_x,original_y=o.SX,o.SY
    try:
        o.SX=np.sqrt(2)*original_x; o.SY=np.sqrt(2)*original_y
        left=np.eye(2).reshape(1,2,2)
        right=np.array([[[0.],[-1/np.sqrt(2)]],[[1/np.sqrt(2)],[0.]]])
        wrong=float(o.Measurements([left,right]).bonds(1)[0])
    finally:
        o.SX,o.SY=original_x,original_y
    check('optional mutation wrong transverse coefficient','physical correlation check sensitivity',1,float(abs(wrong+.75)>.1),0)
    data['optional34_mutation']=dict(expected=-.75,wrong_measured=wrong,caught=abs(wrong+.75)>.1)
    data['optional34_runtime_seconds']=time.perf_counter()-start
    data.setdefault('base_runtime_seconds',data['runtime_seconds'])
    data['runtime_seconds']=data['base_runtime_seconds']+data['optional34_runtime_seconds']
    data['optional34_complete']=True
    from src.refinements import enrich
    enrich(data)
    save()
    print(f'OPTIONAL 3/4 COMPLETE: {len(data["checks"])} total checks; {data["optional34_runtime_seconds"]:.1f}s',flush=True)
    return data


if __name__=='__main__':
    data=json.loads((DATA/'results.json').read_text(encoding='utf8'))
    extend(data)
