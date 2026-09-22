"""Lecture 02 作业的独立数值校检。"""

import math
import unittest

import numpy as np

from hubbard_model import BONDS, L, SectorBasis, analytic_trace, build_hamiltonian
from observables import (
    density_correlation_matrix,
    double_occupancies,
    local_densities,
    local_spin_z,
    spin_correlation_matrix,
    total_spin_squared,
)
from run_homework import reduce_symmetric_bonds


class HubbardModelTests(unittest.TestCase):
    def test_geometry_has_exactly_the_seven_assigned_bonds(self):
        expected_bonds = {
            (0, 1), (1, 2), (3, 4), (4, 5), (0, 3), (1, 4), (2, 5)
        }
        self.assertEqual(set(BONDS), expected_bonds)

    def test_bond_plot_reduces_seven_bonds_to_three_symmetry_classes(self):
        values = {
            "(0,1)": 0.8, "(1,2)": 0.8, "(3,4)": 0.8, "(4,5)": 0.8,
            "(0,3)": 1.0, "(2,5)": 1.0, "(1,4)": 0.7,
        }
        reduced = reduce_symmetric_bonds(values)
        self.assertEqual([group["multiplicity"] for group in reduced], [4, 2, 1])
        self.assertTrue(np.allclose([group["value"] for group in reduced], [0.8, 1.0, 0.7]))

        values["(1,2)"] = 0.81
        with self.assertRaises(ValueError):
            reduce_symmetric_bonds(values)

    def test_sector_dimension_is_binomial_product(self):
        for n_up, n_down in ((0, 0), (1, 2), (3, 3), (6, 6)):
            basis = SectorBasis.create(n_up, n_down)
            expected = math.comb(L, n_up) * math.comb(L, n_down)
            self.assertEqual(len(basis.states), expected)
            self.assertEqual(len(basis.index), expected)

    def test_hamiltonian_is_hermitian_and_has_analytic_trace(self):
        parameters = dict(t=0.73, u=3.1, v=0.62, mu=1.4)
        for sector in ((1, 2), (3, 3), (5, 4)):
            hamiltonian, basis = build_hamiltonian(*sector, **parameters)
            self.assertTrue(np.allclose(hamiltonian, hamiltonian.conj().T))
            expected_trace = analytic_trace(*sector, **parameters)
            self.assertAlmostEqual(np.trace(hamiltonian).real, expected_trace, places=10)

    def test_atomic_limit_is_diagonal_with_counting_energy(self):
        hamiltonian, basis = build_hamiltonian(2, 1, t=0, u=4, v=1, mu=2)
        self.assertTrue(np.allclose(hamiltonian, np.diag(np.diag(hamiltonian))))
        for column, (up_bits, down_bits) in enumerate(basis.states):
            double = (up_bits & down_bits).bit_count()
            bond_density = sum(
                (((up_bits >> i) & 1) + ((down_bits >> i) & 1))
                * (((up_bits >> j) & 1) + ((down_bits >> j) & 1))
                for i, j in BONDS
            )
            expected = 4 * double + bond_density - 2 * 3
            self.assertAlmostEqual(hamiltonian[column, column].real, expected)

    def test_one_particle_spectrum_matches_one_body_adjacency(self):
        hamiltonian, _ = build_hamiltonian(1, 0, t=1, u=0, v=0, mu=0)
        adjacency = np.zeros((L, L))
        expected_bonds = (
            (0, 1), (1, 2), (3, 4), (4, 5), (0, 3), (1, 4), (2, 5)
        )
        for i, j in expected_bonds:
            adjacency[i, j] = adjacency[j, i] = -1
        self.assertTrue(np.allclose(hamiltonian, adjacency))


class ObservableTests(unittest.TestCase):
    def test_fully_polarized_filled_state_has_known_observables(self):
        hamiltonian, basis = build_hamiltonian(6, 0, t=1, u=4, v=1, mu=4)
        _, eigenvectors = np.linalg.eigh(hamiltonian)
        state = eigenvectors[:, 0]

        self.assertTrue(np.allclose(local_densities(state, basis), 1))
        self.assertTrue(np.allclose(local_spin_z(state, basis), 0.5))
        self.assertTrue(np.allclose(double_occupancies(state, basis), 0))
        self.assertTrue(np.allclose(density_correlation_matrix(state, basis), 1))
        expected_spin = np.full((L, L), 0.25)
        np.fill_diagonal(expected_spin, 0.75)
        self.assertTrue(np.allclose(spin_correlation_matrix(state, basis), expected_spin))
        self.assertAlmostEqual(total_spin_squared(state, basis), 12.0, places=10)

    def test_half_filled_ground_state_obeys_sum_rules_and_hellmann_feynman(self):
        params = dict(t=1.0, u=4.0, v=1.0, mu=4.0)
        hamiltonian, basis = build_hamiltonian(3, 3, **params)
        energies, vectors = np.linalg.eigh(hamiltonian)
        state = vectors[:, 0]

        density = local_densities(state, basis)
        spin_z = local_spin_z(state, basis)
        doubles = double_occupancies(state, basis)
        density_corr = density_correlation_matrix(state, basis)
        spin_corr = spin_correlation_matrix(state, basis)

        self.assertAlmostEqual(np.sum(density), 6.0, places=10)
        self.assertAlmostEqual(np.sum(spin_z), 0.0, places=10)
        self.assertTrue(np.allclose(np.sum(density_corr, axis=1), 6 * density))
        self.assertAlmostEqual(np.sum(spin_corr), total_spin_squared(state, basis), places=10)

        epsilon = 1e-5
        e_u_plus = np.linalg.eigvalsh(
            build_hamiltonian(3, 3, **(params | {"u": params["u"] + epsilon}))[0]
        )[0]
        e_u_minus = np.linalg.eigvalsh(
            build_hamiltonian(3, 3, **(params | {"u": params["u"] - epsilon}))[0]
        )[0]
        derivative_u = (e_u_plus - e_u_minus) / (2 * epsilon)
        self.assertAlmostEqual(derivative_u, np.sum(doubles), places=5)

        e_v_plus = np.linalg.eigvalsh(
            build_hamiltonian(3, 3, **(params | {"v": params["v"] + epsilon}))[0]
        )[0]
        e_v_minus = np.linalg.eigvalsh(
            build_hamiltonian(3, 3, **(params | {"v": params["v"] - epsilon}))[0]
        )[0]
        derivative_v = (e_v_plus - e_v_minus) / (2 * epsilon)
        bond_density = sum(density_corr[i, j] for i, j in BONDS)
        self.assertAlmostEqual(derivative_v, bond_density, places=5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
