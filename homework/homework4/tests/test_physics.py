import numpy as np

from analytics import dimer_product_state, free_fermion_half_filled_energy, normalized_dimer_momenta
from j1j2_basis import fixed_popcount_basis
from j1j2_hamiltonian import build_sector_hamiltonian
from momentum_blocks import block_hamiltonian, momentum_projector, translation_matrix
from observables import (
    local_spin_expectations,
    longitudinal_correlations,
    lower_envelope_transitions,
    spin_correlations,
    structure_factor,
)


def test_n4_heisenberg_ground_energy_is_minus_two():
    h = build_sector_hamiltonian(4, 2, j1=1.0, j2=0.0, delta=1.0)
    assert np.isclose(np.linalg.eigvalsh(h.toarray())[0], -2.0)


def test_momentum_block_spectra_union_matches_u1_spectrum():
    n_sites = 8
    basis = fixed_popcount_basis(n_sites, 4)
    h = build_sector_hamiltonian(n_sites, 4, j1=1.0, j2=0.5, delta=1.0)
    block_values = []
    for m in range(n_sites):
        p = momentum_projector(n_sites, basis, m)
        block_values.extend(np.linalg.eigvalsh(block_hamiltonian(h, p).toarray()))
    assert np.allclose(np.sort(block_values), np.linalg.eigvalsh(h.toarray()), atol=1e-11)


def test_majumdar_ghosh_dimer_states_are_exact_and_have_0_pi_momenta():
    n_sites = 8
    basis = fixed_popcount_basis(n_sites, n_sites // 2)
    h = build_sector_hamiltonian(n_sites, n_sites // 2, j1=1.0, j2=0.5, delta=1.0)
    d0 = dimer_product_state(n_sites, basis, shift=0)
    d1 = dimer_product_state(n_sites, basis, shift=1)
    expected = -3.0 * n_sites / 8.0
    assert np.linalg.norm(h @ d0 - expected * d0) < 1e-12
    assert np.linalg.norm(h @ d1 - expected * d1) < 1e-12
    plus, minus = normalized_dimer_momenta(d0, d1)
    t = translation_matrix(n_sites, basis)
    assert np.linalg.norm(t @ plus - plus) < 1e-12
    assert np.linalg.norm(t @ minus + minus) < 1e-12


def test_fixed_sector_state_has_zero_sx_and_total_sz_sum_rule():
    n_sites = 4
    basis = fixed_popcount_basis(n_sites, 2)
    h = build_sector_hamiltonian(n_sites, 2)
    _, vectors = np.linalg.eigh(h.toarray())
    sz, sx = local_spin_expectations(vectors[:, 0], basis, n_sites)
    assert np.allclose(sz, 0.0, atol=1e-12)
    assert np.allclose(sx, 0.0, atol=1e-12)
    correlations = spin_correlations(vectors[:, 0], basis, n_sites)
    assert np.isclose(np.sum(correlations), 0.0, atol=1e-12)
    sq = structure_factor(correlations)
    assert np.isclose(np.sum(sq), correlations[0], atol=1e-12)
    assert np.isclose(correlations[0], 0.75, atol=1e-12)
    longitudinal = longitudinal_correlations(vectors[:, 0], basis, n_sites)
    assert np.allclose(correlations, 3.0 * longitudinal, atol=1e-12)


def test_xx_free_fermion_result_matches_exact_spin_ground_energy():
    for n_sites in (8, 10, 12):
        h = build_sector_hamiltonian(n_sites, n_sites // 2, delta=0.0)
        exact = np.linalg.eigvalsh(h.toarray())[0]
        analytic = free_fermion_half_filled_energy(n_sites)
        assert np.isclose(analytic.energy, exact, atol=1e-11)
        assert analytic.boundary in {"periodic", "antiperiodic"}


def test_lower_envelope_skips_nonconvex_sector():
    hull, transitions = lower_envelope_transitions({0.0: 0.0, 1.0: 2.0, 2.0: 3.0})
    assert hull == [(0.0, 0.0), (2.0, 3.0)]
    assert transitions == [(0.0, 2.0, 1.5)]
