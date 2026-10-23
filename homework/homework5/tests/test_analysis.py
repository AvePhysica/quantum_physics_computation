import sys
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
import unittest
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
try:
    from src import analysis as a
except ImportError:
    a=None
from src import core as c


class AnalysisTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(a,'Analysis functions are not implemented')

    def test_dimer_action_and_entropy(self):
        h,b=c.ed_hamiltonian(8,j2=.5)
        v=a.dimer(b,8)
        self.assertLess(np.linalg.norm(h@v+3*v),1e-14)
        full=a.full_state(v,b,8)
        s=a.entropies(full,8)
        np.testing.assert_allclose(s,[np.log(2),0,np.log(2),0,np.log(2),0,np.log(2)],atol=1e-13)
        np.testing.assert_allclose(s,a.entropies(full,8,method='rho'),atol=1e-13)

    def test_projection_energy_is_direct_physical_expectation(self):
        h,b=c.ed_hamiltonian(12)
        e,v=c.ground(h)
        rows=a.compare_truncations(h,b,v,12,[2,4,6,8,12,16])
        for row in rows:
            self.assertGreaterEqual(row['dm_error'],-1e-12)
            self.assertGreaterEqual(row['energy_error'],-1e-12)
            self.assertLess(row['dm_check'],1e-10)
            self.assertLess(row['energy_check'],1e-10)
            self.assertLessEqual(row['dm_error'],row['energy_error']+1e-10)


if __name__=='__main__': unittest.main(verbosity=2)
