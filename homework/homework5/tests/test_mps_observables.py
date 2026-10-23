"""Independent checks for scalable physical measurements without 2**N expansion."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import sys
import unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src import core as c
try:
    from src import mps_observables as o
except ImportError:
    o=None


class MPSTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(o,'Scalable physical MPS measurements not implemented')

    def test_state_and_individual_bonds_match_original_bit_basis(self):
        run=c.dmrg(10,j2=.3,delta=.73,chi=4,max_sweeps=2)
        snapshot=run['snapshot']; mps=o.snapshot_mps(snapshot)
        h,basis=c.ed_hamiltonian(10,j2=.3,delta=.73)
        v=c.to_ed_state(*snapshot,basis,10)
        full=mps[0][0]
        for tensor in mps[1:]: full=np.tensordot(full,tensor,axes=(-1,0))
        full=full[...,0].reshape(-1)
        # Sequential MPS tensors are physical site 0 first (MSB in flatten).
        reverse=np.array([int(f'{int(x):010b}'[::-1],2) for x in basis])
        np.testing.assert_allclose(full[reverse],v,atol=1e-12)
        measured=o.measure_snapshot(snapshot,j2=.3,delta=.73)
        self.assertAlmostEqual(measured['norm'],1,places=12)
        self.assertAlmostEqual(measured['energy'],float(v@(h@v)),places=10)
        for distance,key in ((1,'nearest'),(2,'next_nearest')):
            independent=o.bit_bonds(v,basis,10,distance,delta=.73)
            np.testing.assert_allclose(measured[key],independent,atol=2e-12)

    def test_dimer_product_has_exact_bond_profile(self):
        # Rank-2 exact singlet MPS, assembled without DMRG or core spin operators.
        a=np.zeros((1,2,2)); a[0]=np.eye(2)
        b=np.array([[[0.],[-1/np.sqrt(2)]],[[1/np.sqrt(2)],[0.]]])
        mps=[x.copy() for _ in range(20) for x in (a,b)]
        meter=o.Measurements(mps)
        np.testing.assert_allclose(meter.bonds(1),[-.75 if j%2==0 else 0 for j in range(39)],atol=1e-13)
        np.testing.assert_allclose(meter.bonds(2),0,atol=1e-13)
        self.assertAlmostEqual(meter.norm,1,places=12)

    def test_measurements_are_invariant_under_virtual_gauge(self):
        run=c.dmrg(8,j2=.2,chi=4,max_sweeps=2)
        mps=o.snapshot_mps(run['snapshot'])
        baseline=o.Measurements(mps).bonds(1)
        bond=3; dim=mps[bond].shape[-1]
        rng=np.random.default_rng(709)
        gauge=np.eye(dim)+.05*rng.normal(size=(dim,dim))
        mps[bond]=np.einsum('asb,bc->asc',mps[bond],gauge)
        mps[bond+1]=np.einsum('ab,bsc->asc',np.linalg.inv(gauge),mps[bond+1])
        np.testing.assert_allclose(o.Measurements(mps).bonds(1),baseline,atol=1e-12)

    def test_asymmetric_random_state_cannot_hide_right_reversal_errors(self):
        left=right=c.site()
        for _ in range(5): left=c.enlarge(left,j2=.3)
        for _ in range(3): right=c.enlarge(right,j2=.3)
        rng=np.random.default_rng(1019)
        psi=rng.normal(size=(len(left.q),len(right.q)))
        psi*=left.q[:,None]+right.q[None,:]==0
        psi/=np.linalg.norm(psi)
        _,basis=c.ed_hamiltonian(10)
        v=c.to_ed_state(left,right,psi,basis,10)
        meter=o.Measurements(o.snapshot_mps((left,right,psi)))
        for distance in (1,2):
            np.testing.assert_allclose(meter.bonds(distance),o.bit_bonds(v,basis,10,distance),atol=2e-12)
        full=np.zeros(1<<10); full[basis]=v
        np.testing.assert_allclose(o.tensor_selected_bonds(full,10,[(3,4),(4,5)]),
                                   o.bit_bonds(v,basis,10)[3:5],atol=2e-12)


if __name__=='__main__': unittest.main(verbosity=2)
