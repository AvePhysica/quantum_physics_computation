"""Sparse Hamiltonian construction in a fixed-U(1) sector."""

from __future__ import annotations

import numpy as np
from scipy.sparse import coo_matrix, csr_matrix

from j1j2_basis import basis_index, fixed_popcount_basis


def undirected_bonds(n_sites: int, distance: int) -> list[tuple[int, int]]:
    """Return each physical periodic bond once, including the N=2 special case."""
    bonds: set[tuple[int, int]] = set()
    for site in range(n_sites):
        other = (site + distance) % n_sites
        if site != other:
            bonds.add(tuple(sorted((site, other))))
    return sorted(bonds)


def build_sector_hamiltonian(
    n_sites: int,
    n_up: int,
    *,
    j1: float = 1.0,
    j2: float = 0.0,
    delta: float = 1.0,
) -> csr_matrix:
    basis = fixed_popcount_basis(n_sites, n_up)
    lookup = basis_index(basis)
    rows: list[int] = []
    cols: list[int] = []
    data: list[float] = []
    bond_terms = [(j1, undirected_bonds(n_sites, 1))]
    if j2 != 0.0:
        bond_terms.append((j2, undirected_bonds(n_sites, 2)))

    for column, raw_state in enumerate(basis):
        state = int(raw_state)
        diagonal = 0.0
        for coupling, bonds in bond_terms:
            for a, b in bonds:
                a_up = (state >> a) & 1
                b_up = (state >> b) & 1
                diagonal += coupling * delta * (0.25 if a_up == b_up else -0.25)
                if a_up != b_up:
                    flipped = state ^ (1 << a) ^ (1 << b)
                    rows.append(lookup[flipped])
                    cols.append(column)
                    data.append(0.5 * coupling)
        rows.append(column)
        cols.append(column)
        data.append(diagonal)
    size = len(basis)
    return coo_matrix((data, (rows, cols)), shape=(size, size), dtype=float).tocsr()

