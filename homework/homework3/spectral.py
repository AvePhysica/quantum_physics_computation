"""Particle-addition/removal spectra for the Hubbard ring."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from hubbard_basis import BlockBasis, Spin, apply_fermion_to_state
from hubbard_operator import HubbardHamiltonian, lowest_eigenpairs
from lanczos import continued_fraction, lanczos


@dataclass(frozen=True)
class DOSResult:
    omega_shifted: np.ndarray
    chemical_potential: float
    addition: np.ndarray
    removal: np.ndarray
    total: np.ndarray
    addition_weight: float
    removal_weight: float
    channel_weights: dict[str, float]
    adjacent_ground_energies: dict[str, float]


def target_particle_numbers(
    source_basis: BlockBasis,
    spin: Spin,
    dagger: bool,
) -> tuple[int, int]:
    """Return the symmetry block reached by one local fermion operator."""

    delta = 1 if dagger else -1
    if spin == "up":
        target = source_basis.n_up + delta, source_basis.n_down
    elif spin == "down":
        target = source_basis.n_up, source_basis.n_down + delta
    else:
        raise ValueError("spin must be 'up' or 'down'")
    if not all(0 <= count <= source_basis.n_sites for count in target):
        raise ValueError("fermion operation leaves the physical Hilbert space")
    return target


def apply_local_operator(
    source_basis: BlockBasis,
    target_basis: BlockBasis,
    vector: np.ndarray,
    site: int,
    spin: Spin,
    dagger: bool,
) -> np.ndarray:
    """Apply ``c_site,spin`` or its adjoint between explicit blocks."""

    expected_counts = target_particle_numbers(source_basis, spin, dagger)
    if (
        target_basis.n_sites != source_basis.n_sites
        or (target_basis.n_up, target_basis.n_down) != expected_counts
    ):
        raise ValueError("target_basis does not match the fermion operation")
    state = np.asarray(vector)
    if state.ndim != 1 or state.size != source_basis.dimension:
        raise ValueError("source vector has the wrong shape")

    output = np.zeros(target_basis.dimension, dtype=np.result_type(state.dtype, float))
    for source_index, up_mask, down_mask in source_basis.iter_states():
        amplitude = state[source_index]
        if amplitude == 0:
            continue
        transformed = apply_fermion_to_state(
            up_mask,
            down_mask,
            source_basis.n_sites,
            site,
            spin,
            dagger,
        )
        if transformed is None:
            continue
        new_up, new_down, sign = transformed
        output[target_basis.index(new_up, new_down)] += sign * amplitude
    return output


def local_add_remove_weights(
    source_basis: BlockBasis,
    normalized_state: np.ndarray,
) -> tuple[float, float, dict[str, float]]:
    """Return separately summed addition and removal zeroth moments."""

    state = np.asarray(normalized_state)
    norm = float(np.vdot(state, state).real)
    if not np.isclose(norm, 1.0, atol=1e-10):
        raise ValueError("state must be normalized")

    total_addition = 0.0
    total_removal = 0.0
    details: dict[str, float] = {}
    for dagger, label in ((True, "add"), (False, "rem")):
        for spin in ("up", "down"):
            n_up, n_down = target_particle_numbers(source_basis, spin, dagger)
            target_basis = BlockBasis(source_basis.n_sites, n_up, n_down)
            for site in range(source_basis.n_sites):
                transformed = apply_local_operator(
                    source_basis,
                    target_basis,
                    state,
                    site,
                    spin,
                    dagger,
                )
                weight = float(np.vdot(transformed, transformed).real)
                details[f"{label}_{spin}_{site}"] = weight
                if dagger:
                    total_addition += weight
                else:
                    total_removal += weight
    return total_addition, total_removal, details


def _deterministic_start(dimension: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return rng.normal(size=dimension)


def adjacent_sector_ground_energies(
    source_basis: BlockBasis,
    hopping: float,
    interaction: float,
    eigensolver_tolerance: float = 1e-12,
    seed: int = 20260928,
) -> dict[str, float]:
    """Compute the lowest energies in all four N+1/N-1 target blocks."""

    energies: dict[str, float] = {}
    for dagger, label in ((True, "add"), (False, "rem")):
        for spin_index, spin in enumerate(("up", "down")):
            n_up, n_down = target_particle_numbers(source_basis, spin, dagger)
            target_basis = BlockBasis(source_basis.n_sites, n_up, n_down)
            hamiltonian = HubbardHamiltonian(target_basis, hopping, interaction)
            values, _ = lowest_eigenpairs(
                hamiltonian,
                n_eigenpairs=2,
                tolerance=eigensolver_tolerance,
                initial_vector=_deterministic_start(
                    target_basis.dimension,
                    seed + 100 * int(dagger) + spin_index,
                ),
            )
            energies[f"{label}_{spin}"] = float(values[0])
    return energies


def chemical_potential_from_adjacent_energies(energies: dict[str, float]) -> float:
    """Return 1/2 [E0(N+1)-E0(N-1)] from all spin sectors."""

    addition_ground = min(energies["add_up"], energies["add_down"])
    removal_ground = min(energies["rem_up"], energies["rem_down"])
    return 0.5 * (addition_ground - removal_ground)


def particle_hole_channel_relative_error(
    addition: np.ndarray,
    removal: np.ndarray,
) -> float:
    """Return the pointwise error in rho_add(xi) = rho_rem(-xi)."""

    addition_array = np.asarray(addition, dtype=float)
    removal_array = np.asarray(removal, dtype=float)
    if addition_array.ndim != 1 or addition_array.shape != removal_array.shape:
        raise ValueError("addition and removal must be one-dimensional arrays of equal size")
    if addition_array.size == 0:
        raise ValueError("addition and removal spectra cannot be empty")
    scale = max(
        float(np.max(np.abs(addition_array))),
        float(np.max(np.abs(removal_array))),
        np.finfo(float).tiny,
    )
    return float(np.max(np.abs(addition_array - removal_array[::-1])) / scale)


def total_density_of_states(
    source_basis: BlockBasis,
    ground_energy: float,
    ground_state: np.ndarray,
    hopping: float,
    interaction: float,
    eta: float,
    omega_shifted: np.ndarray,
    max_lanczos_steps: int,
    eigensolver_tolerance: float = 1e-12,
    seed: int = 20260928,
    reorthogonalization_passes: int = 0,
) -> DOSResult:
    """Sum all local addition/removal spectra using Lanczos fractions."""

    if eta <= 0:
        raise ValueError("eta must be positive")
    state = np.asarray(ground_state)
    if not np.isclose(np.vdot(state, state).real, 1.0, atol=1e-9):
        raise ValueError("ground_state must be normalized")
    shifted = np.asarray(omega_shifted, dtype=float)
    adjacent_energies = adjacent_sector_ground_energies(
        source_basis,
        hopping,
        interaction,
        eigensolver_tolerance=eigensolver_tolerance,
        seed=seed,
    )
    mu = chemical_potential_from_adjacent_energies(adjacent_energies)
    omega = shifted + mu
    addition = np.zeros_like(shifted)
    removal = np.zeros_like(shifted)
    channel_weights: dict[str, float] = {}
    hamiltonian_cache: dict[tuple[int, int], HubbardHamiltonian] = {}

    for dagger, label in ((True, "add"), (False, "rem")):
        for spin in ("up", "down"):
            counts = target_particle_numbers(source_basis, spin, dagger)
            target_basis = BlockBasis(source_basis.n_sites, *counts)
            if counts not in hamiltonian_cache:
                hamiltonian_cache[counts] = HubbardHamiltonian(
                    target_basis, hopping, interaction
                )
            target_hamiltonian = hamiltonian_cache[counts]

            for site in range(source_basis.n_sites):
                initial = apply_local_operator(
                    source_basis,
                    target_basis,
                    state,
                    site,
                    spin,
                    dagger,
                )
                weight = float(np.vdot(initial, initial).real)
                channel_weights[f"{label}_{spin}_{site}"] = weight
                if weight <= 1e-15:
                    continue
                chain = lanczos(
                    target_hamiltonian.matvec,
                    initial,
                    min(max_lanczos_steps, target_basis.dimension),
                    reorthogonalization_passes=reorthogonalization_passes,
                )
                if dagger:
                    z = omega + 1j * eta + ground_energy
                else:
                    z = -omega + 1j * eta + ground_energy
                green = continued_fraction(
                    z,
                    chain.alphas,
                    chain.betas,
                    weight=chain.initial_norm**2,
                )
                contribution = -np.imag(green) / np.pi
                if dagger:
                    addition += contribution
                else:
                    removal += contribution

    addition_weight = sum(
        weight for name, weight in channel_weights.items() if name.startswith("add_")
    )
    removal_weight = sum(
        weight for name, weight in channel_weights.items() if name.startswith("rem_")
    )
    return DOSResult(
        omega_shifted=shifted,
        chemical_potential=mu,
        addition=addition,
        removal=removal,
        total=addition + removal,
        addition_weight=float(addition_weight),
        removal_weight=float(removal_weight),
        channel_weights=channel_weights,
        adjacent_ground_energies=adjacent_energies,
    )


def free_fermion_dos(
    omega_shifted: np.ndarray,
    n_sites: int,
    hopping: float,
    eta: float,
) -> np.ndarray:
    """Exact spin-summed broadened DOS of the U=0 periodic ring."""

    omega = np.asarray(omega_shifted, dtype=float)
    momenta = np.arange(n_sites)
    energies = -2.0 * hopping * np.cos(2.0 * np.pi * momenta / n_sites)
    differences = omega[:, None] - energies[None, :]
    return 2.0 * np.sum(eta / (np.pi * (differences**2 + eta**2)), axis=1)


def spectral_moments(
    matvec,
    initial_vector: np.ndarray,
) -> tuple[float, float]:
    """Return exact zeroth and first absolute-energy moments of one channel."""

    vector = np.asarray(initial_vector)
    zeroth = float(np.vdot(vector, vector).real)
    first = float(np.vdot(vector, matvec(vector)).real)
    return zeroth, first

