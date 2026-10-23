"""Scalable physical measurements, independent of renormalized H/edge operators.

Reconstruct a physical MPS from the saved isometries, never a 2**N vector.
Spin matrices below are defined independently of the DMRG implementation.
"""
import numpy as np

I=np.eye(2)
SX=np.array([[0.,1.],[1.,0.]])/2
SY=np.array([[0.,1j],[-1j,0.]])/2
SZ=np.diag([-.5,.5])


def block_tensors(block):
    """The last virtual index is the current renormalized block basis."""
    if block.parent is None:
        return [np.eye(2).reshape(1,2,2)]
    dim=len(block.parent.q)
    transform=np.eye(2*dim) if block.transform is None else block.transform
    return block_tensors(block.parent)+[transform.reshape(dim,2,-1)]


def snapshot_mps(snapshot):
    left,right,psi=snapshot
    tensors=block_tensors(left)
    # Right block physical order is inner -> outer, reverse BOTH chain and bonds.
    right_tensors=[t.transpose(2,1,0) for t in reversed(block_tensors(right))]
    right_tensors[0]=np.einsum('ab,bsc->asc',psi,right_tensors[0],optimize=True)
    return tensors+right_tensors


def transfer(env,tensor,op):
    return np.einsum('ab,asc,st,btd->cd',env,tensor.conj(),op,tensor,optimize=True)


class Measurements:
    """Physical left/right environments permit measurements at any bond."""
    def __init__(self,mps):
        self.mps=mps
        self.left=[np.ones((1,1))]
        for tensor in mps:
            self.left.append(transfer(self.left[-1],tensor,I))
        self.right=[None]*(len(mps)+1); self.right[-1]=np.ones((1,1))
        for j in range(len(mps)-1,-1,-1):
            t=mps[j]
            self.right[j]=np.einsum('asc,st,btd,cd->ab',t.conj(),I,t,self.right[j+1],optimize=True)
        self.norm=float(self.left[-1][0,0].real)
        if abs(self.norm-1)>1e-8:
            raise ArithmeticError(f'Physical MPS norm {self.norm} != 1')

    def pair(self,i,j,op_i,op_j):
        env=transfer(self.left[i],self.mps[i],op_i)
        for k in range(i+1,j): env=transfer(env,self.mps[k],I)
        env=transfer(env,self.mps[j],op_j)
        value=np.sum(env*self.right[j+1])/self.norm
        if abs(value.imag)>1e-10: raise ArithmeticError('Non-real Hermitian expectation')
        return float(value.real)

    def bonds(self,distance=1,delta=1.):
        return np.array([self.pair(j,j+distance,SX,SX)+self.pair(j,j+distance,SY,SY)+
                         delta*self.pair(j,j+distance,SZ,SZ)
                         for j in range(len(self.mps)-distance)])


def measure_snapshot(snapshot,j1=1.,j2=0.,delta=1.):
    meter=Measurements(snapshot_mps(snapshot))
    nearest=meter.bonds(1,delta); next_nearest=meter.bonds(2,delta)
    return dict(norm=meter.norm,nearest=nearest,next_nearest=next_nearest,
                energy=float(j1*nearest.sum()+j2*next_nearest.sum()))


def bit_bonds(v,basis,n,distance=1,delta=1.):
    """Independent bit-basis pair expectations, no MPS transfer or block operators."""
    results=[]
    for i in range(n-distance):
        j=i+distance
        bi=(basis>>i)&1; bj=(basis>>j)&1
        value=delta*np.sum(abs(v)**2*(bi-.5)*(bj-.5))
        source=np.flatnonzero(bi!=bj)
        target=np.searchsorted(basis,basis[source]^((1<<i)|(1<<j)))
        value+=.5*np.vdot(v[target],v[source]).real
        results.append(float(value.real))
    return np.array(results)


def tensor_selected_bonds(full,n,bonds):
    """Independent local tensor contractions for selected pairs in an exact state."""
    x=full.reshape((2,)*n,order='F')
    def act(state,op,axis):
        return np.moveaxis(np.tensordot(op,state,axes=(1,axis)),0,axis)
    out=[]
    for i,j in bonds:
        value=sum(np.vdot(x,act(act(x,op,j),op,i)) for op in (SX,SY,SZ))
        out.append(float(value.real))
    return np.array(out)
