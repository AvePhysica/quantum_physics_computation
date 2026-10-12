"""Generate all mandatory and optional numerical results for Homework 4."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy.sparse import identity

from analytics import dimer_product_state, free_fermion_half_filled_energy, normalized_dimer_momenta
from io_utils import save_csv, save_json
from j1j2_basis import fixed_popcount_basis, rotate_sites
from j1j2_hamiltonian import build_sector_hamiltonian
from momentum_blocks import block_hamiltonian, momentum_projector, translation_matrix
from observables import (
    local_spin_expectations,
    longitudinal_correlations,
    lower_envelope_transitions,
    magnetization_envelope,
    spin_correlations,
    structure_factor,
)
from plots import plot_dispersion, plot_j2_scan, plot_magnetization, plot_structure_factor
from solvers import ground_momenta_from_subspace, lowest_eigenpairs, sector_ground_energies
from validation_catalog import describe_validation


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output"
DATA = OUTPUT / "data"
FIGURES = OUTPUT / "figures"
N_MAIN = 16
J1 = 1.0
DELTA = 1.0
COUPLINGS = (0.0, 0.5)
TOLERANCE = 1e-9


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)
    DATA.mkdir(exist_ok=True)
    FIGURES.mkdir(exist_ok=True)
    results: dict = {"parameters": {"N": N_MAIN, "J1": J1, "Delta": DELTA, "J2": list(COUPLINGS)}}
    validations: list[dict] = []

    def validate(name: str, measured: float, tolerance: float, *, target: float = 0.0, fault: bool = False) -> None:
        error = abs(measured - target)
        passed = error <= tolerance
        if fault:
            passed = error > tolerance
        description = describe_validation(name)
        validations.append(
            {
                "check": name,
                "targeted_error": description.targeted_error,
                "failure_signature": description.failure_signature,
                "target": target,
                "measured": measured,
                "absolute_error": error,
                "tolerance": tolerance,
                "status": "PASS" if passed else "FAIL",
                "fault_injection": fault,
            }
        )

    print("[1/7] dimensions and small-system benchmarks", flush=True)
    dimension_rows = []
    for n_up in range(N_MAIN + 1):
        dimension_rows.append(
            {
                "n_up": n_up,
                "Sztot": n_up - N_MAIN / 2,
                "dimension": len(fixed_popcount_basis(N_MAIN, n_up)),
            }
        )
    save_csv(DATA / "n16_sector_dimensions.csv", dimension_rows)
    results["dimensions"] = {
        "Sz0": dimension_rows[N_MAIN // 2]["dimension"],
        "sum": sum(row["dimension"] for row in dimension_rows),
        "full": 2**N_MAIN,
    }
    validate("N=16 sector dimensions sum", results["dimensions"]["sum"], 0.0, target=2**N_MAIN)

    h2 = build_sector_hamiltonian(2, 1)
    spectrum2 = np.linalg.eigvalsh(h2.toarray())
    validate("N=2 singlet energy", float(spectrum2[0]), 1e-13, target=-0.75)
    validate("N=2 triplet m=0 energy", float(spectrum2[1]), 1e-13, target=0.25)
    h4 = build_sector_hamiltonian(4, 2)
    validate("N=4 Heisenberg ground", float(np.linalg.eigvalsh(h4.toarray())[0]), 1e-12, target=-2.0)

    basis16 = fixed_popcount_basis(N_MAIN, N_MAIN // 2)
    translation16 = translation_matrix(N_MAIN, basis16)
    unsigned_entries = np.asarray(translation16.data)
    validate("spin translation entries are +1", float(np.max(np.abs(unsigned_entries - 1.0))), 0.0)
    max_cycle_error = max(
        int(rotate_sites(int(state), N_MAIN, N_MAIN) != int(state)) for state in basis16
    )
    validate("T^N=I (bit permutation)", float(max_cycle_error), 0.0)

    print("[2/7] N=16 U(1) and momentum blocks", flush=True)
    main_rows = []
    dispersion_tables: dict[str, list[dict]] = {}
    magnetization_plot_data: dict[str, tuple[np.ndarray, np.ndarray]] = {}
    structure_plot_data: dict[str, np.ndarray] = {}
    ground_summaries: dict[str, dict] = {}
    sector_tables: dict[str, dict[float, float]] = {}
    correct_hamiltonians = {}

    for j2 in COUPLINGS:
        label = f"J2={j2:g}"
        print(f"  {label}", flush=True)
        hamiltonian = build_sector_hamiltonian(N_MAIN, N_MAIN // 2, j1=J1, j2=j2, delta=DELTA)
        correct_hamiltonians[j2] = hamiltonian
        hermitian_residual = hamiltonian - hamiltonian.conj().T
        hermitian_error = float(np.max(np.abs(hermitian_residual.data))) if hermitian_residual.nnz else 0.0
        validate(f"Hermiticity {label}", hermitian_error, 1e-13)
        commutator = hamiltonian @ translation16 - translation16 @ hamiltonian
        commutator_error = float(np.max(np.abs(commutator.data))) if commutator.nnz else 0.0
        validate(f"[H,T]=0 {label}", commutator_error, 1e-13)

        u1_values, _ = lowest_eigenpairs(hamiltonian, count=8)
        ground_energy = float(u1_values[0])
        degeneracy = int(np.sum(np.abs(u1_values - ground_energy) <= TOLERANCE))
        momentum_rows = []
        resolved_levels: list[tuple[float, int, int]] = []
        projector_orthogonality = 0.0
        projector_phase = 0.0
        for m in range(N_MAIN):
            projector = momentum_projector(N_MAIN, basis16, m)
            gram = projector.conj().T @ projector - identity(projector.shape[1], dtype=complex)
            if gram.nnz:
                projector_orthogonality = max(projector_orthogonality, float(np.max(np.abs(gram.data))))
            phase = np.exp(2j * np.pi * m / N_MAIN)
            phase_difference = translation16 @ projector - phase * projector
            if phase_difference.nnz:
                projector_phase = max(projector_phase, float(np.max(np.abs(phase_difference.data))))
            block = block_hamiltonian(hamiltonian, projector)
            values, _ = lowest_eigenpairs(block, count=4)
            row = {
                "m": m,
                "k_over_pi": 2.0 * m / N_MAIN,
                "dimension": block.shape[0],
                "E0": float(values[0]),
                "E1": float(values[1]) if len(values) > 1 else np.nan,
                "E2": float(values[2]) if len(values) > 2 else np.nan,
                "E3": float(values[3]) if len(values) > 3 else np.nan,
                "energy": float(values[0]),
            }
            momentum_rows.append(row)
            resolved_levels.extend((float(value), m, index) for index, value in enumerate(values))
        validate(f"P_k orthonormality {label}", projector_orthogonality, 2e-12)
        validate(f"T P_k=e^(ik) P_k {label}", projector_phase, 2e-12)
        validate(
            f"sum momentum dimensions {label}",
            float(sum(row["dimension"] for row in momentum_rows)),
            0.0,
            target=float(len(basis16)),
        )
        block_ground = min(row["E0"] for row in momentum_rows)
        validate(f"U(1) vs block ground {label}", block_ground, 2e-10, target=ground_energy)
        ground_momenta = [row["m"] for row in momentum_rows if abs(row["E0"] - ground_energy) <= TOLERANCE]
        excitation_energy = min(level[0] for level in resolved_levels if level[0] > ground_energy + TOLERANCE)
        excitation_momenta = sorted(
            {level[1] for level in resolved_levels if abs(level[0] - excitation_energy) <= TOLERANCE}
        )
        dispersion_tables[label] = momentum_rows
        save_csv(DATA / f"n16_momentum_J2_{j2:g}.csv", momentum_rows)

        resolved_energy, resolved_momenta, ground_vectors = ground_momenta_from_subspace(
            hamiltonian, basis16, N_MAIN
        )
        validate(f"ground-subspace resolution {label}", resolved_energy, 2e-10, target=ground_energy)
        ground_vector = ground_vectors[:, 0]
        local_sz, local_sx = local_spin_expectations(ground_vector, basis16, N_MAIN)
        local_rows = [
            {"site": site, "Sz": local_sz[site], "Sx": local_sx[site]} for site in range(N_MAIN)
        ]
        save_csv(DATA / f"n16_local_observables_J2_{j2:g}.csv", local_rows)
        validate(f"sum local Sz {label}", float(np.sum(local_sz)), 2e-12)
        validate(f"max local Sx {label}", float(np.max(np.abs(local_sx))), 2e-12)

        correlations = spin_correlations(ground_vector, basis16, N_MAIN)
        longitudinal = longitudinal_correlations(ground_vector, basis16, N_MAIN)
        structure = structure_factor(correlations)
        structure_plot_data[label] = structure
        correlation_rows = [
            {"r": r, "Cdot": correlations[r], "Czz": longitudinal[r], "S_q": structure[r]}
            for r in range(N_MAIN)
        ]
        save_csv(DATA / f"n16_correlations_J2_{j2:g}.csv", correlation_rows)
        validate(f"singlet correlation sum rule {label}", float(np.sum(correlations)), 5e-10)
        validate(
            f"normalized structure-factor sum rule {label}",
            float(np.sum(structure)),
            5e-12,
            target=0.75,
        )
        validate(
            f"SU(2) Cdot=3Czz {label}",
            float(np.max(np.abs(correlations - 3.0 * longitudinal))),
            5e-10,
        )

        print(f"    all Sztot sectors for {label}", flush=True)
        sector_energies = sector_ground_energies(N_MAIN, j1=J1, j2=j2, delta=DELTA)
        sector_tables[label] = sector_energies
        sector_rows = [
            {"Sztot": magnetization, "energy": energy}
            for magnetization, energy in sorted(sector_energies.items())
        ]
        save_csv(DATA / f"n16_sector_energies_J2_{j2:g}.csv", sector_rows)
        spin_inversion_error = max(
            abs(energy - sector_energies[-magnetization])
            for magnetization, energy in sector_energies.items()
        )
        validate(f"spin inversion E(M)=E(-M) {label}", float(spin_inversion_error), 2e-10)
        hull, transitions = lower_envelope_transitions(sector_energies)
        critical_rows = [
            {"M_left": left, "M_right": right, "critical_field": field}
            for left, right, field in transitions
        ]
        save_csv(DATA / f"n16_critical_fields_J2_{j2:g}.csv", critical_rows)
        maximum_field = max(field for _, _, field in transitions) + 0.4
        fields = np.linspace(0.0, maximum_field, 1601)
        magnetization_density, envelope_energy = magnetization_envelope(
            sector_energies, fields, N_MAIN
        )
        magnetization_plot_data[label] = (fields, magnetization_density)
        save_csv(
            DATA / f"n16_magnetization_curve_J2_{j2:g}.csv",
            [
                {"field": field, "m_density": density, "envelope_energy": energy}
                for field, density, energy in zip(fields, magnetization_density, envelope_energy)
            ],
        )

        excited_sz0 = min(value for value in u1_values if value > ground_energy + TOLERANCE)
        spin_gap = sector_energies[1.0] - ground_energy
        ground_summaries[label] = {
            "energy": ground_energy,
            "energy_per_site": ground_energy / N_MAIN,
            "u1_degeneracy": degeneracy,
            "ground_momenta": ground_momenta,
            "resolved_ground_momenta": resolved_momenta,
            "lowest_excitation_energy": excitation_energy,
            "lowest_excitation_gap": excitation_energy - ground_energy,
            "lowest_excitation_momenta": excitation_momenta,
            "lowest_Sz0_excitation_gap": float(excited_sz0 - ground_energy),
            "spin_gap": float(spin_gap),
            "local_Sz_max_abs": float(np.max(np.abs(local_sz))),
            "local_Sx_max_abs": float(np.max(np.abs(local_sx))),
            "correlation_sum": float(np.sum(correlations)),
            "structure_factor_peak_m": int(np.argmax(structure)),
            "critical_fields": critical_rows,
            "magnetization_hull": hull,
        }
        main_rows.append(
            {
                "J2": j2,
                "E0": ground_energy,
                "E0_per_site": ground_energy / N_MAIN,
                "degeneracy": degeneracy,
                "ground_momenta": ";".join(map(str, ground_momenta)),
                "lowest_excitation_momenta": ";".join(map(str, excitation_momenta)),
                "spin_gap": spin_gap,
            }
        )
    results["n16"] = ground_summaries
    save_csv(DATA / "n16_ground_summary.csv", main_rows)

    print("[3/7] N=8 complete spectra in every momentum block", flush=True)
    n8_full = {}
    basis8 = fixed_popcount_basis(8, 4)
    for j2 in COUPLINGS:
        h8 = build_sector_hamiltonian(8, 4, j2=j2)
        rows = []
        all_block_values = []
        for m in range(8):
            projector = momentum_projector(8, basis8, m)
            values = np.linalg.eigvalsh(block_hamiltonian(h8, projector).toarray())
            all_block_values.extend(values)
            rows.extend(
                {"m": m, "k_over_pi": 2.0 * m / 8, "level": level, "energy": float(value)}
                for level, value in enumerate(values)
            )
        direct_values = np.linalg.eigvalsh(h8.toarray())
        spectral_error = float(np.max(np.abs(np.sort(all_block_values) - direct_values)))
        validate(f"N=8 block-spectrum union J2={j2:g}", spectral_error, 2e-11)
        save_csv(DATA / f"n8_full_spectrum_J2_{j2:g}.csv", rows)
        n8_full[f"J2={j2:g}"] = {"levels": len(rows), "union_error": spectral_error}
    results["n8_full_spectrum"] = n8_full

    print("[4/7] Majumdar-Ghosh and XX analytic benchmarks", flush=True)
    mg_rows = []
    for n_sites in (8, 10, 12):
        basis = fixed_popcount_basis(n_sites, n_sites // 2)
        hamiltonian = build_sector_hamiltonian(n_sites, n_sites // 2, j2=0.5)
        d0 = dimer_product_state(n_sites, basis, shift=0)
        d1 = dimer_product_state(n_sites, basis, shift=1)
        energy = -3.0 * n_sites / 8.0
        translation = translation_matrix(n_sites, basis)
        plus, minus = normalized_dimer_momenta(d0, d1)
        ed_values, _ = lowest_eigenpairs(hamiltonian, count=1)
        row = {
            "N": n_sites,
            "target_energy": energy,
            "ED_ground_energy": float(ed_values[0]),
            "ED_error": abs(float(ed_values[0]) - energy),
            "D0_residual": float(np.linalg.norm(hamiltonian @ d0 - energy * d0)),
            "D1_residual": float(np.linalg.norm(hamiltonian @ d1 - energy * d1)),
            "D0_translation_to_D1": float(np.linalg.norm(translation @ d0 - d1)),
            "D0_is_T_eigen_residual": float(np.linalg.norm(translation @ d0 - d0)),
            "k0_residual": float(np.linalg.norm(translation @ plus - plus)),
            "kpi_residual": float(np.linalg.norm(translation @ minus + minus)),
            "D0_D1_overlap": float(np.real(np.vdot(d0, d1))),
        }
        mg_rows.append(row)
        validate(f"MG D0 residual N={n_sites}", row["D0_residual"], 2e-12)
        validate(f"MG D1 residual N={n_sites}", row["D1_residual"], 2e-12)
        validate(f"MG ED ground energy N={n_sites}", row["ED_ground_energy"], 2e-11, target=energy)
        validate(f"MG k=0 combination N={n_sites}", row["k0_residual"], 2e-12)
        validate(f"MG k=pi combination N={n_sites}", row["kpi_residual"], 2e-12)
    save_csv(DATA / "majumdar_ghosh_checks.csv", mg_rows)
    results["majumdar_ghosh"] = mg_rows

    xx_rows = []
    for n_sites in (8, 10, 12):
        basis = fixed_popcount_basis(n_sites, n_sites // 2)
        hamiltonian = build_sector_hamiltonian(n_sites, n_sites // 2, delta=0.0)
        numerical, _ = lowest_eigenpairs(hamiltonian, count=1)
        analytic = free_fermion_half_filled_energy(n_sites)
        row = {
            "N": n_sites,
            "numerical": float(numerical[0]),
            "analytic": analytic.energy,
            "error": abs(float(numerical[0]) - analytic.energy),
            "chosen_boundary": analytic.boundary,
            "periodic_energy": analytic.periodic_energy,
            "antiperiodic_energy": analytic.antiperiodic_energy,
        }
        xx_rows.append(row)
        validate(f"XX free-fermion N={n_sites}", row["error"], 2e-11)
    save_csv(DATA / "xx_free_fermion_checks.csv", xx_rows)
    results["xx_free_fermion"] = xx_rows

    print("[5/7] anisotropy comparison and J2 scan", flush=True)
    h_anisotropic = build_sector_hamiltonian(N_MAIN, N_MAIN // 2, delta=0.5)
    _, anisotropic_vectors = lowest_eigenpairs(h_anisotropic, count=1)
    anisotropic_c = spin_correlations(anisotropic_vectors[:, 0], basis16, N_MAIN)
    anisotropic_zz = longitudinal_correlations(anisotropic_vectors[:, 0], basis16, N_MAIN)
    anisotropy_deviation = float(np.max(np.abs(anisotropic_c - 3.0 * anisotropic_zz)))
    results["anisotropy"] = {
        "Delta=0.5 max_abs_Cdot_minus_3Czz": anisotropy_deviation,
        "interpretation": "nonzero as expected when SU(2) is broken",
    }
    validate("Delta=0.5 breaks SU(2) relation (deliberate contrast)", anisotropy_deviation, 1e-5, fault=True)

    scan_rows = []
    for j2 in np.linspace(0.0, 1.0, 11):
        hamiltonian = build_sector_hamiltonian(N_MAIN, N_MAIN // 2, j2=float(j2))
        energy, momenta, _ = ground_momenta_from_subspace(hamiltonian, basis16, N_MAIN)
        scan_rows.append(
            {
                "j2": float(j2),
                "energy": energy,
                "energy_per_site": energy / N_MAIN,
                "ground_momenta": ";".join(map(str, momenta)),
            }
        )
        print(f"  scan J2={j2:.1f}: E0/N={energy/N_MAIN:.9f}, m={momenta}", flush=True)
    save_csv(DATA / "n16_j2_scan.csv", scan_rows)
    results["j2_scan"] = scan_rows

    print("[6/7] deliberate fault injections", flush=True)
    double_count_energy = float(np.linalg.eigvalsh((2.0 * h2).toarray())[0])
    validate("FAULT: N=2 double-counted bond is detected", double_count_energy, 1e-6, target=-0.75, fault=True)
    p0 = momentum_projector(N_MAIN, basis16, 0)
    bad_projector = np.sqrt(N_MAIN) * p0
    bad_gram = bad_projector.conj().T @ bad_projector - identity(bad_projector.shape[1])
    bad_gram_error = float(np.max(np.abs(bad_gram.data)))
    validate("FAULT: unnormalized momentum projector is detected", bad_gram_error, 1e-6, fault=True)
    correct_mg_energy = ground_summaries["J2=0.5"]["energy"]
    omitted_j2_energy = ground_summaries["J2=0"]["energy"]
    validate(
        "FAULT: omitted J2 bonds are detected at J2=0.5",
        omitted_j2_energy,
        1e-6,
        target=correct_mg_energy,
        fault=True,
    )
    xx8 = xx_rows[0]
    wrong_boundary_energy = (
        xx8["antiperiodic_energy"]
        if xx8["chosen_boundary"] == "periodic"
        else xx8["periodic_energy"]
    )
    validate(
        "FAULT: wrong Jordan-Wigner boundary is detected for N=8",
        wrong_boundary_energy,
        1e-6,
        target=xx8["numerical"],
        fault=True,
    )

    print("[7/7] figures and machine-readable summary", flush=True)
    plot_dispersion(dispersion_tables, FIGURES / "dispersion_n16.png")
    plot_magnetization(magnetization_plot_data, FIGURES / "magnetization_n16.png")
    plot_j2_scan(scan_rows, FIGURES / "j2_scan_n16.png")
    plot_structure_factor(structure_plot_data, FIGURES / "structure_factor_n16.png")
    save_csv(DATA / "validation_checks.csv", validations)
    results["validations"] = validations
    results["validation_summary"] = {
        "passed": sum(row["status"] == "PASS" for row in validations),
        "failed": sum(row["status"] != "PASS" for row in validations),
        "total": len(validations),
    }
    save_json(DATA / "raw_results.json", results)
    if results["validation_summary"]["failed"]:
        raise RuntimeError("One or more validation checks failed; inspect validation_checks.csv")
    print(f"All {results['validation_summary']['total']} validation checks passed.", flush=True)


if __name__ == "__main__":
    main()
