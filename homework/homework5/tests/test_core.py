"""Independent physics and truncation regression tests (unittest, no pytest needed)."""
import sys
import unittest
from unittest.mock import patch
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from src import core as c
except ImportError:
    c = None


class CoreTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(c, 'DMRG core has not been implemented')

    def test_two_spin_normalization(self):
        h, _ = c.ed_hamiltonian(2, full=True)
        np.testing.assert_allclose(np.linalg.eigvalsh(h.toarray()), [-.75,.25,.25,.25], atol=1e-14)

    def test_global_charge_selection_and_discard(self):
        # Largest two weights are in DIFFERENT charge sectors. A per-sector cap is wrong.
        q = np.array([-2,0,0,2])
        psi = np.zeros((4,4))
        psi[0,3],psi[1,1],psi[2,2],psi[3,0] = np.sqrt([.4,.3,.2,.1])
        t, qt, w, eps = c.truncate(psi,q,q,2)
        self.assertEqual(t.shape,(4,2))
        np.testing.assert_allclose(w,[.4,.3],atol=1e-14)
        self.assertAlmostEqual(eps,.3,places=13)
        np.testing.assert_allclose(t.T@t,np.eye(2),atol=1e-14)
        np.testing.assert_allclose(q[:,None]*t,t*qt[None,:],atol=1e-14)
        self.assertAlmostEqual(np.linalg.norm(psi-t@(t.T@psi))**2,eps,places=13)

    def test_asymmetric_charge_svd_and_zero_weights(self):
        qa=np.array([-3,-1,-1,-1,1,1,1,3]); qb=np.array([-1,1])
        psi=np.zeros((8,2)); psi[1,1]=np.sqrt(.7); psi[4,0]=np.sqrt(.3)
        t,q,w,eps=c.truncate(psi,qa,qb,6)
        self.assertEqual(t.shape,(8,6))
        np.testing.assert_allclose(t.T@t,np.eye(6),atol=1e-14)
        self.assertAlmostEqual(eps,0,places=13)

    def test_untruncated_superblock_and_edge_positions(self):
        for j2 in (0,.3,.5):
            for n in (4,6,8):
                b=c.site()
                for _ in range(n//2-2):
                    b=c.enlarge(b,1,j2,.73)
                a=c.enlarge(b,1,j2,.73)
                sol=c.solve_super(a,a,1,j2,.73)
                h,basis=c.ed_hamiltonian(n,j2=j2,delta=.73)
                e,_=c.ground(h)
                self.assertAlmostEqual(sol['energy'],e,places=10)
                v=c.to_ed_state(a,a,sol['psi'],basis,n)
                self.assertLess(np.linalg.norm(h@v-e*v),1e-9)

    def test_real_truncation_and_finite_sweep(self):
        run=c.dmrg(10,j2=.3,chi=4,max_sweeps=3)
        self.assertTrue(any(r['eps_max']>1e-8 for r in run['growth']))
        self.assertLessEqual(max(run['dimensions']),4)
        h,basis=c.ed_hamiltonian(10,j2=.3)
        e,_=c.ground(h)
        a,b,psi=run['snapshot']
        v=c.to_ed_state(a,b,psi,basis,10)
        measured=float(v@(h@v))
        self.assertAlmostEqual(measured,run['energy'],places=9)
        self.assertGreaterEqual(measured,e-1e-10)
        self.assertLess(measured-e,.03)
        self.assertLessEqual(run['sweeps'][-1]['energy'],run['growth'][-1]['energy']+1e-9)

    def test_every_local_sweep_position_against_physical_hamiltonian(self):
        original=c.solve_super
        positions=set(); cache={}; observed=[]
        def audited(a,b,j1,j2,delta):
            sol=original(a,b,j1,j2,delta)
            n=a.length+b.length
            if n not in cache:
                cache[n]=c.ed_hamiltonian(n,j1,j2,delta)
            h,basis=cache[n]
            v=c.to_ed_state(a,b,sol['psi'],basis,n)
            observed.append(abs(float(v@(h@v))-sol['energy']))
            if n==10: positions.add(a.length-1)
            return sol
        with patch.object(c,'solve_super',side_effect=audited):
            c.dmrg(10,j2=.3,delta=.73,chi=2,max_sweeps=2)
        self.assertEqual(positions,set(range(1,8)))
        self.assertGreater(len(observed),30)
        self.assertLess(max(observed),1e-10)


if __name__=='__main__':
    unittest.main(verbosity=2)
