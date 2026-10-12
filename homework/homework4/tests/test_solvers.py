import numpy as np

from j1j2_basis import fixed_popcount_basis
from j1j2_hamiltonian import build_sector_hamiltonian
from solvers import (
    ground_momenta_from_subspace,
    lowest_eigenpairs,
    momentum_ground_table,
    sector_ground_energies,
)


def test_lowest_eigenpairs_reports_heisenberg_ground_and_degeneracy():
    h = build_sector_hamiltonian(4, 2)
    values, vectors = lowest_eigenpairs(h, count=4)
    assert np.isclose(values[0], -2.0)
    assert np.sum(np.isclose(values, values[0], atol=1e-10)) == 1
    assert np.isclose(np.linalg.norm(vectors[:, 0]), 1.0)


def test_mg_ground_occurs_in_zero_and_pi_blocks():
    n_sites = 8
    basis = fixed_popcount_basis(n_sites, 4)
    h = build_sector_hamiltonian(n_sites, 4, j2=0.5)
    table = momentum_ground_table(h, basis, n_sites)
    ground = min(row["energy"] for row in table)
    ground_m = [row["m"] for row in table if np.isclose(row["energy"], ground, atol=1e-10)]
    assert ground_m == [0, 4]
    assert np.isclose(ground, -3.0)
    assert sum(row["dimension"] for row in table) == len(basis)
    energy, momenta, _ = ground_momenta_from_subspace(h, basis, n_sites)
    assert np.isclose(energy, -3.0)
    assert momenta == [0, 4]


def test_sector_energies_obey_spin_inversion():
    energies = sector_ground_energies(6, j1=1.0, j2=0.2, delta=1.0)
    for magnetization, energy in energies.items():
        assert np.isclose(energy, energies[-magnetization], atol=1e-11)
