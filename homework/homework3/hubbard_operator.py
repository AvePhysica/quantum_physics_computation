"""Hubbard Hamiltonian in a fixed particle-number block."""

from __future__ import annotations

from dataclasses import dataclass, field
from math import comb
from typing import Iterable

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import LinearOperator, eigsh

from hubbard_basis import BlockBasis, Spin, apply_hop_to_state


@dataclass
class HubbardHamiltonian:
    """Matrix-free periodic one-dimensional Hubbard Hamiltonian.

    Hopping transitions are precomputed as integer lookup data, but no sparse
    or dense Hamiltonian matrix is required by :meth:`matvec`.
    """

    basis: BlockBasis
    hopping: float
    interaction: float
    _double_occupancies: np.ndarray = field(init=False, repr=False)
    _sources: np.ndarray = field(init=False, repr=False)
    _targets: np.ndarray = field(init=False, repr=False)
    _hop_signs: np.ndarray = field(init=False, repr=False)

    def __post_init__(self) -> None:
        double_occupancies = np.empty(self.basis.dimension, dtype=np.int16)
        sources: list[int] = []
        targets: list[int] = []
        signs: list[int] = []
        n_sites = self.basis.n_sites

        for source_index, up_mask, down_mask in self.basis.iter_states():
            double_occupancies[source_index] = (up_mask & down_mask).bit_count()
            for site in range(n_sites):
                neighbor = (site + 1) % n_sites
                for spin in ("up", "down"):
                    for source_site, destination_site in (
                        (site, neighbor),
                        (neighbor, site),
                    ):
                        hopped = apply_hop_to_state(
                            up_mask,
                            down_mask,
                            n_sites,
                            source_site,
                            destination_site,
                            spin,
                        )
                        if hopped is None:
                            continue
                        new_up, new_down, sign = hopped
                        sources.append(source_index)
                        targets.append(self.basis.index(new_up, new_down))
                        signs.append(sign)

        self._double_occupancies = double_occupancies
        self._sources = np.asarray(sources, dtype=np.int64)
        self._targets = np.asarray(targets, dtype=np.int64)
        self._hop_signs = np.asarray(signs, dtype=np.int8)

    @property
    def shape(self) -> tuple[int, int]:
        return self.basis.dimension, self.basis.dimension

    def matvec(self, vector: np.ndarray) -> np.ndarray:
        """Return ``H @ vector`` without constructing ``H``."""

        vector = np.asarray(vector)
        if vector.ndim != 1 or vector.shape[0] != self.basis.dimension:
            raise ValueError("vector has the wrong shape for this symmetry block")
        dtype = np.result_type(vector.dtype, np.float64)
        result = (
            self.interaction * self._double_occupancies.astype(float) * vector
        ).astype(dtype, copy=False)
        hopping_values = -self.hopping * self._hop_signs * vector[self._sources]
        np.add.at(result, self._targets, hopping_values)
        return result

    def as_linear_operator(self) -> LinearOperator:
        return LinearOperator(self.shape, matvec=self.matvec, dtype=np.float64)


def _independent_single_spin_hop(
    mask: int,
    source_site: int,
    destination_site: int,
) -> tuple[int, int] | None:
    """Independent sign implementation used only by sparse assembly."""

    if not (mask >> source_site) & 1 or (mask >> destination_site) & 1:
        return None
    after_annihilation = mask ^ (1 << source_site)
    sign_annihilation = -1 if (mask & ((1 << source_site) - 1)).bit_count() % 2 else 1
    sign_creation = (
        -1
        if (after_annihilation & ((1 << destination_site) - 1)).bit_count() % 2
        else 1
    )
    final_mask = after_annihilation | (1 << destination_site)
    return final_mask, sign_annihilation * sign_creation


def build_sparse_hamiltonian_independent(
    basis: BlockBasis,
    hopping: float,
    interaction: float,
    bonds: Iterable[tuple[int, int]] | None = None,
) -> sparse.csr_matrix:
    """Assemble an explicit CSR Hamiltonian using independent hopping logic.

    ``bonds=None`` selects the periodic ring.  Supplying a bond list is useful
    for controlled boundary-condition checks.
    """

    if bonds is None:
        bond_list = [(site, (site + 1) % basis.n_sites) for site in range(basis.n_sites)]
    else:
        bond_list = list(bonds)

    rows: list[int] = []
    columns: list[int] = []
    values: list[float] = []
    for column, up_mask, down_mask in basis.iter_states():
        diagonal = interaction * (up_mask & down_mask).bit_count()
        rows.append(column)
        columns.append(column)
        values.append(diagonal)

        for left, right in bond_list:
            for spin in ("up", "down"):
                active_mask = up_mask if spin == "up" else down_mask
                for source_site, destination_site in ((left, right), (right, left)):
                    hopped = _independent_single_spin_hop(
                        active_mask, source_site, destination_site
                    )
                    if hopped is None:
                        continue
                    new_active_mask, sign = hopped
                    if spin == "up":
                        new_up, new_down = new_active_mask, down_mask
                    else:
                        new_up, new_down = up_mask, new_active_mask
                    rows.append(basis.index(new_up, new_down))
                    columns.append(column)
                    values.append(-hopping * sign)

    matrix = sparse.coo_matrix(
        (values, (rows, columns)), shape=(basis.dimension, basis.dimension), dtype=float
    )
    matrix.sum_duplicates()
    return matrix.tocsr()


def expected_interaction_trace(basis: BlockBasis, interaction: float) -> float:
    """Closed-form trace of the Hubbard interaction in one symmetry block."""

    if basis.n_up == 0 or basis.n_down == 0:
        return 0.0
    per_site = comb(basis.n_sites - 1, basis.n_up - 1) * comb(
        basis.n_sites - 1, basis.n_down - 1
    )
    return float(interaction * basis.n_sites * per_site)


def lowest_eigenpairs(
    operator: HubbardHamiltonian | sparse.spmatrix,
    n_eigenpairs: int = 8,
    tolerance: float = 1e-12,
    initial_vector: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Return sorted low-energy eigenpairs without dense diagonalization."""

    dimension = operator.shape[0]
    if dimension < 2:
        vector = np.ones((dimension, 1), dtype=float)
        if isinstance(operator, HubbardHamiltonian):
            value = float(np.real(operator.matvec(vector[:, 0])[0]))
        else:
            value = float(np.real(operator[0, 0]))
        return np.asarray([value]), vector
    k = min(n_eigenpairs, dimension - 1)
    linear_operator = (
        operator.as_linear_operator()
        if isinstance(operator, HubbardHamiltonian)
        else operator
    )
    values, vectors = eigsh(
        linear_operator,
        k=k,
        which="SA",
        tol=tolerance,
        v0=initial_vector,
    )
    order = np.argsort(values)
    return np.asarray(values[order]), np.asarray(vectors[:, order])


def ground_state_degeneracy(
    eigenvalues: np.ndarray,
    absolute_tolerance: float = 1e-9,
) -> int:
    """Count computed eigenvalues numerically equal to the lowest one."""

    values = np.asarray(eigenvalues, dtype=float)
    if values.ndim != 1 or values.size == 0:
        raise ValueError("at least one eigenvalue is required")
    return int(np.count_nonzero(np.abs(values - values[0]) <= absolute_tolerance))

