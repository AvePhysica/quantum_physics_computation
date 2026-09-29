# 第三讲作业：Hubbard 环上的 Lanczos 方法与谱函数

> 本文件是 Gate 2 的报告骨架。所有 `{{...}}` 内容必须在 Gate 3 运行、
> 校检并核对后替换；不得把占位符或未经执行的估计值作为最终结果。

## 1. 问题与参数

研究周期边界的一维 Hubbard 环：

$$
H=-t\sum_{j,\sigma}(c^\dagger_{j\sigma}c_{j+1,\sigma}+\mathrm{h.c.})
+U\sum_j n_{j\uparrow}n_{j\downarrow}.
$$

主计算参数为 `N=8, t=1, U=4, eta=0.11`，半满且不在 Hamiltonian 中加入
化学势项。谱图横轴为 `omega-mu`，其中

$$
\mu=\frac12[E_0(N+1)-E_0(N-1)].
$$

## 2. 表示、分块与费米符号

每个自旋用一个 N 位整数表示占据。基底限制在固定
`(N_up,N_down)` 块中，维数的解析式为

$$
\dim\mathcal H_{N_\uparrow,N_\downarrow}
=\binom{N}{N_\uparrow}\binom{N}{N_\downarrow}.
$$

mask 到单自旋列表位置的查找表预先存为长度 `2^N` 的数组，因此块内索引
查询为 O(1)。全局轨道排序采用

`0up,1up,...,(N-1)up,0down,...,(N-1)down`。

作用 `c_p` 或 `c_p^dagger` 时，符号为轨道 p 之前已占据轨道数的奇偶性。
跳跃项始终按“先湮灭、再产生”执行，因此周期边界键不需要手写特殊符号。

## 3. Hamiltonian 与基态

- `(4,4)` 块维数：`{{BLOCK_DIMENSION}}`
- 基态能量：`{{GROUND_ENERGY}}`
- 基态简并度及判定容差：`{{GROUND_DEGENERACY}}`

主算法使用 matrix-free `H @ vector`。另用一套独立的跳跃符号代码装配 CSR
稀疏矩阵，仅用于校检和直接线性求解。需在此列出随机复向量作用误差、
厄米残差、相互作用 trace 和基态残差。

`{{MAIN_BLOCK_VALIDATION_TABLE}}`

## 4. Lanczos 三对角化

从固定随机种子的随机向量开始，递推得到

$$
Hq_m=b_mq_{m-1}+a_mq_m+b_{m+1}q_{m+1}.
$$

本文采用 `b_0=0`。系数表同时列出 `b_m` 与 `b_(m+1)`，从而明确区分
`T_6` 使用的 `b_1,...,b_5` 和末列残差使用的 `b_6`。前六组系数：

`{{LANCZOS_COEFFICIENT_TABLE}}`

对应的 `T_6`：

`{{T6_MATRIX}}`

对于已构造完成的列检查 `HQ=QT`；若包括第六列，则必须把
`b_6 q_6 e_5^T` 末项写回。正交性、已完成列残差及完整递推残差为：

`{{LANCZOS_RESIDUAL_TABLE}}`

若起始向量是严格基态，`H|Phi_0>=E_0|Phi_0>`，减去 `a_0|Phi_0>` 后的
残差为零。因此精确算术中只产生一个 Krylov 向量，在计算下一耦合系数时
立即停止；数值上终止值由基态本征残差和 breakdown 容差决定。

## 5. 连分数与直接求解

对未归一化初始向量 `|Psi_0>`，令 `alpha^2=<Psi_0|Psi_0>`。Green 函数为

$$
G(z)=\alpha^2\frac{1}{z-a_0-\frac{b_1^2}{z-a_1-\cdots}}.
$$

连分数必须从最深层反向递推，否则会把系数对应到另一个三对角矩阵；
循环还必须包含最深的 `a_m`。三个指定复频率的比较及 Krylov 步数收敛表：

`{{CONTINUED_FRACTION_TABLE}}`

误差取决于 Krylov 空间对起始向量谱测度的逼近，以及 z 到实轴极点的距离；
较小的虚部和更接近极点的位置通常要求更长的 Krylov 链。

## 6. 总态密度与权重

加电子分别进入 `(5,4)`、`(4,5)` 块；减电子分别进入 `(3,4)`、`(4,3)`
块。每个格点和自旋都显式求和。加法使用
`z=omega+i eta+E0`，减法使用 `z=-omega+i eta+E0`。

- 化学势：`{{CHEMICAL_POTENTIAL}}`
- 加法权重：`{{ADDITION_WEIGHT}}`
- 减法权重：`{{REMOVAL_WEIGHT}}`

插入图：`dos_vs_U_stacked.png`。

## 7. U=0 解析基准

$$
\rho(\omega)=2\sum_k\frac{1}{\pi}
\frac{\eta}{(\omega+2t\cos(2\pi k/N))^2+\eta^2}.
$$

相对于解析峰值归一的最大偏差：`{{U0_RELATIVE_MAX_ERROR}}`。

这条检查同时锁定跳跃能标、周期边界、展宽、总权重，以及连分数递推的
方向和最深层索引。插入图：`u0_analytic_benchmark.png`。

## 8. 选做：简并陷阱

`{{DEGENERACY_TRAP_TABLE}}`

判断准则：检查每个自旋填充到费米面的最后占据能级和第一个未占据能级
之间是否为严格正的闭壳层能隙。若费米面穿过简并能级，数值求得的简并
基态线性组合未必具有格点均匀性，“一格点乘 N”不安全。还应与 U=4 的
非简并基态对比。

## 9. 选做：Mott 演化

`{{RHO_ZERO_RATIO_TABLE}}`

插入图：`rho_zero_ratio_vs_U.png`。

物理讨论：`{{MOTT_PHYSICAL_DISCUSSION}}`

## 10. 选做：Krylov 维度收敛

`{{RITZ_CONVERGENCE_TABLE}}`

最低 Ritz 值按变分原理应随 Krylov 空间扩大而不升高。能量通常由极端
本征值控制而较快收敛；完整谱形需要在整个相关能窗内逼近多个极点和权重，
因此可能需要明显更大的 Krylov 维数。谱形差异须明确写成相对 480 步完全
再正交参考链的自参照指标，不得表述为相对于精确谱的严格误差。

插入图：`ritz_convergence.png`。

## 11. 校检清单

每条必须包含：校检对象、期望、实测、结论、针对的错误及失败表现。

`{{VALIDATION_CHECKLIST}}`

故障注入包括：翻转跳跃符号、删除周期边界键、删除 U 项。最终报告需给出
它们触发的非零偏差，并确认随后使用的是恢复后的正确 Hamiltonian。

## 12. 源码与复现

`{{SOURCE_MAP_AND_COMMANDS}}`

记录 Python 与依赖版本、随机种子、频率网格、Lanczos 最大步数、
本征求解与 breakdown 容差。

## 13. 额外工作与自驱项

- 对每个 U 逐点检查
  $\rho_{\rm add}(\xi)=\rho_{\rm rem}(-\xi)$。
- 使用相互作用 trace 的组合公式专门检查 U 项。
- 对错误 Hamiltonian 做故障注入，证明检查确实会失败。
- 比较能量与谱形的 Krylov 收敛速度。

## 14. AI 使用说明

最终 AI 对话记录须等 Gate 3 的数值结果经学生确认后，在 Gate 4 根据真实
对话单独生成。本报告不预造对话内容。

