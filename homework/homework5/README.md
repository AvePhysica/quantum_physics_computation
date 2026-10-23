# 第五次作业：开边界 J1–J2 XXZ 链的传统 DMRG

本项目研究开边界自旋 $1/2$ 链基态，用真正的密度矩阵截断完成传统双格点块 DMRG。已实现全部必做及选做 1 至 4；精确对角化是独立基准，不参与 DMRG 优化。

## 环境与一次运行

建议 Python 3.11 或更新版本，依赖见 requirements.txt。报告另外需要 TeX Live 的 XeLaTeX、latexmk、ctex、adjustbox 等常用宏包。中文使用 ctex 默认 Windows 字体配置。所有命令在本作业目录执行：

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python run_homework5.py
python build_report.py
```

最后一个命令绘图、生成全部文档，并用 XeLaTeX 编译到 output/report.pdf；latexmk 不可用时自动调用 XeLaTeX 两次。需要只重建文字与图而暂不编译时使用 `python build_report.py --no-compile`。重新运行计算会覆盖本作业的生成结果，原始作业 PDF 保留。

交付前的可复现检查为 `python verify_outputs.py`：核对 Markdown/PDF 表格与原始 JSON、逐键 CSV 及长链 MPS 存档。该检查另需 Poppler 的 pdftotext，并先运行 `python -m unittest discover -s tests -v > output/test_results.log 2>&1` 保存测试结果；检查摘要写入 output/submission_audit.json。

`python run_homework5.py` 默认包含全部选做。只重算原有必做及选做 1/2 时用 `python run_homework5.py --base-only`，之后还需 `python run_optional.py` 才能重建完整报告。若基础数值已存在，可直接运行 `python run_optional.py` 更新选做 3/4，再执行报告构建。长链和全参数扫描需要更多时间；逐步进度会显示在控制台。

新增定量分析可以单独通过 `python refine_results.py` 重算，不必再次求解相同的物理系统，随后执行 `python build_report.py`。这一步计算 err–epsilon 的幂律与线性拟合，以及同尺寸、同方法的二聚化基线扣除，并增加独立校检。完整运行入口也自动包含该步骤。

若 Python 有多套环境，请选择已安装 NumPy、SciPy、Matplotlib 的同一解释器运行以上所有命令。程序在导入 NumPy 前设置小矩阵运算的单线程默认值，避免过多线程带来的开销。峰值内存主要来自 $N=20$ 的稀疏精确对角化和独立张量作用校检。

## 目录及主要结果

```text
Lecture05_Homework.pdf       原始要求
requirements.txt            数值与绘图依赖
src/core.py                 ED 与传统块 DMRG 核心
src/analysis.py             观测量、一次投影和独立张量校检
src/mps_observables.py      物理 MPS、可扩展逐键关联与独立比特测量
src/refinements.py          误差/权重拟合、同尺寸基线扣除
tests/                      物理及截断回归测试
run_homework5.py             一次生成全部实际数值
run_optional.py              长链及二聚化扫描，可单独重算
optional_report.py           选做 3/4 的结果表、图、物理讨论
refine_results.py            重算误差标度与基线扣除
review_report.py             上述分析及文献相图对照的图表
verify_outputs.py            文档/数据/存档一致性复核
build_report.py              同源生成文档、图、LaTeX PDF
README.md                   本中文说明
AI_USAGE_RECORD.md          用户授权后生成的真实 AI 使用与对话记录
report/report.tex           最终报告 LaTeX 源文件
output/result.md            按题号排列的独立完整结果文档
output/validation.md        逐条校检的错误类型、期望、实测与结论
output/data/results.json    全部原始数值、局部日志、校检和环境版本
output/data/state_*.npz     N=20 最终态及对应整数基矢
output/data/mps_N*.npz      N=40/60 物理 MPS，按张量序号保存
output/data/dimer_bonds.csv 全网格和各尺寸的逐键关联
output/data/dimer_baseline.csv 同尺寸基线与相对增强
output/figures/              PNG 预览及 PDF 矢量图
output/report.pdf           最终合并报告
```

[完整数值结果](output/result.md)、[逐条校检](output/validation.md)、[合并 PDF 报告](output/report.pdf)。报告中的表和图全部来自同一个 results.json，避免手工抄写差异。用户已明确授权，已生成[AI 使用与对话记录](AI_USAGE_RECORD.md)，包含 prompt 原文、可见回复要点、产出文件和修改原因台账。提交时请将该记录与源码及报告一并保留。

## 模型、参数与算法

自旋归一化为 $S^\alpha=\sigma^\alpha/2$，无周期回绕。默认 $J_1=1,\Delta=1$；$N,J_1,J_2,\Delta,\chi$ 都是算法接口参数。例如：

```python
from src.core import dmrg
run = dmrg(n=20, j1=1.0, j2=0.3, delta=1.0, chi=32, max_sweeps=12)
print(run['energy'])
```

比特 j 对应格点 j，1 表示向上。ED 按固定向上自旋数产生基并按整数排序，直接用翻转矩阵元构造稀疏 H。DMRG 的块张量基为“外端到内端”，局域基为向下、向上；右块物理位置反向，恢复态时显式转换。

块保存 H、磁化标签和内边缘最近两个格点的 $S^z,S^+,S^-$。第二套边缘算符用于长度为 2 的相互作用。超块用矩阵自由迭代求解，跨中点恰有最近邻一条、次近邻两条键。

截断先按 $q_A+q_B=0$ 分磁化量做 SVD，再对所有分块权重全局排序，只保留合计最多 chi 个。矩形 SVD 用完整向量基补足零权重态。每个算符都用同一 T 更新，不得只变换 H、遗漏边缘算符。discarded weight 为：

$$
\varepsilon=1-\sum_{\mathrm{kept}}\lambda_i^2.
$$

infinite 生长缓存不同长度的左右块。finite 每轮从中点到右端，再到左端，再回中点；沿增长方向更新块。至少两轮且中点能量变化小于 $10^{-9}$ 时停止；必做和长链上限为 12 轮，二聚化扫描上限为 20 轮。所有主运行均达到该阈值。能量是当前优化态截断前的值；权重是更新块时的局部截断损失。截断后的局部能量不保证处处单调。

## 验证策略

1. 以独立比特 ED 核对未截断超块；将每个生长态和整轮扫描态恢复为物理态，再用原始 ED H 测量能量。小系统测试还覆盖扫描全部局部位置。
2. 用独立局域 2×2 张量作用核对 ED H，含 N=20 精确参照；用两格点解析全谱和 MG 解析解检查物理因子、J2 及边界。
3. 对每次截断核对全局维数、等距性、电荷守恒，以及直接投影范数损失和权重和的一致性。
4. 用约化密度矩阵与 SVD 两种路径核对熵；用稳定残差范数平方和直接相减核对方差。
5. 故意去掉 J2、改变 J2 符号、增加周期键和破坏第二套边缘算符，确认独立检查能失败。MG 能量对某些周期错误不敏感，因此使用一般测试向量补检。
6. 长链从等距矩阵恢复物理 MPS，用独立的自旋算符逐键收缩并重组能量。以不对称随机态、任意虚拟基变换和 40 格点解析二聚体测试该测量流程。
7. 二聚化扫描采用 N=20、chi=64，并逐点与 ED 的全部键对照；N=12/16 的精确结果提供尺寸比较，两条中心键另以局域张量作用校验。

开发中已修正对照实验全局 SVD 在简并截断时混合磁化的问题，并增加全部指定 m 值的回归测试。低 chi 扫描次数不足的问题已通过增加上限解决。完整校检清单在 output/validation.md，辅助求解器残差、厄米性不能代替独立校检。

## 报告与数值口径

报告按五项必做、小系统和 MG 校检、选做 1 至 4、源码说明的顺序组织。单次截断实验只投影左半链，再归一化、用原 H 测量，不额外优化。纠缠熵用自然对数。收敛表同时报告最后一轮最大丢弃权重和中点丢弃权重。直接计算的方差有浮点相消，稳定的残差范数结果也一并保留。1/chi 线性外推并未改善精度，报告中如实分析了原因。

长链取 N=40/60、chi=32/64，比较有限开链能量密度与题给无限链值，区分边界/尺寸效应和截断变化。二聚化取 J2=0,0.1,...,1.0，定义 $D_N=|C_{N/2-2}-C_{N/2-1}|$；开边界即使在 J2=0 也有键交替，有限尺寸结果不能直接确定临界点或证明热力学非零序参量。

选做 2 额外用最后完整 sweep 最大 discarded weight 拟合能量误差，报告幂指数、误差/权重比值、口径敏感性及 epsilon 外推的真实精度；近似正比不当作严格保证。选做 4 引用原始研究给出已知相图，再以 $\Delta D_N(J_2)=D_N(J_2)-D_N(0)$ 展示相对增强；这不能去除所有依赖耦合的边界效应，不能作为新的相变判据。文献链接与具体结论对应地列在结果文档和 PDF 中。
