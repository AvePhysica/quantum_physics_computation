"""Analytic and exact-state benchmarks for the J1-J2 chain."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from j1j2_basis import basis_index


@dataclass(frozen=True)
class FreeFermionResult:
    energy: float
    boundary: str
    periodic_energy: float
    antiperiodic_energy: float


def free_fermion_half_filled_energy(n_sites: int, j1: float = 1.0) -> FreeFermionResult:
    """XX ground energy, explicitly testing both Jordan-Wigner boundary grids."""
    n_particles = n_sites // 2
    periodic_k = 2.0 * np.pi * np.arange(n_sites) / n_sites
    antiperiodic_k = 2.0 * np.pi * (np.arange(n_sites) + 0.5) / n_sites
    periodic_energy = float(np.sort(j1 * np.cos(periodic_k))[:n_particles].sum())
    antiperiodic_energy = float(np.sort(j1 * np.cos(antiperiodic_k))[:n_particles].sum())
    if periodic_energy <= antiperiodic_energy:
        return FreeFermionResult(periodic_energy, "periodic", periodic_energy, antiperiodic_energy)
    return FreeFermionResult(antiperiodic_energy, "antiperiodic", periodic_energy, antiperiodic_energy)


def dimer_product_state(n_sites: int, basis: np.ndarray, shift: int = 0) -> np.ndarray:
    """Product of oriented spin singlets (a,b): (up,down)-(down,up)."""
    if n_sites % 2:
        raise ValueError("A dimer covering requires an even number of sites")
    amplitudes: dict[int, complex] = {0: 1.0 + 0.0j}
    for pair in range(n_sites // 2):
        a = (shift + 2 * pair) % n_sites
        b = (shift + 2 * pair + 1) % n_sites
        updated: dict[int, complex] = {}
        for state, amplitude in amplitudes.items():
            updated[state | (1 << a)] = amplitude / np.sqrt(2.0)
            updated[state | (1 << b)] = -amplitude / np.sqrt(2.0)
        amplitudes = updated
    lookup = basis_index(basis)
    vector = np.zeros(len(basis), dtype=complex)
    for state, amplitude in amplitudes.items():
        vector[lookup[state]] = amplitude
    return vector


def normalized_dimer_momenta(d0: np.ndarray, d1: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    plus_raw = d0 + d1
    minus_raw = d0 - d1
    return plus_raw / np.linalg.norm(plus_raw), minus_raw / np.linalg.norm(minus_raw)

