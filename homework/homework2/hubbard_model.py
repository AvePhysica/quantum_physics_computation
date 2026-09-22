"""2x3 扩展 Hubbard 梯子的分块基底与哈密顿量。"""

from dataclasses import dataclass
from itertools import combinations
from math import comb

import numpy as np


L = 6
LEG_BONDS = ((0, 1), (1, 2), (3, 4), (4, 5))
RUNG_BONDS = ((0, 3), (1, 4), (2, 5))
BONDS = LEG_BONDS + RUNG_BONDS
COORDINATES = np.array(((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1)))


def _bit_patterns(number: int) -> tuple[int, ...]:
    """返回 6 位中恰有 ``number`` 个 1 的全部整数。"""
    return tuple(sum(1 << site for site in occupied) for occupied in combinations(range(L), number))


@dataclass(frozen=True)
class SectorBasis:
    """固定粒子数扇区的基底及 O(1) 查找表。"""

    n_up: int
    n_down: int
    states: tuple[tuple[int, int], ...]
    index: dict[tuple[int, int], int]

    @classmethod
    def create(cls, n_up: int, n_down: int) -> "SectorBasis":
        if not (0 <= n_up <= L and 0 <= n_down <= L):
            raise ValueError("n_up 和 n_down 必须在 0 到 6 之间")
        states = tuple(
            (up_bits, down_bits)
            for up_bits in _bit_patterns(n_up)
            for down_bits in _bit_patterns(n_down)
        )
        return cls(n_up, n_down, states, {state: i for i, state in enumerate(states)})


def combined_bits(state: tuple[int, int]) -> int:
    """轨道顺序为 (0↑,...,5↑,0↓,...,5↓)，合并成 12 位整数。"""
    up_bits, down_bits = state
    return up_bits | (down_bits << L)


def split_bits(bits: int) -> tuple[int, int]:
    mask = (1 << L) - 1
    return bits & mask, (bits >> L) & mask


def apply_fermion_operations(
    state: tuple[int, int], operations: tuple[tuple[str, int], ...]
) -> tuple[tuple[int, int], int] | None:
    """从左到右按实际作用次序（算符式从右到左）施加产生/湮灭算符。"""
    bits = combined_bits(state)
    sign = 1
    for operation, orbital in operations:
        occupied = (bits >> orbital) & 1
        parity = (bits & ((1 << orbital) - 1)).bit_count()
        sign *= -1 if parity % 2 else 1
        if operation == "annihilate":
            if not occupied:
                return None
            bits ^= 1 << orbital
        elif operation == "create":
            if occupied:
                return None
            bits |= 1 << orbital
        else:
            raise ValueError(f"未知费米子操作：{operation}")
    return split_bits(bits), sign


def apply_hop(
    state: tuple[int, int], source: int, target: int, spin: int
) -> tuple[tuple[int, int], int] | None:
    """施加 c_target^dagger c_source；spin=0/1 表示上/下自旋。"""
    source_orbital = source + spin * L
    target_orbital = target + spin * L
    return apply_fermion_operations(
        state,
        (("annihilate", source_orbital), ("create", target_orbital)),
    )


def diagonal_energy(
    state: tuple[int, int], u: float, v: float, mu: float
) -> float:
    """计算相互作用和化学势贡献。"""
    up_bits, down_bits = state
    double_occupancy = (up_bits & down_bits).bit_count()
    densities = [
        ((up_bits >> site) & 1) + ((down_bits >> site) & 1)
        for site in range(L)
    ]
    bond_density = sum(densities[i] * densities[j] for i, j in BONDS)
    particle_number = up_bits.bit_count() + down_bits.bit_count()
    return u * double_occupancy + v * bond_density - mu * particle_number


def build_hamiltonian(
    n_up: int,
    n_down: int,
    t: float = 1.0,
    u: float = 4.0,
    v: float = 1.0,
    mu: float = 4.0,
) -> tuple[np.ndarray, SectorBasis]:
    """在固定 ``(n_up, n_down)`` 扇区构造稠密厄米矩阵。"""
    basis = SectorBasis.create(n_up, n_down)
    dimension = len(basis.states)
    hamiltonian = np.zeros((dimension, dimension), dtype=float)

    for column, state in enumerate(basis.states):
        hamiltonian[column, column] = diagonal_energy(state, u, v, mu)
        for i, j in BONDS:
            for spin in (0, 1):
                for source, target in ((i, j), (j, i)):
                    result = apply_hop(state, source, target, spin)
                    if result is not None:
                        new_state, sign = result
                        row = basis.index[new_state]
                        hamiltonian[row, column] += -t * sign

    return hamiltonian, basis


def analytic_trace(
    n_up: int,
    n_down: int,
    t: float = 1.0,
    u: float = 4.0,
    v: float = 1.0,
    mu: float = 4.0,
) -> float:
    """用组合计数独立给出分块哈密顿量的迹；跃迁项的迹为零。"""
    del t
    dimension = comb(L, n_up) * comb(L, n_down)
    mean_double_sum = n_up * n_down / L
    same_spin = (
        n_up * (n_up - 1) + n_down * (n_down - 1)
    ) / (L * (L - 1))
    opposite_spin = 2 * n_up * n_down / (L * L)
    mean_bond_sum = len(BONDS) * (same_spin + opposite_spin)
    return dimension * (
        u * mean_double_sum + v * mean_bond_sum - mu * (n_up + n_down)
    )


def sector_ground_energy(n_up: int, n_down: int, **parameters: float) -> float:
    hamiltonian, _ = build_hamiltonian(n_up, n_down, **parameters)
    return float(np.linalg.eigvalsh(hamiltonian)[0])
