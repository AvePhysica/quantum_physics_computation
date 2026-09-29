from __future__ import annotations

from math import comb

import numpy as np

from hubbard_basis import (
    BlockBasis,
    apply_fermion_to_state,
    enumerate_masks,
)
from hubbard_operator import (
    HubbardHamiltonian,
    build_sparse_hamiltonian_independent,
    expected_interaction_trace,
)


def test_enumerate_masks_has_fixed_particle_number_and_lexicographic_integer_order() -> None:
    masks = enumerate_masks(4, 2)
    assert masks.tolist() == [3, 5, 6, 9, 10, 12]
    assert all(int(mask).bit_count() == 2 for mask in masks)


def test_block_dimension_and_lookup_match_combinatorics() -> None:
    basis = BlockBasis(6, 2, 3)
    assert basis.dimension == comb(6, 2) * comb(6, 3)

    for index in (0, basis.dimension // 2, basis.dimension - 1):
        up_mask, down_mask = basis.state(index)
        assert basis.index(up_mask, down_mask) == index


def test_fermion_sign_uses_global_up_then_down_orbital_order() -> None:
    # Occupied orbitals are up-0, up-2, down-1 in the declared global order.
    up_mask = 0b0101
    down_mask = 0b0010

    created = apply_fermion_to_state(
        up_mask, down_mask, n_sites=4, site=2, spin="down", dagger=True
    )
    assert created is not None
    new_up, new_down, sign = created
    assert (new_up, new_down) == (up_mask, 0b0110)
    assert sign == -1  # Three occupied orbitals precede down-2.

    assert (
        apply_fermion_to_state(
            up_mask, down_mask, n_sites=4, site=2, spin="up", dagger=True
        )
        is None
    )


def test_matrix_free_action_matches_independently_assembled_sparse_matrix() -> None:
    basis = BlockBasis(4, 2, 1)
    operator = HubbardHamiltonian(basis=basis, hopping=1.3, interaction=2.7)
    sparse = build_sparse_hamiltonian_independent(
        basis=basis, hopping=1.3, interaction=2.7
    )
    rng = np.random.default_rng(20260928)
    vector = rng.normal(size=basis.dimension) + 1j * rng.normal(
        size=basis.dimension
    )

    np.testing.assert_allclose(operator.matvec(vector), sparse @ vector, atol=1e-12)


def test_sparse_hamiltonian_is_hermitian() -> None:
    basis = BlockBasis(5, 2, 2)
    matrix = build_sparse_hamiltonian_independent(
        basis=basis, hopping=0.8, interaction=3.1
    )
    difference = matrix - matrix.getH()
    assert np.linalg.norm(difference.data) < 1e-13


def test_interaction_trace_matches_closed_combinatorial_formula() -> None:
    basis = BlockBasis(6, 2, 4)
    interaction = 3.25
    matrix = build_sparse_hamiltonian_independent(
        basis=basis, hopping=1.0, interaction=interaction
    )
    measured = float(np.real(matrix.diagonal().sum()))
    expected = expected_interaction_trace(basis, interaction)
    assert measured == expected


def test_consistency_check_detects_flipped_hopping_sign() -> None:
    basis = BlockBasis(4, 2, 2)
    correct = HubbardHamiltonian(basis=basis, hopping=1.0, interaction=2.0)
    wrong = build_sparse_hamiltonian_independent(
        basis=basis, hopping=-1.0, interaction=2.0
    )
    probe = np.arange(1, basis.dimension + 1, dtype=float)
    assert np.linalg.norm(correct.matvec(probe) - wrong @ probe) > 1.0


def test_consistency_check_detects_missing_periodic_bond() -> None:
    basis = BlockBasis(4, 2, 1)
    correct = HubbardHamiltonian(basis=basis, hopping=1.0, interaction=2.0)
    open_chain_bonds = [(site, site + 1) for site in range(3)]
    wrong = build_sparse_hamiltonian_independent(
        basis=basis,
        hopping=1.0,
        interaction=2.0,
        bonds=open_chain_bonds,
    )
    probe = np.arange(1, basis.dimension + 1, dtype=float)
    assert np.linalg.norm(correct.matvec(probe) - wrong @ probe) > 1.0


def test_trace_check_detects_removed_interaction() -> None:
    basis = BlockBasis(4, 2, 2)
    wrong = build_sparse_hamiltonian_independent(
        basis=basis, hopping=1.0, interaction=0.0
    )
    expected = expected_interaction_trace(basis, interaction=4.0)
    assert not np.isclose(float(wrong.diagonal().sum()), expected)

