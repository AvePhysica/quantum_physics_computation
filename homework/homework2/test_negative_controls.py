"""故意注入四类错误，确认独立校检确实会拒绝错误结果。"""

import unittest

from negative_controls import evaluate_negative_controls


class NegativeControlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = {
            result["id"]: result for result in evaluate_negative_controls()
        }

    def test_missing_bond_is_detected(self):
        self.assertTrue(self.results["missing_bond"]["detected"])

    def test_flipped_hopping_sign_is_detected(self):
        self.assertTrue(self.results["flipped_hopping_sign"]["detected"])

    def test_missing_u_term_is_detected(self):
        self.assertTrue(self.results["missing_u_term"]["detected"])

    def test_missing_spin_one_half_factor_is_detected(self):
        self.assertTrue(self.results["missing_spin_half_factor"]["detected"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
