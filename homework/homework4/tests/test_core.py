import numpy as np

from j1j2_basis import fixed_popcount_basis, rotate_sites
from j1j2_hamiltonian import build_sector_hamiltonian
from momentum_blocks import momentum_projector, translation_matrix


def test_fixed_popcount_sector_dimensions_sum_to_full_space():
    n_sites = 8
    dimensions = [len(fixed_popcount_basis(n_sites, n_up)) for n_up in range(n_sites + 1)]
    assert dimensions[4] == 70
    assert sum(dimensions) == 2**n_sites


def test_n2_heisenberg_bond_is_counted_once():
    h = build_sector_hamiltonian(2, 1, j1=1.0, j2=0.0, delta=1.0).toarray()
    assert np.allclose(np.linalg.eigvalsh(h), [-0.75, 0.25])


def test_spin_translation_is_unsigned_and_has_order_n():
    n_sites = 4
    basis = fixed_popcount_basis(n_sites, 2)
    t = translation_matrix(n_sites, basis).toarray()
    state = 0b1001
    assert rotate_sites(state, n_sites, 1) == 0b0011
    assert np.all((t == 0.0) | (t == 1.0))
    assert np.allclose(np.linalg.matrix_power(t, n_sites), np.eye(len(basis)))


def test_momentum_projector_has_expected_translation_phase():
    n_sites = 4
    basis = fixed_popcount_basis(n_sites, 2)
    t = translation_matrix(n_sites, basis)
    for m in range(n_sites):
        p = momentum_projector(n_sites, basis, m)
        assert np.allclose((p.conj().T @ p).toarray(), np.eye(p.shape[1]))
        phase = np.exp(2j * np.pi * m / n_sites)
        assert np.allclose((t @ p).toarray(), phase * p.toarray())
