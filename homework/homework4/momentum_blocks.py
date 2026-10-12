"""Translation-orbit momentum blocks in a fixed magnetization sector."""

from __future__ import annotations

import numpy as np
from scipy.sparse import coo_matrix, csr_matrix

from j1j2_basis import basis_index, rotate_sites


def translation_matrix(n_sites: int, basis: np.ndarray) -> csr_matrix:
    lookup = basis_index(basis)
    columns = np.arange(len(basis), dtype=int)
    rows = np.asarray([lookup[rotate_sites(int(s), n_sites)] for s in basis])
    return coo_matrix((np.ones(len(basis)), (rows, columns)), shape=(len(basis), len(basis))).tocsr()


def translation_orbits(n_sites: int, basis: np.ndarray) -> list[list[int]]:
    allowed = {int(state) for state in basis}
    unseen = set(allowed)
    orbits: list[list[int]] = []
    while unseen:
        representative = min(unseen)
        orbit = []
        state = representative
        while state not in orbit:
            orbit.append(state)
            state = rotate_sites(state, n_sites)
        unseen.difference_update(orbit)
        orbits.append(orbit)
    return orbits


def momentum_projector(n_sites: int, basis: np.ndarray, m: int) -> csr_matrix:
    """Columns obey T|r;k> = exp(+ik)|r;k>, k=2*pi*m/N."""
    lookup = basis_index(basis)
    k = 2.0 * np.pi * m / n_sites
    columns_data: list[tuple[list[int], list[complex]]] = []
    for orbit in translation_orbits(n_sites, basis):
        length = len(orbit)
        if (m * length) % n_sites != 0:
            continue
        rows = [lookup[state] for state in orbit]
        values = [np.exp(-1j * k * power) / np.sqrt(length) for power in range(length)]
        columns_data.append((rows, values))
    rows_out: list[int] = []
    cols_out: list[int] = []
    values_out: list[complex] = []
    for column, (rows, values) in enumerate(columns_data):
        rows_out.extend(rows)
        cols_out.extend([column] * len(rows))
        values_out.extend(values)
    return coo_matrix(
        (values_out, (rows_out, cols_out)),
        shape=(len(basis), len(columns_data)),
        dtype=complex,
    ).tocsr()


def block_hamiltonian(hamiltonian: csr_matrix, projector: csr_matrix) -> csr_matrix:
    return (projector.conj().T @ hamiltonian @ projector).tocsr()

