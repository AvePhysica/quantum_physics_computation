"""Human-readable intent and failure signatures for every numerical check."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationDescription:
    targeted_error: str
    failure_signature: str


def describe_validation(name: str) -> ValidationDescription:
    """Return the error class and observable failure mode for a check name."""
    entries = [
        (
            name == "N=16 sector dimensions sum",
            "固定 popcount 基枚举发生漏态、重复态或磁量子数到 n_up 的换算错误",
            "各扇区维数之和不再等于 2^16=65536，且零磁化扇区可能偏离 C(16,8)=12870",
        ),
        (
            name.startswith("N=2 singlet energy"),
            "N=2 周期最近邻键被重复计数，或交换项的符号与 1/2 系数错误",
            "单态能量偏离 -3/4；典型双计数会给出 -3/2",
        ),
        (
            name.startswith("N=2 triplet"),
            "N=2 对角 SzSz 项或横向翻转项的相对系数错误",
            "m=0 三重态能量偏离 +1/4，或与其余三重态不再简并",
        ),
        (
            name.startswith("N=4 Heisenberg ground"),
            "周期键列表、XY 翻转矩阵元或 SzSz 对角项构造错误",
            "精确基态能量不再等于 -2J1",
        ),
        (
            name.startswith("spin translation entries"),
            "把费米 Fock 基的交换负号错误地带入自旋张量积基平移",
            "平移置换矩阵会出现 -1 或非实相位，而不是所有非零元均为 +1",
        ),
        (
            name.startswith("T^N=I"),
            "位旋转方向、周期掩码或跨边界映射错误",
            "某个位串平移 N 次后不能回到自身，T^N-I 出现非零元",
        ),
        (
            name.startswith("Hermiticity"),
            "翻转跃迁只写入一个方向，或共轭相位/矩阵索引处理错误",
            "H-H^dagger 的最大矩阵元显著非零，本征值还可能出现虚部",
        ),
        (
            name.startswith("[H,T]"),
            "周期边界、J2 键或平移约定与 Hamiltonian 的格点编号不一致",
            "交换子 HT-TH 出现非零矩阵元，等价平移态得到不同能量",
        ),
        (
            name.startswith("P_k orthonormality"),
            "轨道重复、短轨道允许条件错误或遗漏 1/sqrt(ell) 归一化",
            "Gram 矩阵 P_k^dagger P_k-I 非零；漏归一化时对角元按轨道长度放大",
        ),
        (
            name.startswith("T P_k=e^(ik) P_k"),
            "动量指数正负号、T 的方向或轨道内排序错误",
            "TP_k-e^(ik)P_k 非零，常见表现是把 m 错标为 N-m",
        ),
        (
            name.startswith("sum momentum dimensions"),
            "短轨道的动量选择规则导致态被遗漏或在多个块中重复计数",
            "全部动量块维数之和不等于固定 Sztot 扇区维数 12870",
        ),
        (
            name.startswith("U(1) vs block ground"),
            "投影矩阵或 H_k=P_k^dagger H P_k 的装配错误",
            "所有动量块的最低值与未分动量 U(1) 基态能量不一致",
        ),
        (
            name.startswith("ground-subspace resolution"),
            "简并基态子空间截取不全，或子空间内平移算符对角化错误",
            "解析后的确定动量态能量偏离原 U(1) 基态，或漏掉简并动量",
        ),
        (
            name.startswith("sum local Sz"),
            "bit 的上下自旋约定或局域 Sz 期望值公式错误",
            "逐点局域磁矩之和不等于所选扇区的 Sztot=0",
        ),
        (
            name.startswith("max local Sx"),
            "错误地在固定 Sztot 基内闭合单自旋翻转，或态重构混入其他扇区",
            "固定 Sztot 本征态出现显著非零的局域 <Sx_i>",
        ),
        (
            name.startswith("singlet correlation sum rule"),
            "SxSx+SySy 关联系数、基态选择或总自旋单态性质处理错误",
            "总和 sum_r <S0 dot Sr> 显著偏离 0",
        ),
        (
            name.startswith("normalized structure-factor sum rule"),
            "结构因子遗漏 1/N、FFT 归一化或 q 网格索引错误",
            "sum_q S(q) 不等于 C(0)=3/4；遗漏 1/N 时 N=16 会得到 12",
        ),
        (
            name.startswith("SU(2) Cdot=3Czz"),
            "自旋点积关联的横向系数错误，或 Delta=1 Hamiltonian 未保持 SU(2)",
            "逐点 C(r)-3Czz(r) 在数值误差以上非零",
        ),
        (
            name.startswith("spin inversion E(M)=E(-M)"),
            "上下自旋编码、扇区 Hamiltonian 或 Zeeman 符号不对称",
            "互为自旋翻转的 M 与 -M 扇区最低能量不同",
        ),
        (
            name.startswith("N=8 block-spectrum union"),
            "动量轨道遗漏/重复、块 Hamiltonian 错误或某些块本征值未完整求出",
            "拼接后的 70 个块谱不能逐点匹配直接 U(1) 全谱",
        ),
        (
            name.startswith("MG D0 residual") or name.startswith("MG D1 residual"),
            "J2/J1=1/2 键系数、周期二聚体的单态符号或跨边界配对错误",
            "精确二聚体态的残差 norm[(H+3N/8)D] 不再接近机器精度",
        ),
        (
            name.startswith("MG ED ground energy"),
            "Hamiltonian 或最低本征值求解器给出错误的 MG 点基态",
            "ED 最低能量偏离解析值 -3NJ1/8",
        ),
        (
            name.startswith("MG k=0 combination"),
            "D0、D1 的相对号、归一化或平移方向错误",
            "对称组合不满足 T(D0+D1)=+(D0+D1)",
        ),
        (
            name.startswith("MG k=pi combination"),
            "D0、D1 的相对号、归一化或平移方向错误",
            "反对称组合不满足 T(D0-D1)=-(D0-D1)",
        ),
        (
            name.startswith("XX free-fermion"),
            "XY 跃迁幅度、Jordan-Wigner 奇偶边界或半填充占据规则错误",
            "自旋 ED 基态能量与正确周期/反周期自由费米子填充能量不一致",
        ),
        (
            name.startswith("Delta=0.5 breaks SU(2)"),
            "代码把 Delta 硬编码为 1，或各向异性 SzSz 项没有真正生效",
            "Delta=0.5 时 C(r)-3Czz(r) 仍错误地接近 0，未显示 SU(2) 破缺",
        ),
        (
            name.startswith("FAULT: N=2 double-counted"),
            "校检是否能捕获 N=2 最近邻键重复计数",
            "注入后 E0 从 -0.75 变为 -1.5；若仍判为正确则说明基准无检错力",
        ),
        (
            name.startswith("FAULT: unnormalized momentum"),
            "校检是否能捕获动量轨道漏掉 1/sqrt(ell) 归一化",
            "注入后 Gram 偏差变为 15；若 P^dagger P 检查不报警则校检失效",
        ),
        (
            name.startswith("FAULT: omitted J2"),
            "校检是否能捕获 J2=0.5 时次近邻键被遗漏",
            "注入后 E0 错成 -7.142296361 而非 -6；MG 能量基准应立即失败",
        ),
        (
            name.startswith("FAULT: wrong Jordan-Wigner"),
            "校检是否能捕获 XX 映射选错费米奇偶边界条件",
            "N=8 注入后能量偏差为 0.198912367；解析-ED 对照应失败",
        ),
    ]
    for matches, targeted_error, failure_signature in entries:
        if matches:
            return ValidationDescription(targeted_error, failure_signature)
    raise KeyError(f"No validation description registered for: {name}")

