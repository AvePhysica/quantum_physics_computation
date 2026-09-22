"""求解三个自旋 1/2 的开放链 Heisenberg 模型。"""

import numpy as np
import numpy.linalg as la


def spinmatrix(dimension: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """构造自旋简并维数为 2m+1 的自旋矩阵 (s_x, s_y, s_z)。

    输入自旋简并维数 dimension = 2m+1（m 为自旋量子数），输出取 ħ = 1 的
    三个自旋矩阵，其本征值为 -m, -m+1, ..., m。
    dimension = 2 时即自旋 1/2，S = σ/2（σ 为泡利矩阵）。
    """
    if dimension < 1:
        raise ValueError("自旋简并维数 dimension 必须为正整数")

    spin_quantum_number = (dimension - 1) / 2
    # 磁量子数按降序排列，与 |↑⟩ 在前、|↓⟩ 在后的基底顺序一致。
    magnetic_quantum_numbers = spin_quantum_number - np.arange(dimension)

    spin_z = np.diag(magnetic_quantum_numbers).astype(complex)

    # 升算符 S₊ = S_x + i S_y 满足 S₊|m⟩ = √(s(s+1) - m(m+1)) |m+1⟩。
    spin_plus = np.zeros((dimension, dimension), dtype=complex)
    for index in range(1, dimension):
        m = magnetic_quantum_numbers[index]
        spin_plus[index - 1, index] = np.sqrt(
            spin_quantum_number * (spin_quantum_number + 1) - m * (m + 1)
        )
    spin_minus = spin_plus.conj().T

    spin_x = (spin_plus + spin_minus) / 2
    spin_y = (spin_plus - spin_minus) / (2j)

    return spin_x, spin_y, spin_z


# 取 ħ = 1；dimension = 2 对应自旋 1/2，即 S = σ/2（σ 为泡利矩阵）。
spin_x, spin_y, spin_z = spinmatrix(2)
identity = np.array([[1, 0], [0, 1]], dtype=complex)

# 张量积基底的顺序；↑ 和 ↓ 分别表示 Sz = +1/2 和 -1/2。
basis_states = (
    "|↑↑↑⟩", "|↑↑↓⟩", "|↑↓↑⟩", "|↑↓↓⟩",
    "|↓↑↑⟩", "|↓↑↓⟩", "|↓↓↑⟩", "|↓↓↓⟩",
)


def build_hamiltonian() -> np.ndarray:
    """构造 H = S₁·S₂ + S₂·S₃，对应耦合常数 J = 1。"""
    hamiltonian = np.zeros((8, 8), dtype=complex)

    for spin in (spin_x, spin_y, spin_z):
        # A⊗B⊗C 分别作用于第 1、2、3 个自旋。
        bond_12 = np.kron(np.kron(spin, spin), identity)
        bond_23 = np.kron(np.kron(identity, spin), spin)
        hamiltonian += bond_12 + bond_23

    return hamiltonian


def build_total_spin() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """构造总自旋的三个分量：S_tot = S₁ + S₂ + S₃。"""
    return tuple(
        np.kron(np.kron(spin, identity), identity)
        + np.kron(np.kron(identity, spin), identity)
        + np.kron(np.kron(identity, identity), spin)
        for spin in (spin_x, spin_y, spin_z)
    )


def main() -> None:
    hamiltonian = build_hamiltonian()
    eigenvalues, eigenvectors = la.eigh(hamiltonian)

    print("三自旋 Heisenberg 模型：H = S₁·S₂ + S₂·S₃（ħ = J = 1）")
    print("基底顺序：", ", ".join(basis_states))
    print("\n哈密顿量矩阵：")
    print(np.real_if_close(hamiltonian))
    ground_energy = eigenvalues[0]
    ground_indices = np.flatnonzero(
        np.isclose(eigenvalues, ground_energy, atol=1e-10, rtol=0)
    )
    ground_degeneracy = len(ground_indices)
    print(f"\n基态能量：{ground_energy:.6f}，简并度：{ground_degeneracy}")
    print("\n全部本征值和本征态：")

    for index, energy in enumerate(eigenvalues):
        # 消除浮点计算造成的 -0.000000 等显示误差。
        energy = 0.0 if abs(energy) < 1e-10 else energy
        terms = []
        for coefficient, basis_state in zip(eigenvectors[:, index], basis_states):
            if abs(coefficient) > 1e-10:
                value = float(np.real_if_close(coefficient))
                if not terms:
                    terms.append(f"{value:.6f}{basis_state}")
                else:
                    sign = "+" if value >= 0 else "-"
                    terms.append(f"{sign} {abs(value):.6f}{basis_state}")

        ground_label = " [基态]" if np.isclose(
            energy, ground_energy, atol=1e-10, rtol=0
        ) else ""
        print(f"E{index + 1} = {energy:.6f}{ground_label}，|ψ{index + 1}⟩ = {' '.join(terms)}")

    total_spin = build_total_spin()
    total_spin_squared = sum(component @ component for component in total_spin)
    print("\n基态的总自旋平方期望值（S_tot = S₁ + S₂ + S₃）：")
    for index in ground_indices:
        state = eigenvectors[:, index]
        spin_squared = float(np.real_if_close(
            np.vdot(state, total_spin_squared @ state)
        ))
        print(f"|ψ{index + 1}⟩：⟨S_tot²⟩ = {spin_squared:.6f}")


if __name__ == "__main__":
    main()
# 程序入口：运行 main() 完成哈密顿量对角化并输出本征能量与本征态。
