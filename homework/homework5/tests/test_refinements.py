"""Analytic regression cases for error scaling and same-size baseline subtraction."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import sys
from pathlib import Path
import unittest
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
try:
    from src import refinements as r
except ImportError:
    r=None


class RefinementTests(unittest.TestCase):
    def setUp(self): self.assertIsNotNone(r,'Review analysis is not implemented')

    def test_proportional_errors_give_unit_power_and_known_coefficient(self):
        x=np.array([1e-3,1e-5,1e-7,1e-9])
        fit=r.scaling_fit(x,7*x)
        self.assertAlmostEqual(fit['power'],1,places=12)
        self.assertAlmostEqual(fit['amplitude'],7,places=12)
        self.assertAlmostEqual(fit['r2_log'],1,places=12)
        self.assertAlmostEqual(fit['origin_slope'],7,places=12)
        self.assertLess(abs(fit['linear_intercept']),1e-17)

    def test_nonunit_power_is_measured_not_forced(self):
        x=np.geomspace(1e-8,1e-2,6)
        fit=r.scaling_fit(x,3*x**1.5)
        self.assertAlmostEqual(fit['power'],1.5,places=12)
        self.assertAlmostEqual(fit['amplitude'],3,places=12)
        with self.assertRaises(ValueError): r.scaling_fit([0,1],[0,1])

    def test_affine_intercept_and_independent_fit(self):
        x=np.array([1e-3,2e-3,3e-3,4e-3]); y=2*x+1e-5
        fit=r.scaling_fit(x,y)
        self.assertAlmostEqual(fit['linear_slope'],2,places=12)
        self.assertAlmostEqual(fit['linear_intercept'],1e-5,places=15)
        self.assertLess(fit['independent_power_difference'],1e-12)
        self.assertLess(fit['independent_intercept_difference'],1e-12)

    def test_energy_intercept_uses_signed_energy_errors(self):
        x=np.array([1e-3,2e-3,3e-3,4e-3]); signed=-(2*x+1e-5)
        fit=r.scaling_fit(x,abs(signed),signed_errors=signed)
        self.assertAlmostEqual(fit['linear_slope'],-2,places=12)
        self.assertAlmostEqual(fit['linear_intercept'],-1e-5,places=15)

    def test_enrichment_rejects_incomplete_or_duplicate_chi_sets(self):
        row=dict(n=20,j2=0.,chi=4)
        with self.assertRaises(ValueError): r.enrich(dict(dmrg=[row]))
        with self.assertRaises(ValueError): r.enrich(dict(dmrg=[row.copy() for _ in range(4)]))

    def test_baseline_is_same_size_same_method_and_abs_before_subtraction(self):
        scan=[]
        for n,method,base in ((12,'ED',.2),(20,'ED',.15),(20,'DMRG',.151)):
            for j,d in ((0.,base),(.5,.75)):
                scan.append(dict(n=n,method=method,j2=j,dimer=d,signed_dimer=-d,
                                 central_values=[-.1-d,-.1],chi=64 if method=='DMRG' else None))
        values=r.baseline_subtraction(scan)
        for row in values:
            if row['j2']==0: self.assertEqual(row['enhancement'],0)
            elif row['n']==12: self.assertAlmostEqual(row['enhancement'],.55)
            elif row['method']=='ED': self.assertAlmostEqual(row['enhancement'],.60)
            else: self.assertAlmostEqual(row['enhancement'],.599)
        # If the signed difference changes sign, |d(J)|-|d(0)| must not be
        # replaced by |d(J)-d(0)|. Those are distinct physical conventions.
        flip=[dict(n=12,method='ED',j2=0.,dimer=.2,signed_dimer=-.2,central_values=[-.4,-.2]),
              dict(n=12,method='ED',j2=.1,dimer=.1,signed_dimer=.1,central_values=[-.1,-.2])]
        self.assertAlmostEqual(r.baseline_subtraction(flip)[1]['enhancement'],-.1)


if __name__=='__main__': unittest.main(verbosity=2)
