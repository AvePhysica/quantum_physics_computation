# 第三讲作业：Hubbard 环上的 Lanczos 方法与谱函数

本目录包含第三讲作业的完整源码、自动校检、数值结果、作图程序和 LaTeX 报告。
主计算严格使用固定 $(N_\uparrow,N_\downarrow)$ 的 $U(1)\times U(1)$
分块；谱函数使用 Lanczos 三对角化与反向连分数，不使用全 Hilbert 空间稠密
对角化后逐本征态求和。

## 文件结构

- `hubbard_basis.py`：定粒子数基底、O(1) mask 查找表和费米算符符号。
- `hubbard_operator.py`：matrix-free Hamiltonian、独立稀疏矩阵及低能本征求解。
- `lanczos.py`：Lanczos 递推、三对角矩阵、Ritz 值和反向连分数。
- `spectral.py`：加减粒子目标块、化学势、谱权重和总态密度。
- `plots.py`：数值图绘制。
- `run_homework3.py`：一次生成全部数值结果、校检表与数值图。
- `tests/`：单元测试、解析基准和故障注入测试。
- `AI_USAGE_RECORD.md`：逐条记录本次作业的用户 prompt、AI 返回要点与修改日志。
- `output/result.md`：集中保存本次运行得到的数值结果与解释。
- `output/pdf/Homework3_Hubbard_Lanczos_Report.tex`：最终报告的 LaTeX 源码。
- `output/pdf/Homework3_Hubbard_Lanczos_Report.pdf`：最终 PDF。

## 约定

- 每个自旋种类使用一个 $N$ 位整数，比特 $j$ 表示格点 $j$。
- 全局轨道顺序为
  $(0\uparrow,\ldots,N-1\uparrow,0\downarrow,\ldots,N-1\downarrow)$。
- 基底先按 `up_mask` 的整数值排序，再按 `down_mask` 排序。
- Lanczos 系数使用 $a_0,\ldots,a_{M-1}$ 与
  $b_1,\ldots,b_{M-1}$，并约定 $b_0=0$。
- 连分数从最深层向外反向递推，初始向量的范数 $\alpha^2$ 必须乘回。
- Hamiltonian 中不加入化学势项；谱图横轴为 $\omega-\mu$。

## 环境与运行

安装 Python 依赖：

```powershell
python -m pip install -r requirements.txt
```

运行测试：

```powershell
python -m pytest -q -p no:cacheprovider
```

生成数值结果与图片：

```powershell
python run_homework3.py
```

使用 XeLaTeX 生成最终报告：

```powershell
Set-Location output/pdf
xelatex -interaction=nonstopmode -halt-on-error Homework3_Hubbard_Lanczos_Report.tex
xelatex -interaction=nonstopmode -halt-on-error Homework3_Hubbard_Lanczos_Report.tex
```

第二次编译用于更新目录和交叉引用。

## 输出

数值数据位于 `output/data/`，图片位于 `output/figures/`。最终 PDF 使用以下
四张数值图：

1. `dos_vs_U_stacked.png`：不同相互作用强度下的总态密度；
2. `u0_analytic_benchmark.png`：$U=0$ 数值谱与解析谱；
3. `rho_zero_ratio_vs_U.png`：$\rho(0)/\rho_{\max}$ 随 $U$ 的变化；
4. `ritz_convergence.png`：最低 Ritz 值与能量误差的收敛。

详细数值请直接阅读 [`output/result.md`](output/result.md)。

## 校检说明

当前测试共 24 项，结果校检共 30 条。校检覆盖：

- matrix-free Hamiltonian 与独立 CSR 矩阵的一致性；
- 厄米性、相互作用 trace 和基态残差；
- Lanczos 正交性与三项递推；
- 连分数与直接稀疏线性求解；
- 加、减谱分别满足的权重求和规则；
- $U=0$ 自由费米子解析谱；
- 粒子-空穴关系 $\rho_{\rm add}(\xi)=\rho_{\rm rem}(-\xi)$ 的逐点比较；
- Ritz 变分单调性，以及相对 480 步完全再正交参考链的谱形收敛；
- 翻转跳跃符号、删除周期边界键、删除 $U$ 项的故障注入。

逐条记录见 `output/data/validation_checklist.csv`。

