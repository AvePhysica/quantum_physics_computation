"""对作业校检做四个可重复的故意改错实验。"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import numpy as np

import hubbard_model
import observables
from hubbard_model import L, analytic_trace, build_hamiltonian


OUTPUT_DIRECTORY = Path(__file__).resolve().parent / "output"
ASSIGNED_BONDS = (
    (0, 1), (1, 2), (3, 4), (4, 5), (0, 3), (1, 4), (2, 5)
)
TOLERANCE = 1e-10


def _one_particle_reference() -> np.ndarray:
    """直接按题目给出的七条键构造单粒子参考矩阵。"""
    reference = np.zeros((L, L))
    for i, j in ASSIGNED_BONDS:
        reference[i, j] = reference[j, i] = -1.0
    return reference


def _missing_bond_control() -> dict[str, object]:
    wrong_bonds = ASSIGNED_BONDS[:-1]
    with patch.object(hubbard_model, "BONDS", wrong_bonds):
        wrong_hamiltonian, _ = build_hamiltonian(1, 0, t=1, u=0, v=0, mu=0)
    residual = float(np.max(np.abs(wrong_hamiltonian - _one_particle_reference())))
    return {
        "id": "missing_bond",
        "mutation": "从 H 删除横档键 (2,5)",
        "validator": "(1,0) 单粒子矩阵与题目七键邻接矩阵逐元比较",
        "expected_for_correct_code": "maximum_residual < 1e-10",
        "measured": {"maximum_residual": residual},
        "detected": bool(residual >= TOLERANCE),
    }


def _flipped_hopping_sign_control() -> dict[str, object]:
    correct_hamiltonian, _ = build_hamiltonian(1, 0, t=1, u=0, v=0, mu=0)
    wrong_hamiltonian = -correct_hamiltonian
    residual = float(np.max(np.abs(wrong_hamiltonian - _one_particle_reference())))
    return {
        "id": "flipped_hopping_sign",
        "mutation": "把跃迁项整体从 -t 改成 +t",
        "validator": "(1,0) 单粒子矩阵与带 -t 的参考矩阵逐元比较",
        "expected_for_correct_code": "maximum_residual < 1e-10",
        "measured": {"maximum_residual": residual},
        "detected": bool(residual >= TOLERANCE),
    }


def _missing_u_term_control() -> dict[str, object]:
    parameters = {"t": 0.73, "u": 3.1, "v": 0.62, "mu": 1.4}
    wrong_hamiltonian, basis = build_hamiltonian(2, 1, **parameters)
    u_diagonal = np.array(
        [parameters["u"] * (up & down).bit_count() for up, down in basis.states]
    )
    wrong_hamiltonian = wrong_hamiltonian - np.diag(u_diagonal)
    expected_trace = analytic_trace(2, 1, **parameters)
    trace_error = float(abs(np.trace(wrong_hamiltonian).real - expected_trace))
    return {
        "id": "missing_u_term",
        "mutation": "从 H 的对角元中删除全部 U 双占据项",
        "validator": "数值迹与独立组合计数得到的解析迹比较",
        "expected_for_correct_code": "trace_error < 1e-10",
        "measured": {"trace_error": trace_error},
        "detected": bool(trace_error >= TOLERANCE),
    }


def _missing_spin_half_factor_control() -> dict[str, object]:
    hamiltonian, basis = build_hamiltonian(3, 3, t=1, u=4, v=1, mu=4)
    _, vectors = np.linalg.eigh(hamiltonian)
    state = vectors[:, 0]

    correct = np.asarray(observables.spin_correlation_matrix(state, basis), dtype=float)
    up, down = observables._occupation_arrays(basis)
    probabilities = observables._probabilities(state)
    spin_z = (up - down) / 2
    longitudinal = np.einsum("a,ai,aj->ij", probabilities, spin_z, spin_z)

    # 正确的非对角元是 longitudinal + 1/2 * transverse_sum。
    # 2*correct-longitudinal 等价于故意漏掉 1/2 后的结果。
    wrong = correct.copy()
    off_diagonal = ~np.eye(L, dtype=bool)
    wrong[off_diagonal] = (2 * correct - longitudinal)[off_diagonal]
    wrong_s2 = float(np.sum(wrong))
    singlet_error = abs(wrong_s2)
    return {
        "id": "missing_spin_half_factor",
        "mutation": "在自旋关联的横向翻转项中漏掉 1/2",
        "validator": "半填充非简并基态须满足 SU(2) 单态关系 <S_tot^2>=0",
        "expected_for_correct_code": "abs(S2) < 1e-10",
        "measured": {"wrong_S2": wrong_s2, "singlet_error": singlet_error},
        "detected": bool(singlet_error >= TOLERANCE),
    }


def evaluate_negative_controls() -> list[dict[str, object]]:
    """返回四个故意改错实验的结果；detected=True 表示校检成功报错。"""
    return [
        _missing_bond_control(),
        _flipped_hopping_sign_control(),
        _missing_u_term_control(),
        _missing_spin_half_factor_control(),
    ]


def write_results(results: list[dict[str, object]]) -> None:
    OUTPUT_DIRECTORY.mkdir(exist_ok=True)
    (OUTPUT_DIRECTORY / "negative_control_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    lines = [
        "# 故意改错负向验证",
        "",
        "每个实验都实际构造错误的哈密顿量或观测量，并要求原有独立校检拒绝它。",
        "",
        "|故意改错|使用的独立校检|错误版本实测值|是否成功检出|",
        "|---|---|---|:---:|",
    ]
    for result in results:
        measured = json.dumps(result["measured"], ensure_ascii=False)
        lines.append(
            f"|{result['mutation']}|{result['validator']}|`{measured}`|"
            f"{'是' if result['detected'] else '否'}|"
        )
    lines += [
        "",
        "这里的“成功检出”表示：错误版本没有通过对应校检。测试结束后不会修改正式实现。",
    ]
    (OUTPUT_DIRECTORY / "negative_control_results.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    results = evaluate_negative_controls()
    write_results(results)
    missed = [result["id"] for result in results if not result["detected"]]
    if missed:
        raise RuntimeError(f"以下故意错误未被校检发现：{missed}")
    print("4 个故意改错实验均被独立校检成功检出。")


if __name__ == "__main__":
    main()
