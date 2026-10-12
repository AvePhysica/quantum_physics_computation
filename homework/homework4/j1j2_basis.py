"""Bit-basis helpers for the spin-1/2 J1-J2 ring.

Bit j labels site j and bit value 1 means spin up.  Translation is a
permutation of tensor-product spin states, so it never acquires a fermionic
exchange sign.
"""

from __future__ import annotations

from itertools import combinations

import numpy as np


def fixed_popcount_basis(n_sites: int, n_up: int) -> np.ndarray:
    """Return all N-bit integers with exactly ``n_up`` set bits."""
    if not 0 <= n_up <= n_sites:
        return np.empty(0, dtype=np.uint64)
    states = []
    for occupied in combinations(range(n_sites), n_up):
        state = 0
        for site in occupied:
            state |= 1 << site
        states.append(state)
    return np.asarray(states, dtype=np.uint64)


def rotate_sites(state: int, n_sites: int, shift: int = 1) -> int:
    """Apply T**shift, with T moving site j to site j+1 modulo N."""
    shift %= n_sites
    mask = (1 << n_sites) - 1
    value = int(state) & mask
    if shift == 0:
        return value
    return ((value << shift) & mask) | (value >> (n_sites - shift))


def basis_index(basis: np.ndarray) -> dict[int, int]:
    return {int(state): index for index, state in enumerate(basis)}

