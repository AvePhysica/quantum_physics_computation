"""Local observables, correlations, and magnetization envelope helpers."""

from __future__ import annotations

import numpy as np

from j1j2_basis import basis_index


def local_spin_expectations(
    state_vector: np.ndarray, basis: np.ndarray, n_sites: int
) -> tuple[np.ndarray, np.ndarray]:
    probabilities = np.abs(state_vector) ** 2
    sz = np.zeros(n_sites, dtype=float)
    sx = np.zeros(n_sites, dtype=float)
    lookup = basis_index(basis)
    for column, raw_state in enumerate(basis):
        state = int(raw_state)
        for site in range(n_sites):
            sz[site] += probabilities[column] * (0.5 if (state >> site) & 1 else -0.5)
            flipped = state ^ (1 << site)
            row = lookup.get(flipped)
            if row is not None:
                sx[site] += 0.5 * np.real(np.conjugate(state_vector[row]) * state_vector[column])
    return sz, sx


def spin_correlations(state_vector: np.ndarray, basis: np.ndarray, n_sites: int) -> np.ndarray:
    """Return C(r)=<S_0 dot S_r> for r=0,...,N-1."""
    correlations = np.zeros(n_sites, dtype=float)
    correlations[0] = 0.75
    lookup = basis_index(basis)
    for r in range(1, n_sites):
        value = 0.0 + 0.0j
        for column, raw_state in enumerate(basis):
            bit_state = int(raw_state)
            spin0 = 0.5 if bit_state & 1 else -0.5
            spinr = 0.5 if (bit_state >> r) & 1 else -0.5
            value += np.abs(state_vector[column]) ** 2 * spin0 * spinr
            if spin0 != spinr:
                flipped = bit_state ^ 1 ^ (1 << r)
                row = lookup[flipped]
                value += 0.5 * np.conjugate(state_vector[row]) * state_vector[column]
        correlations[r] = float(np.real(value))
    return correlations


def longitudinal_correlations(
    state_vector: np.ndarray, basis: np.ndarray, n_sites: int
) -> np.ndarray:
    """Return Czz(r)=<S^z_0 S^z_r>."""
    probabilities = np.abs(state_vector) ** 2
    correlations = np.zeros(n_sites, dtype=float)
    for r in range(n_sites):
        value = 0.0
        for probability, raw_state in zip(probabilities, basis):
            bit_state = int(raw_state)
            spin0 = 0.5 if bit_state & 1 else -0.5
            spinr = 0.5 if (bit_state >> r) & 1 else -0.5
            value += probability * spin0 * spinr
        correlations[r] = value
    return correlations


def structure_factor(correlations: np.ndarray) -> np.ndarray:
    """Return S(q)=N^{-1} sum_r exp(-iqr) C(r)."""
    return np.real(np.fft.fft(correlations)) / len(correlations)


def magnetization_envelope(
    sector_energies: dict[float, float], fields: np.ndarray, n_sites: int
) -> tuple[np.ndarray, np.ndarray]:
    magnetizations = np.asarray(sorted(sector_energies), dtype=float)
    bare = np.asarray([sector_energies[m] for m in magnetizations], dtype=float)
    tilted = bare[:, None] - magnetizations[:, None] * fields[None, :]
    winners = np.argmin(tilted, axis=0)
    return magnetizations[winners] / n_sites, tilted[winners, np.arange(len(fields))]


def adjacent_critical_fields(sector_energies: dict[float, float]) -> list[tuple[float, float, float]]:
    magnetizations = sorted(sector_energies)
    crossings = []
    for left, right in zip(magnetizations[:-1], magnetizations[1:]):
        field = (sector_energies[right] - sector_energies[left]) / (right - left)
        crossings.append((left, right, float(field)))
    return crossings


def lower_envelope_transitions(
    sector_energies: dict[float, float], *, nonnegative_only: bool = True
) -> tuple[list[tuple[float, float]], list[tuple[float, float, float]]]:
    """Build the lower convex hull of E(M) and its exact field crossings."""
    points = sorted(
        (float(m), float(e))
        for m, e in sector_energies.items()
        if not nonnegative_only or m >= 0.0
    )
    hull: list[tuple[float, float]] = []
    for point in points:
        while len(hull) >= 2:
            slope_old = (hull[-1][1] - hull[-2][1]) / (hull[-1][0] - hull[-2][0])
            slope_new = (point[1] - hull[-1][1]) / (point[0] - hull[-1][0])
            if slope_old < slope_new - 1e-13:
                break
            hull.pop()
        hull.append(point)
    transitions = []
    for left, right in zip(hull[:-1], hull[1:]):
        field = (right[1] - left[1]) / (right[0] - left[0])
        transitions.append((left[0], right[0], float(field)))
    return hull, transitions

