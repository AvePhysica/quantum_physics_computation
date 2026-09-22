# Lecture 02 Homework Implementation Plan

**Goal:** 用粒子数守恒分块精确对角化 2x3 扩展 Hubbard 梯子，完成全部必做与选做结果，并给出独立校检。

**Architecture:** `hubbard_model.py` 负责比特基底、费米子符号与分块哈密顿量；`observables.py` 负责期望值和关联函数；`run_homework.py` 组合 49 个分块、输出结果并绘图；`test_homework.py` 用解析极限、和规则和有限差分校检实现。

**Tech Stack:** Python 3、NumPy、SciPy、Matplotlib、标准库 unittest。

---

- [x] 建立固定 `(N_up, N_down)` 的比特基底与查找表。
- [x] 实现带正确费米子符号的跃迁和参数化分块哈密顿量。
- [x] 用解析维数、厄米性、解析迹和非相互作用极限校检模型。
- [x] 实现局域密度、自旋、双占据、键关联、总自旋平方和结构因子。
- [x] 用粒子数和规则、自旋和规则、Hellmann-Feynman 有限差分校检观测量。
- [x] 计算 8 项必做结果以及 3 项选做结果。
- [x] 生成 `results.md`、`results.json`、`V_scan.csv` 和 `V_scan.png`。
- [x] 编写 `README.md`，说明原理、代码、结果、校检、物理讨论和 AI 使用记录。
- [x] 从干净进程运行测试和主程序，核对所有生成文件。
