"""Numerical eigensolvers used by the homework workflow."""

from __future__ import annotations

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigsh

from j1j2_basis import fixed_popcount_basis
from j1j2_hamiltonian import build_sector_hamiltonian
from momentum_blocks import block_hamiltonian, momentum_projector
from momentum_blocks import translation_matrix


def lowest_eigenpairs(matrix: csr_matrix, count: int = 4) -> tuple[np.ndarray, np.ndarray]:
    dimension = matrix.shape[0]
    if dimension == 0:
        return np.empty(0), np.empty((0, 0), dtype=complex)
    if dimension == 1:
        return np.asarray([float(np.real(matrix[0, 0]))]), np.ones((1, 1), dtype=complex)
    if dimension <= 64 or count >= dimension - 1:
        values, vectors = np.linalg.eigh(matrix.toarray())
        chosen = min(count, dimension)
        return np.real(values[:chosen]), vectors[:, :chosen]
    chosen = min(count, dimension - 2)
    values, vectors = eigsh(matrix, k=chosen, which="SA", tol=1e-11, maxiter=100000)
    order = np.argsort(values)
    return np.real(values[order]), vectors[:, order]


def momentum_ground_table(
    hamiltonian: csr_matrix, basis: np.ndarray, n_sites: int
) -> list[dict[str, float | int]]:
    rows = []
    for m in range(n_sites):
        projector = momentum_projector(n_sites, basis, m)
        block = block_hamiltonian(hamiltonian, projector)
        values, _ = lowest_eigenpairs(block, count=2)
        rows.append(
            {
                "m": m,
                "k_over_pi": 2.0 * m / n_sites,
                "dimension": block.shape[0],
                "energy": float(values[0]),
            }
        )
    return rows


def sector_ground_energies(
    n_sites: int, *, j1: float = 1.0, j2: float = 0.0, delta: float = 1.0
) -> dict[float, float]:
    energies: dict[float, float] = {}
    for n_up in range(n_sites + 1):
        hamiltonian = build_sector_hamiltonian(n_sites, n_up, j1=j1, j2=j2, delta=delta)
        values, _ = lowest_eigenpairs(hamiltonian, count=1)
        magnetization = n_up - n_sites / 2.0
        energies[magnetization] = float(values[0])
    return energies


def ground_momenta_from_subspace(
    hamiltonian: csr_matrix,
    basis: np.ndarray,
    n_sites: int,
    *,
    tolerance: float = 1e-9,
) -> tuple[float, list[int], np.ndarray]:
    """Resolve translation inside the (possibly degenerate) ground subspace."""
    values, vectors = lowest_eigenpairs(hamiltonian, count=min(8, hamiltonian.shape[0]))
    ground_mask = np.abs(values - values[0]) <= tolerance
    ground_vectors = vectors[:, ground_mask]
    translation = translation_matrix(n_sites, basis)
    restricted = ground_vectors.conj().T @ (translation @ ground_vectors)
    phases, rotation = np.linalg.eig(restricted)
    definite_vectors = ground_vectors @ rotation
    for column in range(definite_vectors.shape[1]):
        definite_vectors[:, column] /= np.linalg.norm(definite_vectors[:, column])
    momenta = [int(np.rint((np.angle(phase) % (2.0 * np.pi)) * n_sites / (2.0 * np.pi))) % n_sites for phase in phases]
    order = np.argsort(momenta)
    return float(values[0]), [momenta[index] for index in order], definite_vectors[:, order]

