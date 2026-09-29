"""Lanczos tridiagonalization and Green functions by continued fractions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve


Matvec = Callable[[np.ndarray], np.ndarray]


@dataclass(frozen=True)
class LanczosResult:
    """Finite Lanczos chain with an optional terminal residual vector."""

    alphas: np.ndarray
    betas: np.ndarray
    vectors: np.ndarray
    initial_norm: float
    terminal_beta: float
    terminal_vector: np.ndarray | None

    @property
    def n_steps(self) -> int:
        return int(len(self.alphas))

    def tridiagonal(self) -> np.ndarray:
        return tridiagonal_matrix(self.alphas, self.betas)


def lanczos(
    matvec: Matvec,
    initial_vector: np.ndarray,
    max_steps: int,
    breakdown_tolerance: float = 1e-13,
    reorthogonalization_passes: int = 2,
) -> LanczosResult:
    """Run Hermitian Lanczos with full reorthogonalization.

    ``betas[k]`` couples Lanczos vectors ``k`` and ``k+1``.  Consequently an
    M-dimensional tridiagonal matrix contains M diagonal ``alphas`` and M-1
    internal ``betas``.  ``terminal_beta`` is the coefficient of the next,
    not-yet-included vector and is retained for recurrence checks.
    """

    if max_steps < 1:
        raise ValueError("max_steps must be at least one")
    if reorthogonalization_passes < 0:
        raise ValueError("reorthogonalization_passes cannot be negative")

    start = np.asarray(initial_vector)
    if start.ndim != 1:
        raise ValueError("initial_vector must be one-dimensional")
    initial_norm = float(np.linalg.norm(start))
    if initial_norm == 0.0:
        raise ValueError("initial_vector must be nonzero")

    q = start.astype(np.result_type(start.dtype, np.float64), copy=True) / initial_norm
    q_vectors: list[np.ndarray] = [q.copy()]
    alphas: list[float] = []
    betas: list[float] = []
    previous_q = np.zeros_like(q)
    terminal_beta = 0.0
    terminal_vector: np.ndarray | None = None

    for step in range(max_steps):
        residual = np.asarray(matvec(q), dtype=q.dtype)
        if residual.shape != q.shape:
            raise ValueError("matvec returned a vector with the wrong shape")
        if step > 0:
            residual = residual - betas[-1] * previous_q

        alpha_complex = np.vdot(q, residual)
        if abs(alpha_complex.imag) > 100 * np.finfo(float).eps * max(1.0, abs(alpha_complex.real)):
            raise ValueError("Lanczos alpha is not real; the operator may be non-Hermitian")
        alpha = float(alpha_complex.real)
        residual = residual - alpha * q

        for _ in range(reorthogonalization_passes):
            for basis_vector in q_vectors:
                residual = residual - np.vdot(basis_vector, residual) * basis_vector

        beta_next = float(np.linalg.norm(residual))
        alphas.append(alpha)
        is_last_requested_step = step + 1 == max_steps
        if beta_next <= breakdown_tolerance or is_last_requested_step:
            terminal_beta = beta_next
            if beta_next > breakdown_tolerance:
                terminal_vector = residual / beta_next
            break

        betas.append(beta_next)
        next_q = residual / beta_next
        previous_q, q = q, next_q
        q_vectors.append(q.copy())

    vectors = np.column_stack(q_vectors)
    return LanczosResult(
        alphas=np.asarray(alphas, dtype=float),
        betas=np.asarray(betas, dtype=float),
        vectors=vectors,
        initial_norm=initial_norm,
        terminal_beta=terminal_beta,
        terminal_vector=terminal_vector,
    )


def tridiagonal_matrix(alphas: np.ndarray, betas: np.ndarray) -> np.ndarray:
    """Build the real symmetric Lanczos tridiagonal matrix."""

    diagonal = np.asarray(alphas, dtype=float)
    off_diagonal = np.asarray(betas, dtype=float)
    if off_diagonal.shape != (max(0, len(diagonal) - 1),):
        raise ValueError("an M-dimensional T requires exactly M-1 beta values")
    matrix = np.diag(diagonal)
    if len(diagonal) > 1:
        matrix += np.diag(off_diagonal, 1) + np.diag(off_diagonal, -1)
    return matrix


def continued_fraction(
    z: complex | np.ndarray,
    alphas: np.ndarray,
    betas: np.ndarray,
    weight: float = 1.0,
) -> complex | np.ndarray:
    """Evaluate ``weight * [(z-T)^-1]_{00}`` by backward recursion."""

    diagonal = np.asarray(alphas, dtype=float)
    off_diagonal = np.asarray(betas, dtype=float)
    if diagonal.ndim != 1 or diagonal.size == 0:
        raise ValueError("at least one alpha is required")
    if off_diagonal.shape != (len(diagonal) - 1,):
        raise ValueError("betas must have length len(alphas)-1")

    frequency = np.asarray(z, dtype=complex)
    fraction = np.zeros_like(frequency, dtype=complex)
    for index in range(len(diagonal) - 1, -1, -1):
        coupling = 0.0 if index == len(diagonal) - 1 else off_diagonal[index] ** 2 * fraction
        fraction = 1.0 / (frequency - diagonal[index] - coupling)
    result = weight * fraction
    return complex(result) if result.ndim == 0 else result


def direct_resolvent_element(
    matrix: np.ndarray | sparse.spmatrix,
    vector: np.ndarray,
    z: complex,
) -> complex:
    """Directly compute ``<v|(z-H)^-1|v>`` for validation only."""

    state = np.asarray(vector, dtype=complex)
    dimension = state.size
    if sparse.issparse(matrix):
        shifted = z * sparse.identity(dimension, format="csr") - matrix
        solution = spsolve(shifted, state)
    else:
        dense = np.asarray(matrix)
        solution = np.linalg.solve(z * np.eye(dimension) - dense, state)
    return complex(np.vdot(state, solution))


def _apply_to_columns(matvec: Matvec, vectors: np.ndarray) -> np.ndarray:
    return np.column_stack([matvec(vectors[:, column]) for column in range(vectors.shape[1])])


def lanczos_relation_residuals(
    matvec: Matvec,
    result: LanczosResult,
) -> tuple[float, float, float]:
    """Return orthogonality, completed-column, and full-recurrence residuals."""

    q_matrix = result.vectors
    identity = np.eye(result.n_steps)
    orthogonality = float(np.linalg.norm(q_matrix.conj().T @ q_matrix - identity))
    t_matrix = result.tridiagonal()
    hq = _apply_to_columns(matvec, q_matrix)

    if result.n_steps > 1:
        completed_difference = hq[:, :-1] - q_matrix @ t_matrix[:, :-1]
        completed = float(np.linalg.norm(completed_difference))
    else:
        completed = 0.0

    full_difference = hq - q_matrix @ t_matrix
    if result.terminal_vector is not None:
        full_difference[:, -1] -= result.terminal_beta * result.terminal_vector
    full = float(np.linalg.norm(full_difference))
    return orthogonality, completed, full


def lowest_ritz_history(alphas: np.ndarray, betas: np.ndarray) -> np.ndarray:
    """Return the lowest Ritz value of every leading Krylov subspace."""

    diagonal = np.asarray(alphas, dtype=float)
    off_diagonal = np.asarray(betas, dtype=float)
    if off_diagonal.shape != (max(0, len(diagonal) - 1),):
        raise ValueError("betas must have length len(alphas)-1")
    history = []
    for size in range(1, len(diagonal) + 1):
        leading = tridiagonal_matrix(diagonal[:size], off_diagonal[: size - 1])
        history.append(float(np.linalg.eigvalsh(leading)[0]))
    return np.asarray(history)

