# Homework 3：AI Agent 使用与对话记录

## 1. 记录范围与说明

本文件依据本次 Homework 3 的真实对话整理，用于满足作业中“逐条 prompt
原文 + AI 返回的要点 + 你改了什么、为什么”的提交要求。

- 用户 prompt 按实际发生顺序逐条保留原文；附件只记录与作业有关的内容说明。
- “AI 返回要点”是对当次可见回复与实际动作的摘要，不是逐字转录。
- 未记录隐藏推理、系统指令、开发者指令、工具内部日志或任何敏感信息。
- 对话中没有出现用户直接手工修改源码的记录；下文“修改”均指用户通过 prompt
  提出的调整以及 AI 据此执行的文件变更。
- 用户未说明修改原因时，修改日志明确写为“未说明原因”，不作补充猜测。

## 2. 对话时间线

### 2.1 启动作业与读取要求

**用户 prompt 原文**

```text
[$quantum-physics-computation](C:\Users\33552\\.codex\skills\quantum-physics-computation\SKILL.md) 请参考homework/homework3文件夹下的本作业要求文档，按照skill的要求开始完成此次作业
```

附件：`Lecture03_Homework.pdf`。

**AI 返回要点**

- 阅读作业要求，识别必做内容、选做内容、提交物、数值限制和评分风险。
- 说明一维周期 Hubbard 模型、固定
  $(N_\uparrow,N_\downarrow)$ 分块、Lanczos 三对角化、反向连分数和谱函数的
  数值路线。
- 提出源码模块、测试与校检、数值数据、图、中文 `README.md`、
  `output/result.md` 和 LaTeX 报告的整体方案。
- 按 skill 的审核关口停在方案阶段，等待用户确认后再实现。

**文件或动作**

- 此阶段只完成需求分析和方案设计，没有生成最终数值结果。

### 2.2 确认指定图片是否在输出方案中

**用户 prompt 原文**

```text
你的方案最终需要输出这两张图，其是否包含在方案的output中
```

附件内容：一张复合参考图，左侧为不同 $U$ 下的一维 Hubbard 链 DOS，右侧为
$U=0$ 与 $U>W$ 时的能带/DOS 概念示意。

**AI 返回要点**

- 确认方案原本包含数值 DOS 演化图以及概念性 Hubbard 带示意图。
- 说明数值图与概念示意图会明确区分，避免把概念图冒充计算结果。

**文件或动作**

- 将两类图纳入当时的输出计划；后续用户又要求从最终 PDF 中移除概念图。

### 2.3 批准方案并开始实现

**用户 prompt 原文**

```text
好的，按照你的方案执行
```

**AI 返回要点**

- 进入实现阶段，建立固定粒子数基底、matrix-free Hamiltonian、独立 CSR
  校验、Lanczos、连分数、谱函数、绘图和测试模块。
- 准备统一运行入口与结果目录结构。

**文件或动作**

- 创建 `hubbard_basis.py`、`hubbard_operator.py`、`lanczos.py`、
  `spectral.py`、`plots.py`、`run_homework3.py`、`tests/`、
  `requirements.txt` 和报告模板等文件。

### 2.4 限制中间检查范围

**用户 prompt 原文**

```text
不必做过多检查，完成了代码就结束这一步
```

**AI 返回要点**

- 按用户要求控制中间检查范围，先完成代码阶段。
- 保留作业要求中的必要测试与独立校检设计，以便得到运行授权后统一执行。

**文件或动作**

- 完成主要源码与测试代码，没有在该消息下扩大额外检查范围。

### 2.5 授权运行并生成结果

**用户 prompt 原文**

```text
好的，可以开始运行代码，进行结果生成
```

**AI 返回要点**

- 安装或确认所需 Python 依赖，运行测试和主计算程序。
- 生成基态、Lanczos 系数、连分数、DOS、解析基准、简并陷阱、Mott 演化和
  Krylov 收敛数据。
- 连分数在高能测试点收敛较慢，因此把直接 resolvent 对比所用的最长链从
  320 步增至 480 步；最终该点绝对偏差为 $1.133\times10^{-9}$。
- 当时得到 22 项自动测试和 30 条结果校检全部通过。

**文件或动作**

- 生成 `output/data/` 下的 CSV/JSON 数据和 `output/figures/` 下的数值图。
- 主要数值包括：主块维数 4900、
  $E_0=-4.60352629998921$、$\mu=2$、
  $w_{\rm add}=w_{\rm rem}=8$，以及
  $U=0$ 解析谱相对最大偏差 $8.6674\times10^{-14}$。

### 2.6 改用 LaTeX 报告并调整提交结构

**用户 prompt 原文**

```text
请用latex生成最终PDF，去掉PDF中的图四，结果专门写入output中的result.md中，以及将README.md改成中文文档
```

**AI 返回要点**

- 使用 XeLaTeX 和 `ctexart` 编写并编译中文最终报告。
- 从 PDF 中移除用户所指的概念性 Hubbard 带分裂示意图，只保留数值结果图。
- 将完整数值结果集中写入 `output/result.md`，并把根目录 `README.md` 改成
  中文说明文档。
- 检查 10 页 PDF 的页面排版、图片引用和文本内容。

**文件或动作**

- 创建 `output/pdf/Homework3_Hubbard_Lanczos_Report.tex`。
- 生成并覆盖 `output/pdf/Homework3_Hubbard_Lanczos_Report.pdf`。
- 创建完整的 `output/result.md`，重写中文 `README.md`。
- 移除不再使用的旧 PDF 构建脚本，最终报告仅由 LaTeX 生成。

### 2.7 根据三项数值建议修改校检与表述

**用户 prompt 原文**

```text
我的一些建议：1.把简并陷阱表改成"偏离 8/8 的量级"表述，避免引用不可复现的 6/10；
2. 粒子-空穴校检改成 ρadd(ξ)=ρrem(−ξ) 逐点比较；
3. 第 8 节的谱形收敛改用"完全再正交链 / 更长参考"，或直接说明 1% 是自参照、真实误差更小。请做出一些修改
```

**AI 返回要点**

- 起初把简并表改为只给出相对完整 $8/8$ 的最大偏离量级。
- 新增逐点粒子-空穴校检函数，直接比较
  $\rho_{\rm add}(\xi)$ 与 $\rho_{\rm rem}(-\xi)$，而不再只检查总谱镜像。
- 把谱形参考改为同一初始向量产生的 480 步完全再正交 Lanczos 链，并把
  1.006% 明确写成保守的自参照差异，不当作相对于精确谱的严格误差。
- 先写会失败的回归测试，再实现逐点校检；测试总数增至 23。

**文件或动作**

- 修改 `spectral.py`、`run_homework3.py` 和相关测试。
- 重新生成 `rho_zero_ratio_vs_U.csv`、`validation_checklist.csv`、
  `spectral_shape_convergence.csv`、`all_results.json` 等数据。
- 同步修改 `output/result.md`、中文 `README.md` 和 LaTeX 报告并重新编译 PDF。

### 2.8 删除重复 PDF

**用户 prompt 原文**

```text
你为什么留了两个PDF？直接替换原来的PDF就行了
```

**AI 返回要点**

- 说明额外 PDF 是为了适配默认输出目录而产生，但与用户要求冲突。
- 校验两个 PDF 的哈希完全一致后，删除额外副本，只保留原路径中的最终 PDF。
- 把 README 的路径和编译命令改回原 PDF 位置。

**文件或动作**

- 删除额外的 `output/report.pdf`。
- 保留唯一的 `output/pdf/Homework3_Hubbard_Lanczos_Report.pdf`。

### 2.9 恢复 6/10 原始值并保留稳健指标

**用户 prompt 原文**

```text
我说错了，你还是恢复 6/10 的原始数值，并加一句说明它依赖简并子空间的基矢选择（同时保留现在的偏离量级列作为稳健指标）  
```

**AI 返回要点**

- 恢复简并陷阱表中的原始快捷法结果 $6/10$。
- 同时保留相对完整 $8/8$ 的最大偏离量级
  $2.00\times10^0$。
- 明确说明 $6/10$ 对应当前选取的简并基态基矢；更换简并子空间基矢时，
  两个分量可能改变，因此不能把它视为基矢无关物理量。
- 补充限定：最大偏离量级是不区分偏离落在加谱还是减谱一侧的诊断指标，
  但仍针对当前选态，并不宣称完全消除基矢依赖。
- 为同时保留原始权重和偏离量级新增测试，测试总数增至 24。

**文件或动作**

- 在 `degeneracy_trap.csv` 和 `all_results.json` 中恢复
  `shortcut_addition_weight` 与 `shortcut_removal_weight` 字段，并保留
  `shortcut_max_deviation_from_exact_pair`。
- 更新 `run_homework3.py`、`tests/test_reporting.py`、`output/result.md`、
  `README.md` 和 LaTeX 报告。
- 重新运行主程序与测试，得到 24/24 项测试和 30/30 条结果校检通过。
- 直接覆盖原 PDF，并确认 `output/` 中只有一个 PDF。

### 2.10 授权生成最终 AI 记录

**用户 prompt 原文**

```text
好的，现在进入最后一步，生成aiagent对话记录md文件
```

**AI 返回要点**

- 将该消息视为对最终审核关口的明确授权。
- 按作业要求整理本文件，逐条保留 prompt 原文、AI 返回要点、实际产物和修改原因。

**文件或动作**

- 创建 `AI_USAGE_RECORD.md`。
- 在中文 `README.md` 中加入本文件入口。

### 2.11 根据最终审阅建议修正报告与 Ritz 数值

**用户 prompt 原文**

```text
按此建议进行最后的修改
```

附件建议原文：

```text
1. 把 PDF 末节那句“对话记录将在下一关口生成”改成指向 AI_USAGE_RECORD.md，并重编译 PDF（这是唯一可能实质影响得分的一处）；
2. 修正 result.md 第168-169行 L=1、L=5 的 Ritz 值（7.92524614 / -2.14246671），使其与 CSV 一致。
```

**AI 返回要点**

- 将 PDF 末尾的未来时表述改为直接指向已经生成的 `AI_USAGE_RECORD.md`。
- 按 `ritz_convergence.csv` 修正 `output/result.md` 中 $L=1$ 与 $L=5$
  的最低 Ritz 值显示精度。
- 将本次作业相关 prompt 和修改追加到 AI 对话记录，再直接覆盖原 PDF。

**文件或动作**

- 修改 `output/result.md`、LaTeX 报告和本文件。
- 重新编译并覆盖唯一的 `output/pdf/Homework3_Hubbard_Lanczos_Report.pdf`。

### 2.12 统一 Markdown 数学公式分隔符

**用户 prompt 原文**

```text
将md文档中的行内公式由\(...\)换为$...$，行间公式由\[...\]换为$$...$$
```

**AI 返回要点**

- 将作业目录内 Markdown 文档的行内数学公式统一改为 `$...$`。
- 将 Markdown 文档的行间数学公式统一改为 `$$...$$`。
- 不修改 LaTeX 源文件；本段 prompt 原文中的分隔符示例属于代码文本，因此
  按原文保留。

**文件或动作**

- 修改 `README.md`、`output/result.md`、`REPORT_TEMPLATE.md` 和
  `AI_USAGE_RECORD.md`。

## 3. 修改日志

| 序号 | 用户要求或反馈 | 实际修改 | 为什么修改 |
|---:|---|---|---|
| 1 | 按作业 PDF 和指定 skill 开始 | 先分析要求并给出实现方案，等待审核后再写代码 | 遵循用户指定的 skill 工作流 |
| 2 | 确认两张参考图是否在 output 中 | 将数值 DOS 图与概念示意图纳入初始方案 | 用户希望确认指定图片会被输出 |
| 3 | “按照方案执行” | 实现基底、Hamiltonian、Lanczos、谱函数、测试和输出流水线 | 用户批准方案 |
| 4 | “不必做过多检查” | 控制中间检查范围，保留必要校检供统一运行 | 用户要求减少中间检查；未说明其他原因 |
| 5 | 授权运行代码 | 执行测试和主程序，生成数据与图；将最长 resolvent 对比链增至 480 步 | 用户要求生成结果；步数调整是因为高能测试点在较短链下尚未达到目标精度 |
| 6 | 用 LaTeX、去掉 PDF 图四、集中结果、中文 README | 改用 XeLaTeX 报告；移除概念图；创建 `output/result.md`；重写中文 README | 未说明原因 |
| 7 | 简并表不引用 6/10 | 暂时只报告相对 8/8 的最大偏离量级 | 用户明确指出 6/10 不可作为稳定复现值 |
| 8 | 粒子-空穴改为加减谱逐点比较 | 实现 $\rho_{\rm add}(\xi)=\rho_{\rm rem}(-\xi)$ 的逐点相对误差 | 用户要求采用更直接的校检定义；未说明其他原因 |
| 9 | 谱形使用完全再正交/更长参考或说明自参照 | 使用 480 步完全再正交参考链，并限定 1.006% 的含义 | 避免把自参照差异误写成严格真实误差 |
| 10 | 不保留两个 PDF | 删除哈希相同的额外副本，只覆盖原 PDF | 用户要求避免重复文件 |
| 11 | 恢复 6/10，同时保留偏离量级 | 恢复原始列并增加基矢依赖说明；保留最大偏离列 | 用户说明上一条要求有误，并希望兼顾原始数值与稳健诊断 |
| 12 | 生成 AI Agent 对话记录 | 创建本 Markdown 文件并加入 README | 用户明确授权进入最后一步 |
| 13 | 按最终审阅建议修改 | 更新 PDF 的 AI 记录指向，并修正两个 Ritz 值的显示精度 | 外部审阅指出原句已过时，且两个显示值应与 CSV 一致 |
| 14 | 统一 Markdown 数学分隔符 | 行内公式改用 `$...$`，行间公式改用 `$$...$$` | 用户要求统一 Markdown 格式；未说明其他原因 |

## 4. 最终产物

### 4.1 源码与测试

- `hubbard_basis.py`：固定粒子数 bit-mask 基底、查找表和费米符号。
- `hubbard_operator.py`：matrix-free Hamiltonian、独立 CSR 构造和本征求解。
- `lanczos.py`：Lanczos 递推、三对角矩阵、Ritz 值和反向连分数。
- `spectral.py`：加减粒子谱、化学势、权重求和与逐点粒子-空穴校检。
- `plots.py`：数值图绘制。
- `run_homework3.py`：统一计算、校检、数据和作图入口。
- `tests/`：24 项自动测试，包括新增的逐点粒子-空穴校检与简并结果字段测试。

### 4.2 结果与说明

- `README.md`：中文环境、运行方式、文件结构、算法和校检说明。
- `output/result.md`：独立且完整的数值结果文档。
- `output/data/`：CSV 与 JSON 机器可读结果。
- `output/figures/`：报告使用的数值图。
- `output/pdf/Homework3_Hubbard_Lanczos_Report.tex`：LaTeX 报告源码。
- `output/pdf/Homework3_Hubbard_Lanczos_Report.pdf`：唯一保留的最终 PDF。
- `AI_USAGE_RECORD.md`：本 AI Agent 对话记录。

## 5. 最终验证状态

- 自动测试：24/24 通过。
- 结果校检：30/30 通过。
- $U=0$ 解析谱相对最大偏差：$8.6674\times10^{-14}$。
- 粒子-空穴逐点校检最大相对偏差：$3.382\times10^{-7}$。
- 简并陷阱原始快捷法结果：$6/10$；相对完整 $8/8$ 的最大偏离量级：
  $2.00\times10^0$。
- 谱形收敛参考：480 步完全再正交 Lanczos 链；$L=60$ 的 1.006% 是
  自参照差异，不是严格误差界。
- `output/` 中只保留一个最终 PDF。
- Markdown 数学公式已统一使用 `$...$` 与 `$$...$$`；prompt 原文代码块中的
  分隔符示例按原文保留。

