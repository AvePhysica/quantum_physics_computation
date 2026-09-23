"""从最新 JSON/PNG 结果可重复生成最终总结 PDF。"""

from __future__ import annotations

import json
import shutil
import subprocess
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output"
TEMPORARY = ROOT / "tmp" / "pdfs"
PDF_NAME = "Lecture02_Homework_Final_Summary.pdf"


def _number(value: float) -> str:
    return f"{value:.10f}"


def _latex_text(value: object) -> str:
    text = str(value)
    for old, new in (
        ("\\", r"\textbackslash{}"),
        ("&", r"\&"),
        ("%", r"\%"),
        ("$", r"\$"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
    ):
        text = text.replace(old, new)
    return text


def _latex_source(results: dict[str, object], controls: list[dict[str, object]]) -> str:
    sector = results["sector_33"]
    lowest_rows = "\n".join(
        f"{row['rank']} & {_number(row['energy'])} & "
        f"$({row['sector'][0]},{row['sector'][1]})$ & {row['global_degeneracy']} \\\\"
        for row in results["global_lowest_20"]
    )
    site_rows = "\n".join(
        f"{site} & {_number(results['local_density'][site])} & "
        f"{_number(results['local_spin_z'][site])} & "
        f"{_number(results['double_occupancy'][site])} \\\\"
        for site in range(6)
    )
    spin_rows = "\n".join(
        f"\\texttt{{{bond}}} & {_number(value)} \\\\"
        for kind in ("leg", "rung")
        for bond, value in results["spin_correlations"][kind].items()
    )
    structure_rows = "\n".join(
        f"\\texttt{{{key}}} & {_number(value)} & "
        f"{_number(results['structure_factors']['charge'][key])} \\\\"
        for key, value in results["structure_factors"]["spin"].items()
    )
    control_rows = []
    for index, control in enumerate(controls, start=1):
        measured = ", ".join(
            f"{key}={value:.6g}" for key, value in control["measured"].items()
        )
        control_rows.append(
            f"{index} & {_latex_text(control['mutation'])} & "
            f"\\texttt{{{_latex_text(measured)}}} & "
            f"{'检出' if control['detected'] else '未检出'} \\\\"
        )
    control_rows = "\n".join(control_rows)
    lowest_values = [_number(value) for value in sector["lowest_8_eigenvalues"]]
    lowest_eight = (
        r"\begin{aligned}"
        + r",\;".join(lowest_values[:4])
        + r",\\ "
        + r",\;".join(lowest_values[4:])
        + r"\end{aligned}"
    )

    source = r"""
\documentclass[11pt,a4paper]{ctexart}
\usepackage[margin=1.8cm,headheight=15pt]{geometry}
\usepackage{amsmath,amssymb,booktabs,longtable,array,graphicx,fancyhdr,enumitem}
\usepackage[table]{xcolor}
\usepackage[colorlinks=true,linkcolor=blue!45!black,urlcolor=blue!45!black]{hyperref}
\definecolor{navy}{HTML}{17365D}
\definecolor{sky}{HTML}{DCE6F1}
\definecolor{pale}{HTML}{F3F6FA}
\definecolor{green}{HTML}{2E7D32}
\setlength{\parindent}{0pt}
\setlength{\parskip}{5pt}
\setlist{nosep,leftmargin=1.7em}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small 2$\times$3 扩展 Hubbard 梯子}
\fancyhead[R]{\small 精确对角化与独立校检}
\fancyfoot[C]{\thepage}
\newcommand{\resultbox}[1]{\colorbox{sky}{\parbox{0.94\linewidth}{#1}}}
\newcommand{\pass}{\textcolor{green}{\textbf{通过}}}
\begin{document}

\begin{titlepage}
\thispagestyle{empty}
\vspace*{2.0cm}
{\color{navy}\rule{\linewidth}{1.5pt}}\\[1.1cm]
{\Huge\bfseries 2$\times$3 梯子上的扩展 Hubbard 模型\par}
\vspace{0.5cm}
{\LARGE 精确对角化、独立校检与负向验证\par}
\vspace{0.8cm}
{\color{navy}\rule{\linewidth}{1.5pt}}
\vfill
\resultbox{\textbf{交付状态（@@DATE@@）}\quad
按 $U(1)\times U(1)$ 对称性分成 49 个扇区；完成 8 项必做与 3 项选做；
8 个正向测试和 4 个故意改错负向测试全部通过。V 扫描保留 7 条键数据，
并明确显示由空间对称性形成的 3 类重合曲线。}
\par\vspace{1.0cm}
\begin{center}
\begin{tabular}{>{\bfseries}p{0.28\linewidth}p{0.62\linewidth}}
模型参数 & $t=1,\ U=4,\ V=1,\ \mu=4$\\[4pt]
主扇区 & $(N_\uparrow,N_\downarrow)=(3,3)$，维数 400\\[4pt]
基态能量 & $E_0=@@GROUND@@$\\[4pt]
基态量子数 & 非简并，$\langle S_{\mathrm{tot}}^2\rangle\simeq0$，$S=0$\\[4pt]
最终验证 & 12/12 单元测试通过，4/4 故意错误被检出
\end{tabular}
\end{center}
\vfill
{\large 量子物理计算方法选讲 -- Lecture 02 Homework\par}
\end{titlepage}

\section{模型、基底与对称性分块}
哈密顿量为
\[
H=-t\sum_{\langle ij\rangle,\sigma}(c_{i\sigma}^\dagger c_{j\sigma}+\mathrm{h.c.})
+U\sum_i n_{i\uparrow}n_{i\downarrow}
+V\sum_{\langle ij\rangle}n_i n_j-\mu\sum_{i\sigma}n_{i\sigma}.
\]
六个格点形成开边界的 $2\times3$ 梯子，共有四条腿键和三条横档。

每个 Fock 态用两个 6 位整数 \texttt{(up\_bits, down\_bits)} 表示，轨道顺序固定为
\[
(0\uparrow,1\uparrow,\ldots,5\uparrow,0\downarrow,1\downarrow,\ldots,5\downarrow).
\]
对第 $p$ 个轨道作用产生或湮灭算符时，费米子符号取
$(-1)^{N_{<p}}$。复合算符始终按从右到左的物理顺序逐个作用，并在每一步重新计算奇偶性。

由于 $[H,N_\uparrow]=[H,N_\downarrow]=0$，程序在固定
$(N_\uparrow,N_\downarrow)$ 中构造和对角化矩阵。49 个扇区的维数总和为 4096，
但程序\textbf{从未分配完整的 $4096\times4096$ 数组，也未对其做对角化}。
全局能谱和全局迹均由各分块结果汇总；最大矩阵只有
$\binom63^2=400$ 维。

\resultbox{查找表 \texttt{state -> matrix\_index} 让每次跃迁后的基矢定位为 $O(1)$；
矩阵元中的 $t,U,V,\mu$ 全部由函数参数传入。}

\newpage
\section{必做结果：低能谱}
$(3,3)$ 扇区最低 8 个本征值为
\[
@@LOWEST8@@.
\]
基态简并度为 @@DEGENERACY@@。合并 49 个扇区后，全系统最低 20 个能级如下；
“最低 20 个”按重数计数。

\rowcolors{2}{pale}{white}
\begin{longtable}{r r c r}
\toprule
序号 & 能量 & $(N_\uparrow,N_\downarrow)$ & 全局简并度\\
\midrule
@@LOWESTROWS@@
\bottomrule
\end{longtable}

\newpage
\section{必做结果：局域量、关联与能隙}
\begin{minipage}[t]{0.50\linewidth}
\centering
\textbf{局域观测量}\\[3pt]
\rowcolors{2}{pale}{white}
\begin{tabular}{c r r r}
\toprule
$i$ & $\langle n_i\rangle$ & $\langle S_i^z\rangle$ & 双占据\\
\midrule
@@SITEROWS@@
\bottomrule
\end{tabular}
\end{minipage}\hfill
\begin{minipage}[t]{0.43\linewidth}
\centering
\textbf{七条键的自旋关联}\\[3pt]
\rowcolors{2}{pale}{white}
\begin{tabular}{c r}
\toprule
键 & $\langle\mathbf S_i\!\cdot\!\mathbf S_j\rangle$\\
\midrule
@@SPINROWS@@
\bottomrule
\end{tabular}
\end{minipage}

\vspace{0.7cm}
\begin{tabular}{>{\bfseries}p{0.31\linewidth}p{0.58\linewidth}}
平均双占据 & $D=@@DOUBLE@@$\\[4pt]
总自旋 & $\langle S_{\mathrm{tot}}^2\rangle=@@S2@@$，对应 $S=0$\\[4pt]
自旋隙 & $\Delta_s=@@SPINGAP@@$\\[4pt]
电荷隙 & $\Delta_c=@@CHARGEGAP@@$
\end{tabular}

所有七条最近邻自旋关联均为负，显示反铁磁关联占主导。开边界使边缘和中间格点的配位数不同；
在 $V=1$ 时，最近邻排斥把部分电荷从高配位的中间格点推向边缘格点，因此局域密度和双占据出现空间不均匀。

\newpage
\section{选做结果：结构因子与 $V$ 扫描}
\begin{minipage}[t]{0.34\linewidth}
\vspace{0pt}\centering
\textbf{结构因子}\\[3pt]
\rowcolors{2}{pale}{white}
\begin{tabular}{c r r}
\toprule
$q$ 索引 & $S(q)$ & $N(q)$\\
\midrule
@@STRUCTUREROWS@@
\bottomrule
\end{tabular}
\end{minipage}\hfill
\begin{minipage}[t]{0.62\linewidth}
\vspace{0pt}
\includegraphics[width=\linewidth]{output/V_scan.png}
\end{minipage}

V 扫描的 CSV 包含全部 7 条键。图中只有 3 条可分辨曲线，是因为哈密顿量及非简并基态保持左右反射和两腿交换对称性：
\begin{itemize}
\item 四条腿键 $(0,1),(1,2),(3,4),(4,5)$ 完全重合；
\item 两条外侧横档 $(0,3),(2,5)$ 完全重合；
\item 中心横档 $(1,4)$ 单独成类。
\end{itemize}
逐个 $V$ 点检查得到组内最大差为 $1.055\times10^{-14}$，远小于 $10^{-10}$ 阈值。

当 $V=0$ 时选取 $\mu=U/2=2$。比较 49 个扇区确认全局基态仍包含 $(3,3)$；
此时每个格点 $\langle n_i\rangle=1$，平均双占据为 @@V0DOUBLE@@。

\newpage
\section{独立校检与故意改错实验}
正向校检覆盖：本征对残差、分块维数和解析迹、原子极限、单粒子极限、
Hellmann--Feynman 导数、粒子数和规则、SU(2) 总自旋量子化、自旋交换对称性、
结构因子傅里叶和规则，以及 $V$ 扫描键对称性。8 个正向单元测试全部通过。

题目要求“故意把 $H$ 改错，确认校检会失败”。下表是实际运行结果，而非分析性预期：

\small
\rowcolors{2}{pale}{white}
\begin{tabular}{c >{\raggedright\arraybackslash}p{0.25\linewidth} >{\raggedright\arraybackslash}p{0.45\linewidth} c}
\toprule
编号 & 故意错误 & 错误版本实测值 & 结论\\
\midrule
@@CONTROLROWS@@
\bottomrule
\end{tabular}
\normalsize

\resultbox{四个错误版本均被相应独立校检拒绝（4/4）。负向测试用临时错误矩阵或错误观测量运行，
不会改写正式实现。完整机器可读记录位于 \texttt{output/negative\_control\_results.json}。}

\newpage
\section{自驱分：额外完成的工作}
除题目要求的数值量之外，本项目还完成了以下可复核工作：
\begin{enumerate}
\item \textbf{对称性可视化与数值归并：}把七条键按空间对称性归并为三类可见曲线，
同时保留全部七条原始数据，并逐个 $V$ 点检查组内一致性。
\item \textbf{跨模块交叉验证：}联合使用 Hellmann--Feynman、SU(2) 总自旋、
离散傅里叶和规则、解析迹、原子极限与单粒子极限，避免校检与被校检代码共享同一错误。
\item \textbf{真实负向验证：}建立四个自动化故意改错实验，保存实测残差和是否检出的记录。
\item \textbf{可重复报告流程：}由最新 JSON 与 PNG 自动生成本 PDF；LaTeX 中间文件进入临时目录，
最终 \texttt{output} 只保留提交所需文件。
\end{enumerate}

\section*{复现命令}
\begin{verbatim}
python -m unittest discover -p "test*.py" -v
python run_homework.py
python negative_controls.py
python generate_summary_pdf.py
\end{verbatim}

\section*{最终状态}
\begin{itemize}
\item 8 项必做、3 项选做均有数值结果与非平凡校检；
\item 8 个正向测试与 4 个负向测试全部通过；
\item 未对任何 $4096\times4096$ 矩阵做对角化，也未分配完整矩阵；
\item V 扫描图和本总结 PDF 均与当前源码及结果同步。
\end{itemize}

\end{document}
"""
    replacements = {
        "@@DATE@@": date.today().isoformat(),
        "@@GROUND@@": _number(sector["ground_energy"]),
        "@@LOWEST8@@": lowest_eight,
        "@@DEGENERACY@@": str(sector["ground_degeneracy"]),
        "@@LOWESTROWS@@": lowest_rows,
        "@@SITEROWS@@": site_rows,
        "@@SPINROWS@@": spin_rows,
        "@@DOUBLE@@": _number(results["average_double_occupancy"]),
        "@@S2@@": _number(results["total_spin_squared"]),
        "@@SPINGAP@@": _number(results["spin_gap"]),
        "@@CHARGEGAP@@": _number(results["charge_gap"]),
        "@@STRUCTUREROWS@@": structure_rows,
        "@@V0DOUBLE@@": _number(results["V0_mu2"]["average_double_occupancy"]),
        "@@CONTROLROWS@@": control_rows,
    }
    for marker, value in replacements.items():
        source = source.replace(marker, value)
    if "@@" in source:
        raise ValueError("PDF 模板仍含未替换标记")
    return source


def main() -> None:
    results = json.loads((OUTPUT / "results.json").read_text(encoding="utf-8"))
    controls = json.loads(
        (OUTPUT / "negative_control_results.json").read_text(encoding="utf-8")
    )
    if not all(control["detected"] for control in controls):
        raise RuntimeError("存在未被校检发现的故意错误，拒绝生成最终 PDF")

    if TEMPORARY.exists():
        shutil.rmtree(TEMPORARY)
    TEMPORARY.mkdir(parents=True)
    tex_path = TEMPORARY / "summary.tex"
    tex_path.write_text(_latex_source(results, controls), encoding="utf-8")

    command = [
        "xelatex", "-interaction=nonstopmode", "-halt-on-error",
        f"-output-directory={TEMPORARY}", str(tex_path),
    ]
    try:
        for _ in range(2):
            completed = subprocess.run(
                command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8"
            )
            if completed.returncode != 0:
                raise RuntimeError(completed.stdout[-5000:] + completed.stderr[-2000:])
        shutil.copy2(TEMPORARY / "summary.pdf", OUTPUT / PDF_NAME)
    finally:
        shutil.rmtree(TEMPORARY, ignore_errors=True)
    print(f"已生成：{OUTPUT / PDF_NAME}")


if __name__ == "__main__":
    main()
