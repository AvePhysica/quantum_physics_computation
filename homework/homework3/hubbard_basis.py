"""Fixed-particle-number Fock bases and fermionic operators.

The global spin-orbital order is

    up-0, up-1, ..., up-(N-1), down-0, ..., down-(N-1).

Each spin species is still stored as its own N-bit integer, as required by the
assignment.  The global ordering is used only to compute fermionic signs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import combinations
from typing import Literal

import numpy as np


Spin = Literal["up", "down"]


def enumerate_masks(n_sites: int, n_particles: int) -> np.ndarray:
    """Return all N-bit masks with a fixed number of set bits.

    Masks are sorted by their integer value.  This convention makes the basis
    order deterministic across platforms and Python versions.
    """

    if n_sites < 1:
        raise ValueError("n_sites must be positive")
    if not 0 <= n_particles <= n_sites:
        raise ValueError("n_particles must lie between 0 and n_sites")

    masks = [sum(1 << site for site in occupied) for occupied in combinations(range(n_sites), n_particles)]
    return np.asarray(sorted(masks), dtype=np.int64)


@dataclass(frozen=True)
class BlockBasis:
    """Basis of a fixed (N_up, N_down) U(1) x U(1) symmetry block."""

    n_sites: int
    n_up: int
    n_down: int
    up_masks: np.ndarray = field(init=False, repr=False, compare=False)
    down_masks: np.ndarray = field(init=False, repr=False, compare=False)
    up_lookup: np.ndarray = field(init=False, repr=False, compare=False)
    down_lookup: np.ndarray = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        up_masks = enumerate_masks(self.n_sites, self.n_up)
        down_masks = enumerate_masks(self.n_sites, self.n_down)
        lookup_size = 1 << self.n_sites
        up_lookup = np.full(lookup_size, -1, dtype=np.int64)
        down_lookup = np.full(lookup_size, -1, dtype=np.int64)
        up_lookup[up_masks] = np.arange(len(up_masks), dtype=np.int64)
        down_lookup[down_masks] = np.arange(len(down_masks), dtype=np.int64)
        object.__setattr__(self, "up_masks", up_masks)
        object.__setattr__(self, "down_masks", down_masks)
        object.__setattr__(self, "up_lookup", up_lookup)
        object.__setattr__(self, "down_lookup", down_lookup)

    @property
    def dimension(self) -> int:
        return int(len(self.up_masks) * len(self.down_masks))

    def state(self, index: int) -> tuple[int, int]:
        """Return ``(up_mask, down_mask)`` for a block-basis index."""

        if not 0 <= index < self.dimension:
            raise IndexError("basis index out of range")
        up_rank, down_rank = divmod(index, len(self.down_masks))
        return int(self.up_masks[up_rank]), int(self.down_masks[down_rank])

    def index(self, up_mask: int, down_mask: int) -> int:
        """Look up a basis index in O(1) time."""

        limit = 1 << self.n_sites
        if not (0 <= up_mask < limit and 0 <= down_mask < limit):
            raise KeyError("mask lies outside the declared number of sites")
        up_rank = int(self.up_lookup[up_mask])
        down_rank = int(self.down_lookup[down_mask])
        if up_rank < 0 or down_rank < 0:
            raise KeyError("state is not in this particle-number block")
        return up_rank * len(self.down_masks) + down_rank

    def iter_states(self):
        """Yield ``(index, up_mask, down_mask)`` in basis order."""

        n_down_masks = len(self.down_masks)
        for up_rank, up_mask in enumerate(self.up_masks):
            offset = up_rank * n_down_masks
            for down_rank, down_mask in enumerate(self.down_masks):
                yield offset + down_rank, int(up_mask), int(down_mask)


def _orbital_index(n_sites: int, site: int, spin: Spin) -> int:
    if not 0 <= site < n_sites:
        raise IndexError("site out of range")
    if spin == "up":
        return site
    if spin == "down":
        return n_sites + site
    raise ValueError("spin must be 'up' or 'down'")


def apply_fermion_to_state(
    up_mask: int,
    down_mask: int,
    n_sites: int,
    site: int,
    spin: Spin,
    dagger: bool,
) -> tuple[int, int, int] | None:
    """Apply one creation or annihilation operator to a Fock state.

    Returns ``(new_up_mask, new_down_mask, sign)`` or ``None`` when Pauli
    exclusion makes the action vanish.
    """

    orbital = _orbital_index(n_sites, site, spin)
    full_mask = int(up_mask) | (int(down_mask) << n_sites)
    occupied = bool(full_mask & (1 << orbital))
    if dagger == occupied:
        return None

    parity_mask = (1 << orbital) - 1
    sign = -1 if (full_mask & parity_mask).bit_count() % 2 else 1
    if dagger:
        full_mask |= 1 << orbital
    else:
        full_mask &= ~(1 << orbital)

    site_mask = (1 << n_sites) - 1
    return full_mask & site_mask, full_mask >> n_sites, sign


def apply_hop_to_state(
    up_mask: int,
    down_mask: int,
    n_sites: int,
    source_site: int,
    destination_site: int,
    spin: Spin,
) -> tuple[int, int, int] | None:
    """Apply ``c^dagger_destination c_source`` to one Fock state."""

    annihilated = apply_fermion_to_state(
        up_mask,
        down_mask,
        n_sites,
        source_site,
        spin,
        dagger=False,
    )
    if annihilated is None:
        return None
    middle_up, middle_down, first_sign = annihilated
    created = apply_fermion_to_state(
        middle_up,
        middle_down,
        n_sites,
        destination_site,
        spin,
        dagger=True,
    )
    if created is None:
        return None
    final_up, final_down, second_sign = created
    return final_up, final_down, first_sign * second_sign

