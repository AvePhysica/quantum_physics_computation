from __future__ import annotations

import numpy as np

from hubbard_basis import BlockBasis
from hubbard_operator import HubbardHamiltonian, build_sparse_hamiltonian_independent
from lanczos import (
    continued_fraction,
    direct_resolvent_element,
    lanczos,
    lanczos_relation_residuals,
    lowest_ritz_history,
)
from spectral import (
    apply_local_operator,
    free_fermion_dos,
    local_add_remove_weights,
    particle_hole_channel_relative_error,
    total_density_of_states,
)


def test_lanczos_stops_after_one_vector_for_an_exact_eigenvector() -> None:
    matrix = np.diag([-2.0, 0.5, 3.0])
    result = lanczos(matrix.__matmul__, np.array([1.0, 0.0, 0.0]), 3)
    assert result.n_steps == 1
    np.testing.assert_allclose(result.alphas, [-2.0], atol=1e-14)
    assert result.terminal_beta < 1e-14


def test_lanczos_basis_and_three_term_relation_are_accurate() -> None:
    matrix = np.array(
        [
            [2.0, -1.0, 0.0, 0.0],
            [-1.0, 1.0, 0.4, 0.0],
            [0.0, 0.4, -0.5, 0.7],
            [0.0, 0.0, 0.7, 3.0],
        ]
    )
    start = np.array([1.0, 2.0, -1.0, 0.5])
    result = lanczos(matrix.__matmul__, start, 3)
    orthogonality, constructed_columns, full_relation = lanczos_relation_residuals(
        matrix.__matmul__, result
    )
    assert orthogonality < 1e-12
    assert constructed_columns < 1e-12
    assert full_relation < 1e-12


def test_reverse_continued_fraction_matches_direct_resolvent_at_full_dimension() -> None:
    matrix = np.array(
        [
            [0.3, -0.7, 0.1],
            [-0.7, 1.2, 0.4],
            [0.1, 0.4, -0.8],
        ],
        dtype=float,
    )
    start = np.array([1.0, -0.2, 0.7])
    result = lanczos(matrix.__matmul__, start, 3)
    z = -0.4 + 0.23j
    from_cf = continued_fraction(
        z, result.alphas, result.betas, weight=result.initial_norm**2
    )
    from_solve = direct_resolvent_element(matrix, start, z)
    np.testing.assert_allclose(from_cf, from_solve, atol=1e-12)


def test_forward_recursion_is_detectably_wrong() -> None:
    alphas = np.array([-1.0, 0.3, 2.1, 4.0])
    betas = np.array([0.8, 1.1, 0.5])
    z = 0.7 + 0.11j
    correct = continued_fraction(z, alphas, betas)

    wrong = 0.0j
    for index in range(len(alphas)):
        coupling = 0.0 if index == 0 else betas[index - 1] ** 2 * wrong
        wrong = 1.0 / (z - alphas[index] - coupling)

    assert abs(correct - wrong) > 1e-3


def test_lowest_ritz_values_are_variationally_nonincreasing() -> None:
    matrix = np.diag([-3.0, -0.2, 1.0, 5.0])
    matrix[0, 1] = matrix[1, 0] = 0.4
    matrix[1, 2] = matrix[2, 1] = -0.7
    matrix[2, 3] = matrix[3, 2] = 0.3
    result = lanczos(matrix.__matmul__, np.ones(4), 4)
    history = lowest_ritz_history(result.alphas, result.betas)
    assert np.all(np.diff(history) <= 1e-12)
    np.testing.assert_allclose(history[-1], np.linalg.eigvalsh(matrix)[0], atol=1e-12)


def test_local_creation_and_annihilation_norms_obey_anticommutation_sum_rule() -> None:
    source = BlockBasis(4, 2, 2)
    add_up = BlockBasis(4, 3, 2)
    remove_up = BlockBasis(4, 1, 2)
    rng = np.random.default_rng(17)
    state = rng.normal(size=source.dimension)
    state /= np.linalg.norm(state)

    created = apply_local_operator(source, add_up, state, 1, "up", dagger=True)
    removed = apply_local_operator(source, remove_up, state, 1, "up", dagger=False)
    np.testing.assert_allclose(
        np.vdot(created, created).real + np.vdot(removed, removed).real,
        1.0,
        atol=1e-13,
    )


def test_half_filled_add_and_remove_weights_are_each_n_sites() -> None:
    basis = BlockBasis(4, 2, 2)
    matrix = build_sparse_hamiltonian_independent(
        basis=basis, hopping=1.0, interaction=2.0
    )
    values, vectors = np.linalg.eigh(matrix.toarray())
    ground = vectors[:, np.argmin(values)]
    add_weight, remove_weight, _ = local_add_remove_weights(basis, ground)
    np.testing.assert_allclose(add_weight, 4.0, atol=1e-12)
    np.testing.assert_allclose(remove_weight, 4.0, atol=1e-12)


def test_u_zero_total_dos_matches_free_fermion_formula() -> None:
    n_sites = 4
    basis = BlockBasis(n_sites, 2, 2)
    matrix = build_sparse_hamiltonian_independent(
        basis=basis, hopping=1.0, interaction=0.0
    )
    values, vectors = np.linalg.eigh(matrix.toarray())
    ground_index = int(np.argmin(values))
    omega_shifted = np.linspace(-4.0, 4.0, 121)
    numerical = total_density_of_states(
        source_basis=basis,
        ground_energy=float(values[ground_index]),
        ground_state=vectors[:, ground_index],
        hopping=1.0,
        interaction=0.0,
        eta=0.2,
        omega_shifted=omega_shifted,
        max_lanczos_steps=64,
    )
    exact = free_fermion_dos(omega_shifted, n_sites, 1.0, 0.2)
    relative_max_error = np.max(np.abs(numerical.total - exact)) / np.max(exact)
    assert relative_max_error < 1e-10


def test_particle_hole_error_compares_addition_with_mirrored_removal_pointwise() -> None:
    addition = np.array([0.0, 1.0, 4.0, 2.0])
    removal = np.array([2.0, 4.0, 1.0, 0.0])
    assert particle_hole_channel_relative_error(addition, removal) == 0.0

    removal[1] += 1.0
    np.testing.assert_allclose(
        particle_hole_channel_relative_error(addition, removal),
        0.2,
        atol=1e-15,
    )


def test_hubbard_matrix_free_operator_accepts_lanczos() -> None:
    basis = BlockBasis(4, 2, 2)
    operator = HubbardHamiltonian(basis=basis, hopping=1.0, interaction=4.0)
    start = np.arange(1, basis.dimension + 1, dtype=float)
    result = lanczos(operator.matvec, start, 5)
    assert result.n_steps == 5
    assert np.all(np.isfinite(result.alphas))

