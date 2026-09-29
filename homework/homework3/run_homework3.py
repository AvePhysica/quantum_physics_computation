"""Generate every numerical table and figure required by Homework 3.

This file is the single reproducible entry point.  It intentionally contains
no precomputed numerical answers: all values are generated from the source
code when the script is run.
"""

from __future__ import annotations

import csv
import json
import platform
import sys
from dataclasses import asdict, dataclass
from math import comb
from pathlib import Path
from typing import Any

import numpy as np
import matplotlib
import scipy

from hubbard_basis import BlockBasis
from hubbard_operator import (
    HubbardHamiltonian,
    build_sparse_hamiltonian_independent,
    expected_interaction_trace,
    ground_state_degeneracy,
    lowest_eigenpairs,
)
from lanczos import (
    continued_fraction,
    direct_resolvent_element,
    lanczos,
    lanczos_relation_residuals,
    lowest_ritz_history,
)
from plots import (
    plot_hubbard_band_schematic,
    plot_rho_zero_ratio,
    plot_ritz_convergence,
    plot_stacked_dos,
    plot_u0_benchmark,
)
from spectral import (
    DOSResult,
    apply_local_operator,
    free_fermion_dos,
    local_add_remove_weights,
    particle_hole_channel_relative_error,
    target_particle_numbers,
    total_density_of_states,
)


@dataclass(frozen=True)
class Configuration:
    n_sites: int = 8
    n_up: int = 4
    n_down: int = 4
    hopping: float = 1.0
    main_interaction: float = 4.0
    eta: float = 0.11
    random_seed: int = 20260928
    eigensolver_tolerance: float = 1e-11
    degeneracy_tolerance: float = 1e-8
    continued_fraction_lanczos_steps: int = 480
    spectral_lanczos_steps: int = 240
    spectral_reference_lanczos_steps: int = 480
    omega_min: float = -10.0
    omega_max: float = 10.0
    omega_points: int = 2001


def _json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_ready(item) for item in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, complex):
        return {"real": value.real, "imag": value.imag}
    return value


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(_json_ready(payload), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _relative_norm(vector: np.ndarray, reference: np.ndarray) -> float:
    denominator = max(float(np.linalg.norm(reference)), np.finfo(float).tiny)
    return float(np.linalg.norm(vector) / denominator)


def _ground_state(
    n_sites: int,
    n_up: int,
    n_down: int,
    hopping: float,
    interaction: float,
    seed: int,
    tolerance: float,
    n_eigenpairs: int,
) -> tuple[BlockBasis, HubbardHamiltonian, np.ndarray, np.ndarray]:
    basis = BlockBasis(n_sites, n_up, n_down)
    hamiltonian = HubbardHamiltonian(basis, hopping, interaction)
    start = np.random.default_rng(seed).normal(size=basis.dimension)
    eigenvalues, eigenvectors = lowest_eigenpairs(
        hamiltonian,
        n_eigenpairs=n_eigenpairs,
        tolerance=tolerance,
        initial_vector=start,
    )
    return basis, hamiltonian, eigenvalues, eigenvectors


def _add_validation(
    records: list[dict[str, Any]],
    name: str,
    target_error: str,
    expectation: str,
    measured: Any,
    passed: bool,
    failure_mode: str,
) -> None:
    records.append(
        {
            "check": name,
            "target_error": target_error,
            "expectation": expectation,
            "measured": measured,
            "conclusion": "PASS" if passed else "FAIL",
            "failure_mode": failure_mode,
        }
    )


def _one_site_times_n_weights(
    basis: BlockBasis,
    state: np.ndarray,
    site: int = 0,
) -> tuple[float, float]:
    addition = 0.0
    removal = 0.0
    for dagger in (True, False):
        for spin in ("up", "down"):
            counts = target_particle_numbers(basis, spin, dagger)
            target_basis = BlockBasis(basis.n_sites, *counts)
            transformed = apply_local_operator(
                basis, target_basis, state, site, spin, dagger
            )
            weight = float(np.vdot(transformed, transformed).real) * basis.n_sites
            if dagger:
                addition += weight
            else:
                removal += weight
    return addition, removal


def _degeneracy_weight_summary(
    full_addition: float,
    full_removal: float,
    shortcut_addition: float,
    shortcut_removal: float,
) -> dict[str, float]:
    """Keep the basis-dependent raw pair together with its deviation magnitude."""

    return {
        "full_addition_weight": full_addition,
        "shortcut_addition_weight": shortcut_addition,
        "full_removal_weight": full_removal,
        "shortcut_removal_weight": shortcut_removal,
        "shortcut_max_deviation_from_exact_pair": max(
            abs(shortcut_addition - full_addition),
            abs(shortcut_removal - full_removal),
        ),
    }


def _closed_shell_gap(n_sites: int, particles_per_spin: int, hopping: float) -> float:
    momenta = np.arange(n_sites)
    energies = np.sort(-2.0 * hopping * np.cos(2.0 * np.pi * momenta / n_sites))
    return float(energies[particles_per_spin] - energies[particles_per_spin - 1])


def _select_extremal_local_density_ground_state(
    basis: BlockBasis,
    eigenvalues: np.ndarray,
    eigenvectors: np.ndarray,
    tolerance: float,
    site: int = 0,
) -> np.ndarray:
    """Choose a deterministic symmetry-broken vector inside a degenerate ground space.

    The projected local-density operator is diagonalized inside the numerically
    obtained ground manifold.  A unique ground state is returned unchanged.
    """

    ground_mask = np.abs(eigenvalues - eigenvalues[0]) <= tolerance
    subspace = eigenvectors[:, ground_mask]
    if subspace.shape[1] == 1:
        return subspace[:, 0]
    local_density = np.empty(basis.dimension, dtype=float)
    for index, up_mask, down_mask in basis.iter_states():
        local_density[index] = ((up_mask >> site) & 1) + ((down_mask >> site) & 1)
    projected_density = subspace.conj().T @ (local_density[:, None] * subspace)
    _, projected_vectors = np.linalg.eigh(projected_density)
    state = subspace @ projected_vectors[:, -1]
    return state / np.linalg.norm(state)


def _save_dos_csv(path: Path, result: DOSResult) -> None:
    array = np.column_stack(
        [result.omega_shifted, result.addition, result.removal, result.total]
    )
    np.savetxt(
        path,
        array,
        delimiter=",",
        header="omega_minus_mu,rho_add,rho_rem,rho_total",
        comments="",
    )


def main() -> None:
    config = Configuration()
    project_dir = Path(__file__).resolve().parent
    output_dir = project_dir / "output"
    data_dir = output_dir / "data"
    figure_dir = output_dir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figure_dir.mkdir(parents=True, exist_ok=True)
    _write_json(data_dir / "configuration.json", asdict(config))

    validations: list[dict[str, Any]] = []
    results: dict[str, Any] = {
        "configuration": asdict(config),
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "matplotlib": matplotlib.__version__,
        },
    }
    rng = np.random.default_rng(config.random_seed)

    # ------------------------------------------------------------------
    # 1. Main U(1) x U(1) block, matrix-free action, and ground state.
    # ------------------------------------------------------------------
    basis, hamiltonian, eigenvalues, eigenvectors = _ground_state(
        config.n_sites,
        config.n_up,
        config.n_down,
        config.hopping,
        config.main_interaction,
        config.random_seed,
        config.eigensolver_tolerance,
        n_eigenpairs=10,
    )
    sparse_hamiltonian = build_sparse_hamiltonian_independent(
        basis, config.hopping, config.main_interaction
    )
    ground_energy = float(eigenvalues[0])
    ground_state = eigenvectors[:, 0]
    degeneracy = ground_state_degeneracy(
        eigenvalues, config.degeneracy_tolerance
    )
    expected_dimension = int(
        comb(config.n_sites, config.n_up)
        * comb(config.n_sites, config.n_down)
    )

    probe = rng.normal(size=basis.dimension) + 1j * rng.normal(size=basis.dimension)
    matrix_free_action = hamiltonian.matvec(probe)
    sparse_action = sparse_hamiltonian @ probe
    matvec_relative_error = _relative_norm(
        matrix_free_action - sparse_action, sparse_action
    )
    hermitian_difference = sparse_hamiltonian - sparse_hamiltonian.getH()
    hermitian_residual = float(np.linalg.norm(hermitian_difference.data))
    measured_trace = float(np.real(sparse_hamiltonian.diagonal().sum()))
    expected_trace = expected_interaction_trace(basis, config.main_interaction)
    ground_residual = _relative_norm(
        sparse_hamiltonian @ ground_state - ground_energy * ground_state,
        ground_state,
    )

    explicit_values, _ = lowest_eigenpairs(
        sparse_hamiltonian,
        n_eigenpairs=10,
        tolerance=config.eigensolver_tolerance,
        initial_vector=rng.normal(size=basis.dimension),
    )
    explicit_ground_difference = abs(float(explicit_values[0]) - ground_energy)
    results["main_block"] = {
        "counts": [config.n_up, config.n_down],
        "dimension_formula": expected_dimension,
        "dimension_enumerated": basis.dimension,
        "ground_energy": ground_energy,
        "ground_degeneracy": degeneracy,
        "lowest_eigenvalues": eigenvalues,
        "ground_residual": ground_residual,
        "matrix_free_sparse_relative_error": matvec_relative_error,
        "hermiticity_residual": hermitian_residual,
        "interaction_trace_expected": expected_trace,
        "interaction_trace_measured": measured_trace,
        "explicit_sparse_ground_difference": explicit_ground_difference,
    }

    _add_validation(
        validations,
        "block_dimension",
        "missing or duplicated fixed-particle-number basis states",
        f"enumerated dimension equals combinatorial value {expected_dimension}",
        basis.dimension,
        basis.dimension == expected_dimension,
        "the two dimensions differ",
    )
    _add_validation(
        validations,
        "matrix_free_vs_independent_sparse",
        "hopping sign, target index, boundary bond, or interaction-action error",
        "relative action error < 1e-12",
        matvec_relative_error,
        matvec_relative_error < 1e-12,
        "a random complex probe produces different output vectors",
    )
    _add_validation(
        validations,
        "hermiticity",
        "missing reverse hop or asymmetric fermionic sign",
        "||H-H^dagger|| < 1e-12",
        hermitian_residual,
        hermitian_residual < 1e-12,
        "the antisymmetric matrix norm becomes nonzero",
    )
    _add_validation(
        validations,
        "interaction_trace",
        "missing or incorrectly weighted U term",
        f"Tr(H) = {expected_trace}",
        measured_trace,
        np.isclose(measured_trace, expected_trace, atol=1e-12),
        "the diagonal trace no longer matches the combinatorial count",
    )
    _add_validation(
        validations,
        "ground_state_residual",
        "unconverged eigensolver or mismatch between Hamiltonian representations",
        "relative residual < 1e-9",
        ground_residual,
        ground_residual < 1e-9,
        "||H psi-E psi|| remains appreciable",
    )
    _add_validation(
        validations,
        "ground_energy_cross_representation",
        "matrix-free Hamiltonian differs from explicit sparse Hamiltonian",
        "absolute energy difference < 1e-9",
        explicit_ground_difference,
        explicit_ground_difference < 1e-9,
        "the independently solved ground energies disagree",
    )

    # Deliberate mutations required by the assignment's self-check rule.
    wrong_hopping = build_sparse_hamiltonian_independent(
        basis, -config.hopping, config.main_interaction
    )
    open_bonds = [(site, site + 1) for site in range(config.n_sites - 1)]
    missing_boundary = build_sparse_hamiltonian_independent(
        basis, config.hopping, config.main_interaction, bonds=open_bonds
    )
    missing_interaction = build_sparse_hamiltonian_independent(
        basis, config.hopping, 0.0
    )
    mutation_measurements = {
        "flipped_hopping_sign_action_difference": _relative_norm(
            wrong_hopping @ probe - matrix_free_action, matrix_free_action
        ),
        "missing_boundary_action_difference": _relative_norm(
            missing_boundary @ probe - matrix_free_action, matrix_free_action
        ),
        "removed_interaction_trace_difference": abs(
            float(missing_interaction.diagonal().sum()) - expected_trace
        ),
    }
    results["deliberate_mutations"] = mutation_measurements
    for mutation, measured in mutation_measurements.items():
        _add_validation(
            validations,
            f"mutation_{mutation}",
            "a deliberately corrupted Hamiltonian escaping validation",
            "the designated validation must report a nonzero discrepancy",
            measured,
            measured > 1e-8,
            "the mutation would be invisible if this value were near zero",
        )

    # ---------------------------------------------------------------
    # 2. Six-step Lanczos chain and the exact recurrence relationship.
    # ---------------------------------------------------------------
    random_start = rng.normal(size=basis.dimension)
    six_step_chain = lanczos(hamiltonian.matvec, random_start, 6)
    orthogonality, completed_residual, full_residual = lanczos_relation_residuals(
        hamiltonian.matvec, six_step_chain
    )
    b_report = np.concatenate(([0.0], six_step_chain.betas))
    b_next_report = np.concatenate(
        (six_step_chain.betas, [six_step_chain.terminal_beta])
    )
    coefficient_rows = [
        {
            "m": index,
            "a_m": six_step_chain.alphas[index],
            "b_m": b_report[index],
            "b_m_plus_1": b_next_report[index],
        }
        for index in range(six_step_chain.n_steps)
    ]
    _write_rows(
        data_dir / "lanczos_first_six_coefficients.csv",
        ["m", "a_m", "b_m", "b_m_plus_1"],
        coefficient_rows,
    )
    np.savetxt(
        data_dir / "lanczos_T6.csv",
        six_step_chain.tridiagonal(),
        delimiter=",",
    )
    ground_start_chain = lanczos(
        hamiltonian.matvec,
        ground_state,
        3,
        breakdown_tolerance=1e-8,
    )
    results["lanczos_six_step"] = {
        "alphas": six_step_chain.alphas,
        "b_report_b0_through_b5": b_report,
        "b_report_b1_through_b6": b_next_report,
        "terminal_b6": six_step_chain.terminal_beta,
        "T6": six_step_chain.tridiagonal(),
        "orthogonality_residual": orthogonality,
        "completed_columns_residual": completed_residual,
        "full_recurrence_residual": full_residual,
        "ground_start_steps_before_breakdown": ground_start_chain.n_steps,
        "ground_start_terminal_beta": ground_start_chain.terminal_beta,
    }
    for name, value in (
        ("lanczos_orthogonality", orthogonality),
        ("lanczos_constructed_columns", completed_residual),
        ("lanczos_full_recurrence", full_residual),
    ):
        _add_validation(
            validations,
            name,
            "Lanczos indexing, coefficient, normalization, or recurrence error",
            "residual < 1e-10",
            value,
            value < 1e-10,
            "the Krylov basis or three-term recurrence fails its matrix identity",
        )

    # ---------------------------------------------------------
    # 3. Continued fraction versus direct sparse linear solves.
    # ---------------------------------------------------------
    e0 = np.zeros(basis.dimension)
    e0[0] = 1.0
    maximum_cf_steps = min(
        config.continued_fraction_lanczos_steps, basis.dimension
    )
    cf_chain = lanczos(hamiltonian.matvec, e0, maximum_cf_steps)
    requested_steps = [4, 8, 16, 32, 64, 128, 256, cf_chain.n_steps]
    convergence_steps = sorted(
        {step for step in requested_steps if 1 <= step <= cf_chain.n_steps}
    )
    z_values = [0.7 + 0.11j, -1.3 + 0.11j, 5.0 + 0.11j]
    fraction_rows: list[dict[str, Any]] = []
    final_deviations: dict[str, float] = {}
    for z in z_values:
        direct = direct_resolvent_element(sparse_hamiltonian, e0, z)
        for step in convergence_steps:
            approximation = continued_fraction(
                z,
                cf_chain.alphas[:step],
                cf_chain.betas[: step - 1],
            )
            deviation = abs(approximation - direct)
            fraction_rows.append(
                {
                    "z_real": z.real,
                    "z_imag": z.imag,
                    "lanczos_steps": step,
                    "cf_real": approximation.real,
                    "cf_imag": approximation.imag,
                    "direct_real": direct.real,
                    "direct_imag": direct.imag,
                    "absolute_deviation": deviation,
                }
            )
        final_deviations[str(z)] = float(fraction_rows[-1]["absolute_deviation"])
    _write_rows(
        data_dir / "continued_fraction_convergence.csv",
        [
            "z_real",
            "z_imag",
            "lanczos_steps",
            "cf_real",
            "cf_imag",
            "direct_real",
            "direct_imag",
            "absolute_deviation",
        ],
        fraction_rows,
    )
    results["continued_fraction"] = {
        "maximum_steps": cf_chain.n_steps,
        "convergence_table": fraction_rows,
        "final_absolute_deviations": final_deviations,
    }
    _add_validation(
        validations,
        "continued_fraction_vs_direct_solve",
        "forward recursion, omitted deepest alpha, wrong beta indexing, or wrong start vector",
        "all longest-chain deviations < 1e-8",
        max(final_deviations.values()),
        max(final_deviations.values()) < 1e-8,
        "the resolvent matrix elements disagree at one or more requested z values",
    )

    # ----------------------------------------------------------
    # 4, 5, and 7. Main DOS, U=0 benchmark, and interaction sweep.
    # ----------------------------------------------------------
    omega_shifted = np.linspace(
        config.omega_min, config.omega_max, config.omega_points
    )
    interaction_values = [0.0, 2.0, 4.0, 6.0, 8.0]
    dos_results: dict[float, DOSResult] = {}
    ratio_rows: list[dict[str, Any]] = []
    weight_rows: list[dict[str, Any]] = []
    ground_cache: dict[float, tuple[BlockBasis, np.ndarray, float]] = {
        config.main_interaction: (basis, ground_state, ground_energy)
    }

    for interaction_index, interaction in enumerate(interaction_values):
        if interaction in ground_cache:
            current_basis, current_ground, current_energy = ground_cache[interaction]
        else:
            current_basis, _, current_values, current_vectors = _ground_state(
                config.n_sites,
                config.n_up,
                config.n_down,
                config.hopping,
                interaction,
                config.random_seed + interaction_index,
                config.eigensolver_tolerance,
                n_eigenpairs=6 if interaction == 0.0 else 2,
            )
            current_energy = float(current_values[0])
            current_ground = current_vectors[:, 0]
            ground_cache[interaction] = (
                current_basis,
                current_ground,
                current_energy,
            )

        dos = total_density_of_states(
            current_basis,
            current_energy,
            current_ground,
            config.hopping,
            interaction,
            config.eta,
            omega_shifted,
            config.spectral_lanczos_steps,
            eigensolver_tolerance=config.eigensolver_tolerance,
            seed=config.random_seed + 10 * interaction_index,
        )
        dos_results[interaction] = dos
        _save_dos_csv(data_dir / f"dos_U{interaction:g}.csv", dos)
        zero_index = int(np.argmin(np.abs(omega_shifted)))
        rho_zero_ratio = float(dos.total[zero_index] / np.max(dos.total))
        particle_hole_channel_error = particle_hole_channel_relative_error(
            dos.addition,
            dos.removal,
        )
        ratio_rows.append(
            {
                "U": interaction,
                "rho_zero": dos.total[zero_index],
                "rho_max": np.max(dos.total),
                "rho_zero_over_rho_max": rho_zero_ratio,
                "chemical_potential": dos.chemical_potential,
                "particle_hole_add_rem_pointwise_relative_error": particle_hole_channel_error,
            }
        )
        weight_rows.append(
            {
                "U": interaction,
                "addition_weight": dos.addition_weight,
                "removal_weight": dos.removal_weight,
                "addition_error_from_N": dos.addition_weight - config.n_sites,
                "removal_error_from_N": dos.removal_weight - config.n_sites,
            }
        )
        _add_validation(
            validations,
            f"U={interaction:g}_separate_addition_weight",
            "wrong creation operator, target spin block, or omitted alpha-squared factor",
            f"w_add = N = {config.n_sites}",
            dos.addition_weight,
            abs(dos.addition_weight - config.n_sites) < 1e-9,
            "the addition zeroth moment differs from the empty-state count",
        )
        _add_validation(
            validations,
            f"U={interaction:g}_separate_removal_weight",
            "wrong annihilation operator, target spin block, or omitted alpha-squared factor",
            f"w_rem = N = {config.n_sites}",
            dos.removal_weight,
            abs(dos.removal_weight - config.n_sites) < 1e-9,
            "the removal zeroth moment differs from the particle count",
        )
        _add_validation(
            validations,
            f"U={interaction:g}_particle_hole_add_rem_pointwise_symmetry",
            "wrong chemical-potential shift or inconsistent addition/removal frequency sign",
            "rho_add(xi) = rho_rem(-xi) pointwise on the symmetric grid",
            particle_hole_channel_error,
            particle_hole_channel_error < 1e-5,
            "addition and mirrored removal channels disagree at half filling",
        )

    _write_rows(
        data_dir / "rho_zero_ratio_vs_U.csv",
        [
            "U",
            "rho_zero",
            "rho_max",
            "rho_zero_over_rho_max",
            "chemical_potential",
            "particle_hole_add_rem_pointwise_relative_error",
        ],
        ratio_rows,
    )
    _write_rows(
        data_dir / "spectral_weights_vs_U.csv",
        [
            "U",
            "addition_weight",
            "removal_weight",
            "addition_error_from_N",
            "removal_error_from_N",
        ],
        weight_rows,
    )

    free_exact = free_fermion_dos(
        omega_shifted, config.n_sites, config.hopping, config.eta
    )
    free_numerical = dos_results[0.0].total
    free_relative_max_error = float(
        np.max(np.abs(free_numerical - free_exact)) / np.max(free_exact)
    )
    np.savetxt(
        data_dir / "u0_analytic_benchmark.csv",
        np.column_stack(
            [omega_shifted, free_numerical, free_exact, free_numerical - free_exact]
        ),
        delimiter=",",
        header="omega_minus_mu,numerical,analytic,difference",
        comments="",
    )
    _add_validation(
        validations,
        "U=0_analytic_DOS",
        "hopping magnitude, periodic boundary, eta, continued-fraction order, or spectral normalization",
        "maximum error divided by analytic peak < 1e-8",
        free_relative_max_error,
        free_relative_max_error < 1e-8,
        "the broadened free-particle peaks differ in location, width, or weight",
    )

    results["spectra"] = {
        "rho_zero_ratio_table": ratio_rows,
        "weight_table": weight_rows,
        "u0_relative_max_error": free_relative_max_error,
        "chemical_potentials": {
            str(interaction): dos.chemical_potential
            for interaction, dos in dos_results.items()
        },
    }
    plot_stacked_dos(
        omega_shifted,
        {interaction: dos.total for interaction, dos in dos_results.items()},
        figure_dir / "dos_vs_U_stacked.png",
    )
    plot_rho_zero_ratio(
        [row["U"] for row in ratio_rows],
        [row["rho_zero_over_rho_max"] for row in ratio_rows],
        figure_dir / "rho_zero_ratio_vs_U.png",
    )
    plot_hubbard_band_schematic(figure_dir / "mott_hubbard_bands_schematic.png")
    plot_u0_benchmark(
        omega_shifted,
        free_numerical,
        free_exact,
        figure_dir / "u0_analytic_benchmark.png",
    )

    # ------------------------------------------------------------
    # 6. Degeneracy trap: full sum versus one-site-times-N shortcut.
    # ------------------------------------------------------------
    degeneracy_rows: list[dict[str, Any]] = []
    for n_sites in (6, 8):
        n_per_spin = n_sites // 2
        small_basis, _, small_values, small_vectors = _ground_state(
            n_sites,
            n_per_spin,
            n_per_spin,
            config.hopping,
            0.0,
            config.random_seed + n_sites,
            config.eigensolver_tolerance,
            n_eigenpairs=6,
        )
        state = small_vectors[:, 0]
        state = _select_extremal_local_density_ground_state(
            small_basis,
            small_values,
            small_vectors,
            config.degeneracy_tolerance,
        )
        full_add, full_rem, _ = local_add_remove_weights(small_basis, state)
        shortcut_add, shortcut_rem = _one_site_times_n_weights(small_basis, state)
        shell_gap = _closed_shell_gap(n_sites, n_per_spin, config.hopping)
        degeneracy_rows.append(
            {
                "N": n_sites,
                "U": 0.0,
                "ground_energy": small_values[0],
                "ground_degeneracy_in_computed_window": ground_state_degeneracy(
                    small_values, config.degeneracy_tolerance
                ),
                "safety_criterion": "positive free-fermion closed-shell gap",
                "single_particle_closed_shell_gap": shell_gap,
                "criterion_one_site_times_N_safe": shell_gap > 1e-10,
                **_degeneracy_weight_summary(
                    full_add,
                    full_rem,
                    shortcut_add,
                    shortcut_rem,
                ),
            }
        )
    interacting_full_add, interacting_full_rem, _ = local_add_remove_weights(
        basis, ground_state
    )
    interacting_shortcut_add, interacting_shortcut_rem = _one_site_times_n_weights(
        basis, ground_state
    )
    degeneracy_rows.append(
        {
            "N": config.n_sites,
            "U": config.main_interaction,
            "ground_energy": ground_energy,
            "ground_degeneracy_in_computed_window": degeneracy,
            "safety_criterion": "unique interacting ground state with translation symmetry",
            "single_particle_closed_shell_gap": "not applicable",
            "criterion_one_site_times_N_safe": degeneracy == 1,
            **_degeneracy_weight_summary(
                interacting_full_add,
                interacting_full_rem,
                interacting_shortcut_add,
                interacting_shortcut_rem,
            ),
        }
    )
    _write_rows(
        data_dir / "degeneracy_trap.csv",
        list(degeneracy_rows[0].keys()),
        degeneracy_rows,
    )
    results["degeneracy_trap"] = degeneracy_rows

    # --------------------------------------------------------------
    # 8. Lowest Ritz convergence and representative spectral shape.
    # --------------------------------------------------------------
    ritz_chain = lanczos(hamiltonian.matvec, rng.normal(size=basis.dimension), 60)
    ritz_values = lowest_ritz_history(ritz_chain.alphas, ritz_chain.betas)
    ritz_steps = np.arange(1, len(ritz_values) + 1)
    ritz_rows = [
        {
            "L": int(step),
            "lowest_ritz": value,
            "error_from_E0": value - ground_energy,
        }
        for step, value in zip(ritz_steps, ritz_values)
    ]
    _write_rows(
        data_dir / "ritz_convergence.csv",
        ["L", "lowest_ritz", "error_from_E0"],
        ritz_rows,
    )
    plot_ritz_convergence(
        ritz_steps,
        ritz_values,
        ground_energy,
        figure_dir / "ritz_convergence.png",
    )
    monotonic_violation = float(max(0.0, np.max(np.diff(ritz_values))))
    _add_validation(
        validations,
        "ritz_variational_monotonicity",
        "incorrect Krylov update or malformed leading tridiagonal blocks",
        "lowest Ritz values are nonincreasing with L",
        monotonic_violation,
        monotonic_violation < 1e-11,
        "a larger Krylov subspace raises the lowest Ritz estimate",
    )

    add_counts = target_particle_numbers(basis, "up", True)
    add_basis = BlockBasis(config.n_sites, *add_counts)
    add_initial = apply_local_operator(
        basis, add_basis, ground_state, 0, "up", dagger=True
    )
    add_hamiltonian = HubbardHamiltonian(
        add_basis, config.hopping, config.main_interaction
    )
    spectral_chain = lanczos(
        add_hamiltonian.matvec,
        add_initial,
        min(config.spectral_reference_lanczos_steps, add_basis.dimension),
        reorthogonalization_passes=2,
    )
    main_mu = dos_results[config.main_interaction].chemical_potential
    add_frequency = omega_shifted + main_mu
    add_z = add_frequency + 1j * config.eta + ground_energy
    reference_green = continued_fraction(
        add_z,
        spectral_chain.alphas,
        spectral_chain.betas,
        weight=spectral_chain.initial_norm**2,
    )
    reference_spectrum = -np.imag(reference_green) / np.pi
    spectral_convergence_rows: list[dict[str, Any]] = []
    for step in (10, 20, 40, 60):
        if step > spectral_chain.n_steps:
            continue
        approximate_green = continued_fraction(
            add_z,
            spectral_chain.alphas[:step],
            spectral_chain.betas[: step - 1],
            weight=spectral_chain.initial_norm**2,
        )
        approximate_spectrum = -np.imag(approximate_green) / np.pi
        relative_shape_error = float(
            np.max(np.abs(approximate_spectrum - reference_spectrum))
            / max(np.max(reference_spectrum), np.finfo(float).tiny)
        )
        spectral_convergence_rows.append(
            {"L": step, "relative_max_difference_from_reference": relative_shape_error}
        )
    _write_rows(
        data_dir / "spectral_shape_convergence.csv",
        ["L", "relative_max_difference_from_reference"],
        spectral_convergence_rows,
    )
    results["krylov_convergence"] = {
        "ritz_table": ritz_rows,
        "spectral_reference_steps": spectral_chain.n_steps,
        "spectral_reference_reorthogonalization_passes": 2,
        "spectral_shape_table": spectral_convergence_rows,
    }

    _write_rows(
        data_dir / "validation_checklist.csv",
        [
            "check",
            "target_error",
            "expectation",
            "measured",
            "conclusion",
            "failure_mode",
        ],
        validations,
    )
    results["validation_checklist"] = validations
    _write_json(data_dir / "all_results.json", results)
    print(f"Homework 3 outputs written to: {output_dir}")


if __name__ == "__main__":
    main()

