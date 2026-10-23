"""Review-requested measured additions; same content feeds Markdown and LaTeX."""
import csv
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
def e(x): return f'{x:.12f}'
def s(x): return f'{x:.4e}'


def figures(d,save):
    analysis=d['review_analysis']; scaling=analysis['error_scaling']; rows=scaling['inputs']
    fit=scaling['fits']['eps_max']
    x=np.array([r['eps_max'] for r in rows]); y=np.array([r['error'] for r in rows])
    grid=np.geomspace(x.min()/1.5,x.max()*1.5,200)
    fig,axs=plt.subplots(1,2,figsize=(9,3.7))
    axs[0].loglog(x,y,'o',label='Measured, last-sweep max epsilon')
    axs[0].loglog(grid,fit['amplitude']*grid**fit['power'],'-',label=f'Power fit: p={fit["power"]:.3f}')
    axs[0].loglog(grid,fit['origin_slope']*grid,'--',label='Proportional fit: p=1')
    for r in rows: axs[0].annotate(f'chi={r["chi"]}',(r['eps_max'],r['error']),xytext=(3,5),textcoords='offset points',fontsize=7)
    axs[0].set(xlabel='Discarded weight epsilon (max)',ylabel='Absolute total-energy error',title='Approximate first-order error scaling')
    axs[0].legend(fontsize=7); axs[0].grid(alpha=.2)
    axs[1].semilogx(x,y/x,'o-',label='Last-sweep maximum')
    xc=np.array([r['eps_centre'] for r in rows])
    axs[1].semilogx(xc,y/xc,'s--',label='Centre-cut weight')
    axs[1].set(xlabel='Discarded weight epsilon',ylabel='Error / epsilon',title='Coefficient and epsilon convention are not universal')
    axs[1].legend(fontsize=7); axs[1].grid(alpha=.2)
    save(fig,'error_epsilon')
    baselines=analysis['baselines']; gc=analysis['phase_reference']['critical_ratio_approx']
    fig,axs=plt.subplots(1,2,figsize=(9,3.7))
    for n in (12,16,20):
        rows=[r for r in baselines if r['method']=='ED' and r['n']==n]
        for ax,field in zip(axs,('dimer','enhancement')):
            ax.plot([r['j2'] for r in rows],[r[field] for r in rows],'o-',ms=3,label=f'ED N={n}')
    rows=[r for r in baselines if r['method']=='DMRG']
    for ax,field in zip(axs,('dimer','enhancement')):
        ax.plot([r['j2'] for r in rows],[r[field] for r in rows],'kx',ms=6,label='DMRG N=20')
        ax.axvline(gc,ls='--',color='grey',lw=1,label='Literature gc ~ 0.2411')
        ax.set_xlabel('J2 / J1'); ax.grid(alpha=.2)
    axs[0].set(ylabel='D(N, J2)',title='Raw finite-chain bond alternation')
    axs[1].axhline(0,color='black',lw=.7)
    axs[1].set(ylabel='D(N, J2) - D(N, 0)',title='Same-size baseline subtraction')
    axs[0].legend(fontsize=7); save(fig,'dimer_baseline')


def append_scaling(doc,d):
    scaling=d['review_analysis']['error_scaling']; rows=scaling['inputs']; fits=scaling['fits']; fit=fits['eps_max']
    doc.sub('能量误差与丢弃权重的定量关系')
    doc.cited_p(r'充分扫描后，可以用丢弃权重而非 $1/\chi$ 作为能量外推的横坐标；近似正比关系需要在具体系统中检查，不能预先当作定律。White 对截断权重外推的讨论也强调环境基不完整可能低估实际截断误差，以及必须核查线性。',
                [('White（2005），第 4 页及图 4','https://arxiv.org/abs/cond-mat/0508709')])
    doc.p(r'固定 $N=20,J_2=0$，使用与前述外推相同的 $\chi=4,8,16,32$ 四个已收敛结果；误差取总能量的 $\mathrm{err}=|E-E_0|$，主分析中 $\varepsilon$ 为最后一整轮 sweep 的最大丢弃权重，不混用 warmup 或不同长度数据。')
    doc.table([r'$\chi$',r'$\mathrm{err}$',r'$\varepsilon_{\max}$',r'$\mathrm{err}/\varepsilon_{\max}$',r'$\varepsilon_{\mathrm{centre}}$'],[
        [r['chi'],s(r['error']),s(r['eps_max']),f'{r["ratio"]:.6f}',s(r['eps_centre'])] for r in rows])
    doc.p('对四个点做无权对数最小二乘拟合，每个数量级上的相对偏差具有相同权重：')
    doc.math(r'\log\mathrm{err}=p\log\varepsilon+\log A,\qquad p='+f'{fit["power"]:.6f}'+r',\quad A='+f'{fit["amplitude"]:.6f}'+r',\quad R^2_{\log}='+f'{fit["r2_log"]:.6f}'+'.')
    doc.p(r'斜率接近 1，支持该数据范围内 $\mathrm{err}$ 随 $\varepsilon$ 近似一阶下降。强制过原点拟合 $\mathrm{err}=k\varepsilon$ 得 $k='+f'{fit["origin_slope"]:.6f}'+r'$，但未加权线性拟合受大误差点主导；实测比值从 '+f'{fit["ratio_min"]:.6f}'+' 到 '+f'{fit["ratio_max"]:.6f}'+r'，说明严格正比系数并不稳定。四点拟合的高 $R^2$ 也不能作为普适标度或统计置信区间。')
    doc.table(['丢弃权重口径','幂指数 $p$',r'$R^2_{\log}$'],[
        ['最后整轮最大值',f'{fit["power"]:.6f}',f'{fit["r2_log"]:.6f}'],
        ['最终中点值',f'{fits["eps_centre"]["power"]:.6f}',f'{fits["eps_centre"]["r2_log"]:.6f}']])
    doc.p(r'口径敏感性说明单个切口的局部权重不能不加说明地代表整条链的总误差。为理解近似正比的来源，若从精确基态做一次投影并归一化，保留态与精确基态的重叠平方恰为 $1-\varepsilon$；将该态按原始哈密顿量本征态展开，有：')
    doc.math(r'E-E_0=\sum_{n>0}|c_n|^2(E_n-E_0)=\varepsilon\,\overline{\Delta E},\qquad \sum_{n>0}|c_n|^2=\varepsilon.')
    doc.p(r'只有有效激发能尺度 $\overline{\Delta E}$ 变化不大时才近似正比。实际 DMRG 经历多个切口的截断和重新优化，所报局部 $\varepsilon_{\max}$ 不等于最终态的总失真权重，因此上述单次精确投影恒等式不能直接当作本计算的严格误差公式。')
    doc.figure('error_epsilon','误差与丢弃权重的双对数拟合，以及不同权重口径下的误差/权重比值。')
    doc.p(r'再尝试四点无权线性外推 $E(\varepsilon)=E_*+a\varepsilon$。为避免大常数相消，先对有符号的 $E-E_0$ 拟合截距，再加回 $E_0$；独立的缩放设计矩阵最小二乘用于复核。')
    doc.math(r'a='+f'{fit["linear_slope"]:.6f}'+r',\qquad E_*='+e(fit['extrapolated_energy'])+'.')
    doc.table(['估计方法','能量','对 ED 的绝对误差'],[
        [r'$1/\chi$ 四点线性外推',e(d['extrapolation']['intercept']),s(d['extrapolation']['error'])],
        [r'$\varepsilon_{\max}$ 四点线性外推',e(fit['extrapolated_energy']),s(fit['extrapolated_error'])],
        [r'直接 $\chi=32$',e(rows[-1]['energy']),s(rows[-1]['error'])]])
    doc.p(r'这次用 $\varepsilon$ 外推比用 $1/\chi$ 外推更接近精确值，但仍不如直接保留 32 个态的结果。近似线性趋势可用于诊断，不能保证外推一定改善精度；截距也不受变分上界约束。')


def append_phase_baseline(doc,d):
    analysis=d['review_analysis']; baselines=analysis['baselines']; gc=analysis['phase_reference']['critical_ratio_approx']
    doc.sub('已知相图对照与同尺寸基线扣除')
    doc.cited_p(r'已知零场、各向同性的反铁磁链在 $g=J_2/J_1\lesssim g_c\simeq0.2411$ 为无隙自旋流体，相变后出现自发二聚化及自旋能隙；该转变属于 BKT 类型。$g=0.5$ 的 MG 点位于二聚化相内部，而非相界。这里的相界数值来自文献，用作对照，不是本次有限尺寸数据拟合出的结果。',
        [('White 与 Affleck（1996），第 II 节','https://arxiv.org/abs/cond-mat/9602126'),
         ('Nomura 与 Okamoto（1994）','https://doi.org/10.1088/0305-4470/27/17/012')])
    doc.table(['文献区间','热力学极限性质','本次网格的对应点'],[
        [r'$0\le g<g_c$','无隙；不具有自发二聚化','0、0.1、0.2'],
        [r'$g\approx g_c$','BKT 转变；临界附近有限尺寸困难','位于 0.2 与 0.3 之间'],
        [r'$g_c<g\le1$','有隙二聚化相','0.3 至 1.0；0.5 为精确二聚体点']])
    doc.p(r'因而本报告中有限开链在 $J_2\approx0.2$ 至 $0.5$ 的平滑增强与已知相图相容；网格上 $J_2=0.6$ 的最大交替强度不是二聚化的起点，也不是另一条相界。BKT 转变附近能隙与序参量可以很小，不能期待 $N\le20$ 的粗网格曲线直接显示突变。')
    doc.p(r'为去掉同一有限链在无挫折点已有的背景，定义用于展示相对增强的量：')
    doc.math(r'\Delta D_N(J_2)=D_N(J_2)-D_N(0),\qquad D_N(J_2)=|C_{N/2-2}(J_2)-C_{N/2-1}(J_2)|.')
    doc.p(r'基线在相同 $N$、边界条件、方法和保留维数下取值。先对原始键差取绝对值，再减去基线；不把它改成两组带符号键差相减后再取绝对值。全部原始 $D_N$ 仍保留，未用扣除值替换原来的序参量定义。')
    ed=lambda n,j:next(r for r in baselines if r['method']=='ED' and r['n']==n and r['j2']==j)
    dm=[r for r in baselines if r['method']=='DMRG']
    doc.table(['$N$','ED 基线 $D_N(0)$'],[[n,e(ed(n,0.)['baseline'])] for n in (12,16,20)])
    doc.table(['$J_2$',r'$\Delta D_{12}$（ED）',r'$\Delta D_{16}$（ED）',r'$\Delta D_{20}$（ED）',r'$\Delta D_{20}$（DMRG）'],[
        [r['j2'],e(ed(12,r['j2'])['enhancement']),e(ed(16,r['j2'])['enhancement']),
         e(ed(20,r['j2'])['enhancement']),e(r['enhancement'])] for r in dm])
    doc.p(r'扣除后 $J_2=0$ 的各尺寸曲线严格归零，更容易比较挫折带来的额外交替。以低于文献临界点的 $J_2=0.2$ 为例，$\Delta D_{20}='+e(ed(20,.2)['enhancement'])+r'$ 仍为正，说明这种相对增强并不等同于自发长程序。')
    doc.p(r'边界诱导的响应随 $J_2$ 和关联长度改变，减去一个 $J_2=0$ 常数不能消除全部边界效应。扣除值依然不能用来确定 $g_c$、证明有隙，或证明 $N\to\infty$ 后序参量非零；应结合更大尺寸外推、能隙或能级交叉等独立诊断。')
    doc.figure('dimer_baseline','原始中心键交替与同尺寸基线扣除后的曲线；虚线为文献参考相界，未由本数据反推。')


def write_tables(d):
    target=ROOT/'output'/'data'/'dimer_baseline.csv'
    with target.open('w',newline='',encoding='utf-8-sig') as stream:
        writer=csv.DictWriter(stream,fieldnames=['n','j2','method','chi','baseline','dimer','enhancement','direct_from_bonds'])
        writer.writeheader(); writer.writerows(d['review_analysis']['baselines'])
