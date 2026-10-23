"""Physical-state observables and the one-shot truncation experiment."""
import numpy as np
from scipy.linalg import eigh, svd
from .core import ed_hamiltonian, truncate


def full_state(v,basis,n):
    out=np.zeros(1<<n,dtype=v.dtype); out[basis]=v
    return out


def dimer(basis,n):
    """Product of (up down - down up)/sqrt(2), no diagonalization involved."""
    v=np.ones(len(basis))
    for j in range(0,n,2):
        b0=(basis>>j)&1; b1=(basis>>(j+1))&1
        v*=np.where(b0!=b1,(2*b0-1)/np.sqrt(2),0.)
    return v


def entropies(full,n,method='svd'):
    values=[]
    for cut in range(1,n):
        x=full.reshape((1<<cut,1<<(n-cut)),order='F')
        if method=='svd':
            p=svd(x,compute_uv=False)**2
        else:
            # Form the SMALLER reduced density matrix, independently of SVD.
            rho=x@x.conj().T if x.shape[0]<=x.shape[1] else x.conj().T@x
            p=np.maximum(eigh(rho,eigvals_only=True),0)
        p=p[p>1e-15]
        values.append(float(-np.sum(p*np.log(p))))
    return np.array(values)


def tensor_h_action(full,n,j1=1.,j2=0.,delta=1.,periodic=False):
    """Independent operator implementation using LOCAL 2x2 tensor contractions.

    Used to check the bit-flip sparse Hamiltonian, not called by ED or DMRG.
    First tensor axis is physical site zero (Fortran reshape).
    """
    sx=np.array([[0,1],[1,0]])/2
    sy=np.array([[0,1j],[-1j,0]])/2  # down/up convention
    sz=np.diag([-.5,.5])
    x=full.reshape((2,)*n,order='F')
    out=np.zeros_like(x,dtype=complex)
    def act(state,op,axis):
        return np.moveaxis(np.tensordot(op,state,axes=(1,axis)),0,axis)
    for distance,coupling in ((1,j1),(2,j2)):
        if coupling==0:
            continue
        for i in range(n if periodic else n-distance):
            j=(i+distance)%n
            for op,factor in ((sx,1.),(sy,1.),(sz,delta)):
                out+=coupling*factor*act(act(x,op,j),op,i)
    return out.ravel(order='F')


def compare_truncations(h,basis,v,n,ms):
    """Project ONLY the left half, normalize, evaluate the ORIGINAL H.

    Energy truncation keeps the globally lowest energies across charge sectors;
    ties are deterministically resolved by charge then sector eigenvector index.
    No diagonalization of a projected Hamiltonian is performed.
    """
    l=n//2; dim=1<<l
    x=full_state(v,basis,n).reshape((dim,dim),order='F')
    u,s,_=svd(x,full_matrices=True)
    ha,_=ed_hamiltonian(l,full=True)
    charges=np.array([2*int(i).bit_count()-l for i in range(dim)])
    candidates=[]
    for q in np.unique(charges):
        inds=np.flatnonzero(charges==q)
        e,z=eigh(ha[np.ix_(inds,inds)].toarray())
        for k,val in enumerate(e):
            vec=np.zeros(dim); vec[inds]=z[:,k]
            candidates.append((float(val),int(q),k,vec))
    candidates.sort(key=lambda item:(item[0],item[1],item[2]))
    e0=float(v@(h@v)); rows=[]
    for m in ms:
        row=dict(m=m,dm_discard=float(np.sum(s[m:]**2)))
        # A global SVD may rotate exactly degenerate singular vectors across
        # different charges. A partial multiplet cutoff would then leak Sz.
        # Charge-resolved SVD keeps the same largest weights without that leak.
        t_dm,_,_,_=truncate(x,charges,charges,m)
        for name,t in (('dm',t_dm),('energy',np.column_stack([item[3] for item in candidates[:m]]))):
            xp=t@(t.T@x); kept=float(np.linalg.norm(xp)**2)
            vp=xp.ravel(order='F')/np.sqrt(kept)
            restricted=vp[basis]
            # Even a cutoff that splits a degenerate charge multiplet retains Sz.
            if abs(restricted@restricted-1)>1e-10:
                raise ArithmeticError('Projected state left the fixed-charge sector')
            energy=float(restricted@(h@restricted))
            tensor_energy=float(np.vdot(vp,tensor_h_action(vp,n)).real)
            row.update({name+'_energy':energy,name+'_error':abs(energy-e0),
                        name+'_kept_norm':kept,name+'_check':abs(energy-tensor_energy)})
        rows.append(row)
    return rows
