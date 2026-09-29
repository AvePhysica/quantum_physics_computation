from __future__ import annotations

import numpy as np

from hubbard_basis import BlockBasis
from run_homework3 import (
    _closed_shell_gap,
    _select_extremal_local_density_ground_state,
)


def test_closed_shell_criterion_distinguishes_n6_and_n8_half_filling() -> None:
    assert _closed_shell_gap(6, 3, 1.0) > 1.0
    assert abs(_closed_shell_gap(8, 4, 1.0)) < 1e-12


def test_extremal_density_selector_chooses_a_symmetry_broken_ground_vector() -> None:
    basis = BlockBasis(2, 1, 1)
    eigenvalues = np.array([0.0, 0.0])
    eigenvectors = np.zeros((basis.dimension, 2))
    doubly_occupied_site_zero = basis.index(0b01, 0b01)
    empty_site_zero = basis.index(0b10, 0b10)
    eigenvectors[doubly_occupied_site_zero, 0] = 1.0
    eigenvectors[empty_site_zero, 1] = 1.0

    chosen = _select_extremal_local_density_ground_state(
        basis, eigenvalues, eigenvectors, tolerance=1e-12, site=0
    )
    np.testing.assert_allclose(abs(chosen[doubly_occupied_site_zero]), 1.0)

