"""固定粒子数基态上的 Hubbard 模型观测量。"""

import numpy as np

from hubbard_model import COORDINATES, L, SectorBasis, apply_fermion_operations


def _probabilities(state: np.ndarray) -> np.ndarray:
    norm = np.vdot(state, state).real
    if not np.isclose(norm, 1.0, atol=1e-10):
        raise ValueError(f"态矢量未归一化：范数为 {norm}")
    return np.abs(state) ** 2


def _occupation_arrays(basis: SectorBasis) -> tuple[np.ndarray, np.ndarray]:
    up = np.array(
        [[(up_bits >> site) & 1 for site in range(L)] for up_bits, _ in basis.states],
        dtype=float,
    )
    down = np.array(
        [[(down_bits >> site) & 1 for site in range(L)] for _, down_bits in basis.states],
        dtype=float,
    )
    return up, down


def local_densities(state: np.ndarray, basis: SectorBasis) -> np.ndarray:
    up, down = _occupation_arrays(basis)
    return _probabilities(state) @ (up + down)


def local_spin_z(state: np.ndarray, basis: SectorBasis) -> np.ndarray:
    up, down = _occupation_arrays(basis)
    return _probabilities(state) @ ((up - down) / 2)


def double_occupancies(state: np.ndarray, basis: SectorBasis) -> np.ndarray:
    up, down = _occupation_arrays(basis)
    return _probabilities(state) @ (up * down)


def density_correlation_matrix(state: np.ndarray, basis: SectorBasis) -> np.ndarray:
    up, down = _occupation_arrays(basis)
    density = up + down
    probabilities = _probabilities(state)
    return np.einsum("a,ai,aj->ij", probabilities, density, density)


def _spin_flip_expectation(
    state: np.ndarray, basis: SectorBasis, i: int, j: int
) -> complex:
    """返回 <S_i^+ S_j^->；四个费米算符按从右到左的顺序作用。"""
    operations = (
        ("annihilate", j),
        ("create", j + L),
        ("annihilate", i + L),
        ("create", i),
    )
    value = 0j
    for column, occupation in enumerate(basis.states):
        result = apply_fermion_operations(occupation, operations)
        if result is None:
            continue
        new_occupation, sign = result
        row = basis.index[new_occupation]
        value += np.conjugate(state[row]) * sign * state[column]
    return value


def spin_correlation_matrix(state: np.ndarray, basis: SectorBasis) -> np.ndarray:
    """返回所有 i,j 的 <S_i dot S_j>。"""
    up, down = _occupation_arrays(basis)
    probabilities = _probabilities(state)
    spin_z_configurations = (up - down) / 2
    correlations = np.einsum(
        "a,ai,aj->ij", probabilities, spin_z_configurations, spin_z_configurations
    ).astype(complex)

    doubles = probabilities @ (up * down)
    densities = probabilities @ (up + down)
    np.fill_diagonal(correlations, 0.75 * (densities - 2 * doubles))

    for i in range(L):
        for j in range(i + 1, L):
            transverse = 0.5 * (
                _spin_flip_expectation(state, basis, i, j)
                + _spin_flip_expectation(state, basis, j, i)
            )
            correlations[i, j] += transverse
            correlations[j, i] = np.conjugate(correlations[i, j])
    return np.real_if_close(correlations)


def total_spin_squared(state: np.ndarray, basis: SectorBasis) -> float:
    return float(np.real_if_close(np.sum(spin_correlation_matrix(state, basis))))


def structure_factors(
    correlation_matrix: np.ndarray,
) -> dict[tuple[int, int], float]:
    """在 q=(2*pi*n_x/3, q_y), q_y=0/pi 上作离散傅里叶变换。"""
    factors: dict[tuple[int, int], float] = {}
    for n_x in range(3):
        for y_index, q_y in enumerate((0.0, np.pi)):
            q = np.array((2 * np.pi * n_x / 3, q_y))
            phase = np.exp(
                1j
                * np.einsum(
                    "k,ijk->ij", q, COORDINATES[:, None, :] - COORDINATES[None, :, :]
                )
            )
            value = np.sum(phase * correlation_matrix) / L
            factors[(n_x, y_index)] = float(np.real_if_close(value))
    return factors
