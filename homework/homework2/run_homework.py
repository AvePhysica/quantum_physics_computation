"""计算 Lecture 02 作业的全部必做和选做结果，并写出报告数据。"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from hubbard_model import (
    BONDS,
    COORDINATES,
    L,
    LEG_BONDS,
    RUNG_BONDS,
    analytic_trace,
    build_hamiltonian,
    sector_ground_energy,
)
from observables import (
    density_correlation_matrix,
    double_occupancies,
    local_densities,
    local_spin_z,
    spin_correlation_matrix,
    structure_factors,
    total_spin_squared,
)


OUTPUT_DIRECTORY = Path(__file__).resolve().parent / "output"
DEFAULT_PARAMETERS = {"t": 1.0, "u": 4.0, "v": 1.0, "mu": 4.0}
TOLERANCE = 1e-8


def ground_degeneracy(energies: np.ndarray) -> int:
    return int(np.count_nonzero(np.isclose(energies, energies[0], atol=TOLERANCE, rtol=0)))


def all_sector_spectra(parameters: dict[str, float]) -> dict[tuple[int, int], np.ndarray]:
    spectra = {}
    for n_up in range(L + 1):
        for n_down in range(L + 1):
            hamiltonian, _ = build_hamiltonian(n_up, n_down, **parameters)
            spectra[(n_up, n_down)] = np.linalg.eigvalsh(hamiltonian)
    return spectra


def global_lowest_states(
    spectra: dict[tuple[int, int], np.ndarray], number: int = 20
) -> list[dict[str, object]]:
    entries = sorted(
        (float(energy), n_up, n_down, level)
        for (n_up, n_down), energies in spectra.items()
        for level, energy in enumerate(energies)
    )
    result = []
    for rank, (energy, n_up, n_down, level) in enumerate(entries[:number], start=1):
        degeneracy = sum(abs(other[0] - energy) < TOLERANCE for other in entries)
        result.append(
            {
                "rank": rank,
                "energy": energy,
                "sector": [n_up, n_down],
                "sector_level": level,
                "global_degeneracy": degeneracy,
            }
        )
    return result


def bond_values(matrix: np.ndarray) -> dict[str, float]:
    return {f"({i},{j})": float(np.real_if_close(matrix[i, j])) for i, j in BONDS}


def finite_difference_ground_energy(
    parameter: str, center: float, epsilon: float = 1e-5
) -> float:
    plus = DEFAULT_PARAMETERS | {parameter: center + epsilon}
    minus = DEFAULT_PARAMETERS | {parameter: center - epsilon}
    return (
        sector_ground_energy(3, 3, **plus) - sector_ground_energy(3, 3, **minus)
    ) / (2 * epsilon)


def v_scan() -> list[dict[str, object]]:
    scan = []
    for v_value in np.arange(0, 3.01, 0.5):
        parameters = DEFAULT_PARAMETERS | {"v": float(v_value)}
        hamiltonian, basis = build_hamiltonian(3, 3, **parameters)
        energies, vectors = np.linalg.eigh(hamiltonian)
        state = vectors[:, 0]
        doubles = double_occupancies(state, basis)
        density_correlations = density_correlation_matrix(state, basis)
        scan.append(
            {
                "V": float(v_value),
                "ground_energy": float(energies[0]),
                "D": float(np.mean(doubles)),
                "bond_density": bond_values(density_correlations),
            }
        )
    return scan


def save_v_scan(scan: list[dict[str, object]]) -> None:
    csv_path = OUTPUT_DIRECTORY / "V_scan.csv"
    with csv_path.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.writer(stream)
        writer.writerow(["V", "D", *[f"n{i}n{j}" for i, j in BONDS]])
        for row in scan:
            writer.writerow(
                [row["V"], row["D"]]
                + [row["bond_density"][f"({i},{j})"] for i, j in BONDS]
            )

    figure, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    v_values = [row["V"] for row in scan]
    axes[0].plot(v_values, [row["D"] for row in scan], "o-", color="black")
    axes[0].set(xlabel="V", ylabel="D", title="Average double occupancy")
    axes[0].grid(alpha=0.3)

    for i, j in BONDS:
        kind = "leg" if (i, j) in LEG_BONDS else "rung"
        axes[1].plot(
            v_values,
            [row["bond_density"][f"({i},{j})"] for row in scan],
            "o-",
            label=f"({i},{j}) {kind}",
        )
    axes[1].set(xlabel="V", ylabel=r"$\langle n_i n_j\rangle$", title="Bond density correlations")
    axes[1].grid(alpha=0.3)
    axes[1].legend(fontsize=8, ncol=2)
    figure.tight_layout()
    figure.savefig(OUTPUT_DIRECTORY / "V_scan.png", dpi=180)
    plt.close(figure)


def calculate() -> dict[str, object]:
    OUTPUT_DIRECTORY.mkdir(exist_ok=True)
    parameters = DEFAULT_PARAMETERS.copy()

    hamiltonian, basis = build_hamiltonian(3, 3, **parameters)
    energies, eigenvectors = np.linalg.eigh(hamiltonian)
    ground_state = eigenvectors[:, 0]
    residual = np.linalg.norm(hamiltonian @ ground_state - energies[0] * ground_state)

    density = local_densities(ground_state, basis)
    spin_z = local_spin_z(ground_state, basis)
    doubles = double_occupancies(ground_state, basis)
    density_correlations = density_correlation_matrix(ground_state, basis)
    spin_correlations = spin_correlation_matrix(ground_state, basis)
    connected_density = density_correlations - np.outer(density, density)
    spin_squared = total_spin_squared(ground_state, basis)
    spin_quantum_number = (-1 + np.sqrt(max(0.0, 1 + 4 * spin_squared))) / 2

    spectra = all_sector_spectra(parameters)
    lowest_global = global_lowest_states(spectra)
    total_state_count = sum(len(values) for values in spectra.values())
    global_trace_numeric = sum(float(np.sum(values)) for values in spectra.values())
    global_trace_analytic = sum(
        analytic_trace(n_up, n_down, **parameters)
        for n_up in range(L + 1)
        for n_down in range(L + 1)
    )

    e33 = float(spectra[(3, 3)][0])
    e24 = float(spectra[(2, 4)][0])
    e34 = float(spectra[(3, 4)][0])
    e32 = float(spectra[(3, 2)][0])
    spin_gap = e24 - e33
    charge_gap = e34 + e32 - 2 * e33

    spin_structure = structure_factors(spin_correlations)
    charge_structure = structure_factors(density_correlations)

    scan = v_scan()
    save_v_scan(scan)

    # V=0 的标准 Hubbard 模型在半填充处取 mu=U/2=2，显式检查全局基态填充。
    v0_parameters = {"t": 1.0, "u": 4.0, "v": 0.0, "mu": 2.0}
    h_v0, basis_v0 = build_hamiltonian(3, 3, **v0_parameters)
    energies_v0, vectors_v0 = np.linalg.eigh(h_v0)
    state_v0 = vectors_v0[:, 0]
    v0_sector_ground_energies = {
        (n_up, n_down): sector_ground_energy(n_up, n_down, **v0_parameters)
        for n_up in range(L + 1)
        for n_down in range(L + 1)
    }
    global_v0_minimum = min(v0_sector_ground_energies.values())
    v0_ground_sectors = [
        list(sector)
        for sector, energy in v0_sector_ground_energies.items()
        if abs(energy - global_v0_minimum) < TOLERANCE
    ]

    derivative_u = finite_difference_ground_energy("u", parameters["u"])
    derivative_v = finite_difference_ground_energy("v", parameters["v"])
    bond_density_sum = sum(density_correlations[i, j] for i, j in BONDS)
    structure_spin_sum = sum(spin_structure.values())
    structure_charge_sum = sum(charge_structure.values())
    expected_spin_structure_sum = float(np.trace(spin_correlations))
    expected_charge_structure_sum = float(np.trace(density_correlations))

    checks = [
        {
            "target": "分块基态本征对",
            "expected": "norm(H psi - E psi) < 1e-10",
            "measured": float(residual),
            "passed": bool(residual < 1e-10),
            "detects": "矩阵对角化结果、列向量索引或本征值配对错误",
        },
        {
            "target": "49 个分块的完备性与全局谱",
            "expected": "总维数 4096，数值总迹等于组合计数解析总迹",
            "measured": {
                "dimension": total_state_count,
                "numeric_trace": global_trace_numeric,
                "analytic_trace": global_trace_analytic,
            },
            "passed": bool(
                total_state_count == 4096
                and abs(global_trace_numeric - global_trace_analytic) < 1e-8
            ),
            "detects": "漏掉粒子数分块、U/V/mu 项或键计数错误",
        },
        {
            "target": "局域密度与局域 Sz",
            "expected": "sum_i <n_i>=6，sum_i <Sz_i>=0",
            "measured": {"sum_n": float(np.sum(density)), "sum_sz": float(np.sum(spin_z))},
            "passed": bool(
                abs(np.sum(density) - 6) < 1e-10 and abs(np.sum(spin_z)) < 1e-10
            ),
            "detects": "上下自旋位序、局域占据或 Sz 的 1/2 因子错误",
        },
        {
            "target": "双占据",
            "expected": "dE0/dU = sum_i <n_i_up n_i_down>",
            "measured": {
                "finite_difference": derivative_u,
                "observable": float(np.sum(doubles)),
            },
            "passed": bool(abs(derivative_u - np.sum(doubles)) < 1e-5),
            "detects": "U 项、双占据算符或归一化错误",
        },
        {
            "target": "键密度关联",
            "expected": "dE0/dV = sum_bonds <n_i n_j>",
            "measured": {
                "finite_difference": derivative_v,
                "observable": float(bond_density_sum),
            },
            "passed": bool(abs(derivative_v - bond_density_sum) < 1e-5),
            "detects": "V 项、漏键或密度关联实现错误",
        },
        {
            "target": "全部密度关联",
            "expected": "sum_j <n_i n_j> = N <n_i>",
            "measured": float(np.max(np.abs(np.sum(density_correlations, axis=1) - 6 * density))),
            "passed": bool(np.allclose(np.sum(density_correlations, axis=1), 6 * density)),
            "detects": "关联矩阵的站点索引或概率权重错误",
        },
        {
            "target": "自旋关联与总自旋",
            "expected": "sum_ij <S_i dot S_j> = <S_tot^2> 且 S 接近整数/半整数",
            "measured": {
                "correlation_sum": float(np.sum(spin_correlations)),
                "S2": spin_squared,
                "S": float(spin_quantum_number),
            },
            "passed": bool(
                abs(np.sum(spin_correlations) - spin_squared) < 1e-10
                and abs(spin_quantum_number - round(2 * spin_quantum_number) / 2) < 1e-8
            ),
            "detects": "自旋翻转的费米子符号、1/2 系数或对角 S_i^2 错误",
        },
        {
            "target": "自旋隙和电荷隙所用分块",
            "expected": "自旋交换对称扇区的基态能相等",
            "measured": {
                "E24-E42": e24 - float(spectra[(4, 2)][0]),
                "E34-E43": e34 - float(spectra[(4, 3)][0]),
                "E32-E23": e32 - float(spectra[(2, 3)][0]),
            },
            "passed": bool(
                abs(e24 - spectra[(4, 2)][0]) < 1e-10
                and abs(e34 - spectra[(4, 3)][0]) < 1e-10
                and abs(e32 - spectra[(2, 3)][0]) < 1e-10
            ),
            "detects": "上下自旋处理不对称或能隙分块索引错误",
        },
        {
            "target": "结构因子",
            "expected": "六个 q 点求和等于实空间关联矩阵的对角和",
            "measured": {
                "spin_q_sum": structure_spin_sum,
                "spin_diagonal_sum": expected_spin_structure_sum,
                "charge_q_sum": structure_charge_sum,
                "charge_diagonal_sum": expected_charge_structure_sum,
            },
            "passed": bool(
                abs(structure_spin_sum - expected_spin_structure_sum) < 1e-9
                and abs(structure_charge_sum - expected_charge_structure_sum) < 1e-9
            ),
            "detects": "q 网格、相位符号、坐标或 1/N 归一化错误",
        },
        {
            "target": "V=0 半填充化学势",
            "expected": "mu=U/2=2 时全局基态包含 (3,3) 扇区",
            "measured": {"ground_sectors": v0_ground_sectors, "energy": global_v0_minimum},
            "passed": bool([3, 3] in v0_ground_sectors),
            "detects": "V=0 重算时化学势不在半满窗口或全局填充判断错误",
        },
    ]

    result = {
        "parameters": parameters,
        "sector_33": {
            "dimension": len(basis.states),
            "lowest_8_eigenvalues": [float(value) for value in energies[:8]],
            "ground_degeneracy": ground_degeneracy(energies),
            "ground_energy": float(energies[0]),
        },
        "global_lowest_20": lowest_global,
        "local_density": density.tolist(),
        "local_spin_z": spin_z.tolist(),
        "double_occupancy": doubles.tolist(),
        "average_double_occupancy": float(np.mean(doubles)),
        "spin_correlations": {
            "leg": {f"({i},{j})": float(spin_correlations[i, j]) for i, j in LEG_BONDS},
            "rung": {f"({i},{j})": float(spin_correlations[i, j]) for i, j in RUNG_BONDS},
        },
        "density_correlations": bond_values(density_correlations),
        "connected_density_correlations": bond_values(connected_density),
        "total_spin_squared": spin_squared,
        "spin_quantum_number": float(spin_quantum_number),
        "spin_gap": float(spin_gap),
        "charge_gap": float(charge_gap),
        "structure_factors": {
            "spin": {f"({n},{y})": value for (n, y), value in spin_structure.items()},
            "charge": {f"({n},{y})": value for (n, y), value in charge_structure.items()},
        },
        "V_scan": scan,
        "V0_mu2": {
            "ground_energy_33": float(energies_v0[0]),
            "local_density": local_densities(state_v0, basis_v0).tolist(),
            "local_spin_z": local_spin_z(state_v0, basis_v0).tolist(),
            "double_occupancy": double_occupancies(state_v0, basis_v0).tolist(),
            "average_double_occupancy": float(np.mean(double_occupancies(state_v0, basis_v0))),
            "global_ground_sectors": v0_ground_sectors,
        },
        "checks": checks,
    }
    return result


def format_vector(values: list[float]) -> str:
    return "[" + ", ".join(f"{value:.10f}" for value in values) + "]"


def write_markdown(result: dict[str, object]) -> None:
    lines = [
        "# Lecture 02 Homework Numerical Results",
        "",
        "参数：`t=1, U=4, V=1, mu=4`；除特别注明外均为 `(N_up,N_down)=(3,3)` 基态。",
        "",
        "## 必做 1：最低 8 个本征值",
        "",
        format_vector(result["sector_33"]["lowest_8_eigenvalues"]),
        "",
        f"基态能量 `{result['sector_33']['ground_energy']:.10f}`，简并度 `{result['sector_33']['ground_degeneracy']}`。",
        "",
        "## 必做 2：全系统最低 20 个本征值（按重数）",
        "",
        "|序号|能量|(N_up,N_down)|该能量的全局简并度|",
        "|---:|---:|:---:|---:|",
    ]
    for row in result["global_lowest_20"]:
        lines.append(
            f"|{row['rank']}|{row['energy']:.10f}|{tuple(row['sector'])}|{row['global_degeneracy']}|"
        )
    lines += [
        "",
        "## 必做 3：局域密度和局域自旋",
        "",
        f"`<n_i> = {format_vector(result['local_density'])}`",
        "",
        f"`<Sz_i> = {format_vector(result['local_spin_z'])}`",
        "",
        "## 必做 4：双占据",
        "",
        f"`<n_i_up n_i_down> = {format_vector(result['double_occupancy'])}`",
        "",
        f"平均双占据 `D = {result['average_double_occupancy']:.10f}`。",
        "",
        "## 必做 5：键自旋关联",
        "",
    ]
    for kind in ("leg", "rung"):
        lines.append(f"- {kind}: " + ", ".join(
            f"{bond}={value:.10f}" for bond, value in result["spin_correlations"][kind].items()
        ))
    lines += ["", "## 必做 6：键密度关联与连通关联", ""]
    for bond, value in result["density_correlations"].items():
        connected = result["connected_density_correlations"][bond]
        lines.append(f"- {bond}: `<n_i n_j>={value:.10f}`, `connected={connected:.10f}`")
    lines += [
        "",
        "## 必做 7：总自旋",
        "",
        f"`<S_tot^2>={result['total_spin_squared']:.10f}`，对应 `S={result['spin_quantum_number']:.10f}`。",
        "",
        "## 必做 8：能隙",
        "",
        f"自旋隙 `Delta_s={result['spin_gap']:.10f}`；电荷隙 `Delta_c={result['charge_gap']:.10f}`。",
        "",
        "## 选做 9：结构因子",
        "",
        "键 `(n_x,y_index)` 中 `y_index=0/1` 分别代表 `q_y=0/pi`。",
        "",
        "|q 索引|S(q)|N(q)|",
        "|:---:|---:|---:|",
    ]
    for key in result["structure_factors"]["spin"]:
        lines.append(
            f"|{key}|{result['structure_factors']['spin'][key]:.10f}|"
            f"{result['structure_factors']['charge'][key]:.10f}|"
        )
    lines += [
        "",
        "## 选做 10：V 扫描",
        "",
        "数值见 `output/V_scan.csv`，图见 `output/V_scan.png`。",
        "",
        "## 选做 11：V=0",
        "",
        "取 `mu=U/2=2`；显式比较 49 个扇区后，全局基态包含 `(3,3)`，因此仍在半填充窗口。",
        "",
        f"`<n_i> = {format_vector(result['V0_mu2']['local_density'])}`",
        "",
        f"`<Sz_i> = {format_vector(result['V0_mu2']['local_spin_z'])}`",
        "",
        f"`<n_i_up n_i_down> = {format_vector(result['V0_mu2']['double_occupancy'])}`",
        "",
        f"平均双占据 `D={result['V0_mu2']['average_double_occupancy']:.10f}`。",
        "",
        "## 校检清单",
        "",
        "|校检对象|期望|实测|结论|针对的错误|",
        "|---|---|---|:---:|---|",
    ]
    for check in result["checks"]:
        measured = json.dumps(check["measured"], ensure_ascii=False)
        lines.append(
            f"|{check['target']}|{check['expected']}|`{measured}`|"
            f"{'通过' if check['passed'] else '失败'}|{check['detects']}|"
        )
    (OUTPUT_DIRECTORY / "results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    result = calculate()
    (OUTPUT_DIRECTORY / "results.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_markdown(result)
    failures = [check["target"] for check in result["checks"] if not check["passed"]]
    if failures:
        raise RuntimeError(f"校检失败：{failures}")
    print("计算完成：所有校检通过。")
    print(f"结果目录：{OUTPUT_DIRECTORY}")


if __name__ == "__main__":
    main()
