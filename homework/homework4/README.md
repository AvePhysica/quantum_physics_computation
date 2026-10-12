# 第四次作业：一维 $J_1$-$J_2$ XXZ 自旋链

本项目用固定总磁量子数 $S^z_{\mathrm{tot}}$ 与晶格平移动量的双重分块，完成周期边界自旋 $1/2$ 链的精确对角化。默认参数为 $N=16$、$J_1=1$、$\Delta=1$，比较 $J_2=0$ 与 $J_2=0.5$。代码还包含题目中的全部四项加分计算。

## 目录说明

- `j1j2_basis.py`：固定粒子数位串基、无符号自旋平移。
- `j1j2_hamiltonian.py`：固定 $S^z_{\mathrm{tot}}$ 稀疏哈密顿量。
- `momentum_blocks.py`：平移轨道、动量投影和分块矩阵。
- `solvers.py`：稀疏最低本征对与简并基态动量解析。
- `observables.py`：局域磁矩、关联函数、结构因子和磁化包络。
- `analytics.py`：Majumdar--Ghosh 二聚体态与 XX 自由费米子基准。
- `plots.py`：四张结果图。
- `validation_catalog.py`：逐条校检所针对的错误类型和预期失败表现。
- `run_homework4.py`：运行全部数值任务并输出数据。
- `tests/`：15 项自动化测试。
- `output/result.md`：独立的中文结果文档。
- `output/report.tex`、`output/report.pdf`：LaTeX 报告源码和最终 PDF。
- `output/data/`：全部 CSV 与 JSON 原始结果。
- `output/figures/`：计算生成的图片。
- `AI_USAGE_RECORD.md`：本次作业的 AI Agent 使用与对话记录。

## 环境与运行

建议使用 Python 3.11 或更新版本：

```powershell
python -m pip install -r requirements.txt
python -m pytest tests -q --basetemp=.pytest_tmp
python run_homework4.py
```

重新编译报告：

```powershell
Set-Location output
xelatex -interaction=nonstopmode -halt-on-error report.tex
xelatex -interaction=nonstopmode -halt-on-error report.tex
```

## 关键约定：不存在额外费米平移负号

位 $j$ 表示格点 $j$，`1` 表示自旋向上，平移定义为 $T|s_0s_1\cdots s_{N-1}\rangle=|s_{N-1}s_0\cdots s_{N-2}\rangle$，即格点 $j$ 移到 $j+1$。这里的计算基是自旋张量积基，不是按产生算符排序的费米 Fock 基；因此平移只是位串置换，所有非零矩阵元都是 $+1$，不应附加交换负号。

费米奇偶性只出现在 XX 极限的 Jordan--Wigner 解析校验中。程序分别计算周期与反周期单粒子动量格点，再取与自旋精确对角化一致的边界条件。该符号约定由 $T^N=I$、$[H,T]=0$、$TP_k=e^{ik}P_k$ 和动量块谱并集四类检查共同约束。

## 数值方法摘要

固定 $n_\uparrow$ 后，基维数为 $\binom{N}{n_\uparrow}$。每条键的作用为

$$
S_i^zS_j^z=\begin{cases}+1/4,&s_i=s_j,\\-1/4,&s_i\ne s_j,\end{cases}
\qquad
S_i^xS_j^x+S_i^yS_j^y=\frac12(S_i^+S_j^-+S_i^-S_j^+).
$$

对于长度为 $\ell$ 的平移轨道，只有满足 $e^{ik\ell}=1$ 的动量被允许，并使用

$$
|r;k\rangle=\frac1{\sqrt\ell}\sum_{n=0}^{\ell-1}e^{-ikn}T^n|r\rangle,
\qquad T|r;k\rangle=e^{ik}|r;k\rangle.
$$

主体系只构造固定 $S^z_{\mathrm{tot}}$ 的稀疏矩阵；$N=16$ 不构造完整 $2^{16}\times2^{16}$ 稠密矩阵。完整数值与误差见 `output/result.md`。

结构因子采用归一化约定

$$
S(q)=\frac1N\sum_r e^{-iqr}C(r),
$$

因此离散动量求和满足 $\sum_qS(q)=C(0)=3/4$。

