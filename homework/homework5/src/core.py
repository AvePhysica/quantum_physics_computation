"""Open-chain J1-J2 XXZ: independent bit ED and traditional two-site block DMRG.

Local tensor basis is (down, up). Blocks are ordered OUTER -> INNER on BOTH
sides, so the physical right block is reversed. Charge q is twice total Sz.
No ED result is used to construct, initialize, or optimize a DMRG state.
"""
from dataclasses import dataclass
from itertools import combinations
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
import numpy as np
from scipy import sparse
from scipy.linalg import eigh, svd
from scipy.sparse.linalg import LinearOperator, eigsh
Z=np.diag([-.5,.5])
P=np.array([[0.,0.],[1.,0.]])
M=P.T
ID=np.eye(2)


def ed_hamiltonian(n,j1=1.,j2=0.,delta=1.,periodic=False,full=False):
    """Independent physical-bit construction. Periodic sums count each j,r term.

    At N=4 the r=2 periodic sum counts each opposite pair twice, as in the
    standard sum_j S_j.S_(j+2); the open-chain construction never duplicates.
    """
    if full:
        basis=np.arange(1<<n,dtype=np.int64)
    else:
        basis=np.array(sorted(sum(1<<j for j in comb)
                              for comb in combinations(range(n),n//2)),dtype=np.int64)
    rows=[]; cols=[]; vals=[]; diagonal=np.zeros(len(basis))
    for distance,coupling in ((1,j1),(2,j2)):
        if coupling==0:
            continue
        for i in range(n if periodic else n-distance):
            j=(i+distance)%n
            if i==j:
                raise ValueError('Self-bond is not supported')
            bi=(basis>>i)&1; bj=(basis>>j)&1
            diagonal+=coupling*delta*(bi-.5)*(bj-.5)
            source=np.flatnonzero(bi!=bj)
            target=np.searchsorted(basis,basis[source]^((1<<i)|(1<<j)))
            rows.append(target); cols.append(source)
            vals.append(np.full(len(source),.5*coupling))
    rows.append(np.arange(len(basis))); cols.append(np.arange(len(basis))); vals.append(diagonal)
    h=sparse.coo_matrix((np.concatenate(vals),(np.concatenate(rows),np.concatenate(cols))),
                       shape=(len(basis),len(basis))).tocsr()
    return h,basis


def ground(h,tol=2e-12):
    """Normalized lowest eigenpair; deterministic initial vector, no energy hints."""
    n=h.shape[0]
    if n<=180 and sparse.issparse(h):
        e,v=eigh(h.toarray(),subset_by_index=[0,0])
    else:
        v0=np.random.default_rng(731+n).normal(size=n)
        e,v=eigsh(h,k=1,which='SA',v0=v0,tol=tol,ncv=min(n,40),maxiter=10000)
    return float(e[0]),v[:,0]


@dataclass
class Block:
    length: int
    h: np.ndarray
    q: np.ndarray
    edges: tuple  # nearest and second-nearest INNER boundary (z,+,-)
    parent: object=None
    transform: object=None


def site():
    return Block(1,np.zeros((2,2)),np.array([-1,1]),((Z,P,M),))


def pair_kron(a,b,delta):
    return delta*np.kron(a[0],b[0])+.5*(np.kron(a[1],b[2])+np.kron(a[2],b[1]))


def enlarge(block,j1=1.,j2=0.,delta=1.):
    """Append one INNER site; keep exactly the two edge operator triples."""
    d=len(block.q)
    h=np.kron(block.h,ID)+j1*pair_kron(block.edges[0],(Z,P,M),delta)
    if len(block.edges)>1:
        h+=j2*pair_kron(block.edges[1],(Z,P,M),delta)
    edges=(tuple(np.kron(np.eye(d),op) for op in (Z,P,M)),
           tuple(np.kron(op,ID) for op in block.edges[0]))
    return Block(block.length+1,h,(block.q[:,None]+np.array([-1,1])).ravel(),
                 edges,block,None)


def solve_super(a,b,j1=1.,j2=0.,delta=1.):
    """A=(left block + site), B=(right block + site), both point inward.

    Apply H to a matrix X without building a dense superblock Hamiltonian.
    Cross bonds are J1 a0-b0, J2 a1-b0, and J2 a0-b1; there is no a1-b1 bond.
    """
    shape=(len(a.q),len(b.q))
    allowed=np.flatnonzero((a.q[:,None]+b.q[None,:]).ravel()==0)
    terms=[]
    for ai,bi,j in ((0,0,j1),(1,0,j2),(0,1,j2)):
        if j==0 or ai>=len(a.edges) or bi>=len(b.edges):
            continue
        ae,be=a.edges[ai],b.edges[bi]
        terms.extend(((j*delta,ae[0],be[0]),(.5*j,ae[1],be[2]),(.5*j,ae[2],be[1])))
    def matvec(v):
        x=np.zeros(shape); x.ravel()[allowed]=v
        y=a.h@x+x@b.h.T
        for coeff,op_a,op_b in terms:
            y+=coeff*(op_a@x@op_b.T)
        return y.ravel()[allowed]
    op=LinearOperator((len(allowed),len(allowed)),matvec=matvec,dtype=float)
    e,v=ground(op)
    psi=np.zeros(shape); psi.ravel()[allowed]=v
    return dict(energy=e,psi=psi,residual=float(np.linalg.norm(matvec(v)-e*v)))


def truncate(psi,qa,qb,chi):
    """Charge-resolved Schmidt truncation, with a GLOBAL cap chi.

    full_matrices=True supplies null-space columns even for rectangular charge
    blocks. Their weights are zero. They must not be lost when requesting an
    untruncated basis or retaining more columns than the Schmidt rank.
    All selected columns retain a definite charge. One stable global ordering
    is used for the columns, charges and weights together.
    """
    candidates=[]
    for charge in np.unique(qa):
        ia=np.flatnonzero(qa==charge); ib=np.flatnonzero(qb==-charge)
        if len(ib):
            u,s,_=svd(psi[np.ix_(ia,ib)],full_matrices=True,lapack_driver='gesvd')
            weights=np.zeros(len(ia)); weights[:len(s)]=s*s
        else:
            u=np.eye(len(ia)); weights=np.zeros(len(ia))
        for col,weight in enumerate(weights):
            vector=np.zeros(len(qa)); vector[ia]=u[:,col]
            candidates.append((float(weight),int(charge),vector))
    candidates.sort(key=lambda item:-item[0])
    chosen=candidates[:min(int(chi),len(qa))]
    t=np.column_stack([item[2] for item in chosen])
    q=np.array([item[1] for item in chosen])
    weights=np.array([item[0] for item in chosen])
    eps=max(0.,1.-float(weights.sum()))
    if abs(np.linalg.norm(psi)**2-1)>1e-9:
        raise ValueError('Truncation requires a normalized superblock state')
    if np.linalg.norm(t.T@t-np.eye(t.shape[1]))>1e-10:
        raise ArithmeticError('Non-isometric truncation')
    return t,q,weights,eps


def compress(a,t,q):
    """Transform H AND EVERY stored edge operator with the SAME isometry."""
    edges=tuple(tuple(t.T@op@t for op in triple) for triple in a.edges)
    return Block(a.length,t.T@a.h@t,q,edges,a.parent,t)


def embedding(a):
    """Physical tensor-product embedding, used only for independent checks."""
    if a.parent is None:
        return np.eye(2)
    e=np.kron(embedding(a.parent),ID)
    return e if a.transform is None else e@a.transform


def to_ed_state(a,b,psi,basis,n):
    """Undo left tensor bit order and physical right-block reversal explicitly."""
    physical=embedding(a)@psi@embedding(b).T
    row=np.zeros(len(basis),dtype=np.int64); col=row.copy()
    for j in range(a.length):
        row=(row<<1)|((basis>>j)&1)
    for j in range(n-1,a.length-1,-1):
        col=(col<<1)|((basis>>j)&1)
    v=physical[row,col]
    if abs(v@v-1)>1e-9:
        raise ArithmeticError('Physical embedding lost norm or charge')
    return v


def dmrg(n,j1=1.,j2=0.,delta=1.,chi=32,max_sweeps=6,energy_tol=1e-9,progress=None):
    """Infinite warmup followed by two-site finite block sweeps.

    Report energies BEFORE truncating the current optimized state. Retained
    blocks themselves never exceed chi. Store BOTH independent environments.
    Each full sweep travels centre -> right -> left -> centre, updating the
    block on the growing side only. No ED vectors enter this routine.
    """
    if n<4 or n%2 or chi<1:
        raise ValueError('Need even N>=4 and chi>=1')
    left={1:site()}; right={1:site()}
    growth=[]; sweeps=[]; local=[]; dimensions=[]; trunc_checks=[]
    growth_snapshots=[]; sweep_snapshots=[]

    def optimize(l,r,phase,step,direction):
        a=enlarge(left[l],j1,j2,delta); b=enlarge(right[r],j1,j2,delta)
        sol=solve_super(a,b,j1,j2,delta); psi=sol['psi']
        ta,qa,wa,ea=truncate(psi,a.q,b.q,chi)
        tb,qb,wb,eb=truncate(psi.T,b.q,a.q,chi)
        # Direct projection error: independent of summing retained SVD weights.
        norm_loss=float(np.linalg.norm(psi-ta@(ta.T@psi))**2)
        charge_leak=float(np.max(np.abs(a.q[:,None]*ta-ta*qa[None,:])))
        trunc_checks.append(dict(n=l+r+2,phase=phase,step=step,
            eps=ea,projection_loss=norm_loss,difference=abs(norm_loss-ea),
            charge_leak=charge_leak,isometry=float(np.linalg.norm(ta.T@ta-np.eye(len(qa))))))
        dimensions.extend([len(qa),len(qb)])
        record=dict(n=l+r+2,chi=chi,kept_left=len(qa),kept_right=len(qb),
            energy=sol['energy'],energy_per_site=sol['energy']/(l+r+2),
            eps_left=ea,eps_right=eb,eps_max=max(ea,eb),solver_residual=sol['residual'],
            phase=phase,step=step,left_length=l,direction=direction)
        local.append(record)
        return a,b,psi,compress(a,ta,qa),compress(b,tb,qb),record

    for l in range(1,n//2):
        a,b,psi,la,rb,rec=optimize(l,l,'growth',l,'both')
        left[l+1]=la; right[l+1]=rb; growth.append(rec)
        growth_snapshots.append((a,b,psi))
    snapshot=(a,b,psi)
    if progress:
        progress(f'N={n} J2={j2} chi={chi}: warmup E={rec["energy"]:.12f}')
    centre=n//2-1
    last=rec['energy']
    for sweep in range(1,max_sweeps+1):
        sweep_records=[]
        for direction,positions in (
            ('right',range(centre,n-2)),
            ('left',range(n-3,0,-1)),
            ('right',range(1,centre+1))):
            for l in positions:
                r=n-l-2
                a,b,psi,la,rb,rec=optimize(l,r,'finite',sweep,direction)
                if direction=='right':
                    left[l+1]=la
                else:
                    right[r+1]=rb
                sweep_records.append(rec)
        snapshot=(a,b,psi)
        sweep_snapshots.append(snapshot)
        summary=dict(sweep=sweep,energy=rec['energy'],
            eps_max=max(x['eps_max'] for x in sweep_records),eps_centre=rec['eps_max'],
            energy_change=rec['energy']-last,
            local_energy_range=max(x['energy'] for x in sweep_records)-min(x['energy'] for x in sweep_records))
        sweeps.append(summary)
        if progress:
            progress(f'  sweep {sweep}: E={rec["energy"]:.12f}, eps={summary["eps_max"]:.3e}')
        if sweep>=2 and abs(rec['energy']-last)<energy_tol:
            break
        last=rec['energy']
    return dict(energy=rec['energy'],growth=growth,sweeps=sweeps,local=local,
                snapshot=snapshot,dimensions=dimensions,trunc_checks=trunc_checks,
                growth_snapshots=growth_snapshots,sweep_snapshots=sweep_snapshots,
                converged=bool(sweeps and abs(sweeps[-1]['energy_change'])<energy_tol))
