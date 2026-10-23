"""Measured optional 3/4 tables, plots and discussion, shared by MD and LaTeX."""
import csv
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent


def e(x): return f'{x:.12f}'
def s(x): return f'{x:.4e}'


def figures(d,save):
    long=d['long_chains']; scan=d['dimer_scan']; limit=d['thermodynamic_energy']
    fig,axs=plt.subplots(1,2,figsize=(9,3.6))
    for chi in (32,64):
        rows=[r for r in long if r['chi']==chi]
        xs=[1/r['n'] for r in rows]; ys=[r['energy_per_site'] for r in rows]
        if chi==32:
            base=next(r for r in d['dmrg'] if r['chi']==32 and r['j2']==0)
            xs.append(1/20); ys.append(base['energy']/20)
        else:
            base=next(r for r in scan if r['method']=='DMRG' and r['j2']==0)
            xs.append(1/20); ys.append(base['energy']/20)
        indices=np.argsort(xs)
        axs[0].plot(np.array(xs)[indices],np.array(ys)[indices],'o-',label=f'chi={chi}')
    axs[0].axhline(limit,color='black',ls='--',label='1/4 - ln 2')
    axs[0].set(xlabel='1/N',ylabel='E/N',title='Open chains: finite-size energy density')
    axs[0].set_xlim(0,.052); axs[0].legend(fontsize=8)
    ns=(40,60); gaps=[]; shifts=[]
    for n in ns:
        hi=next(r for r in long if r['n']==n and r['chi']==64)
        lo=next(r for r in long if r['n']==n and r['chi']==32)
        gaps.append(abs(hi['energy_per_site']-limit))
        shifts.append(abs(hi['energy_per_site']-lo['energy_per_site']))
    axs[1].semilogy(ns,gaps,'o-',label='Distance to infinite-chain value')
    axs[1].semilogy(ns,shifts,'s-',label='Change from chi=32 to 64')
    axs[1].set(xlabel='N',ylabel='Energy density difference',title='Finite size versus finite chi')
    axs[1].set_xticks(ns); axs[1].legend(fontsize=8)
    save(fig,'thermodynamic')

    fig,axs=plt.subplots(1,2,figsize=(9,3.6))
    for n in (12,16,20):
        rows=[r for r in scan if r['method']=='ED' and r['n']==n]
        x=[r['j2'] for r in rows]; y=[r['dimer'] for r in rows]
        axs[0].plot(x,y,'o-',label=f'ED N={n}')
        axs[1].plot(x,y,'o-',label=f'ED N={n}')
    rows=[r for r in scan if r['method']=='DMRG']
    for ax in axs:
        ax.plot([r['j2'] for r in rows],[r['dimer'] for r in rows],'kx',ms=7,label='DMRG N=20, chi=64')
        ax.set(xlabel='J2',ylabel='Central bond alternation D(N)'); ax.grid(alpha=.2)
    axs[0].set_title('Dimerization on open finite chains'); axs[0].legend(fontsize=7)
    axs[1].set(xlim=(-.01,.41),ylim=(.1,.65),title='Low-coupling range: boundary effects remain')
    save(fig,'dimerization')
    fig,ax=plt.subplots(figsize=(7.2,3.6))
    for j2 in (0.,.3,.5,1.):
        row=next(r for r in rows if r['j2']==j2)
        ax.plot(range(19),row['nearest'],'o-',ms=3,label=f'J2={j2}')
    ax.axvspan(7.6,9.4,color='grey',alpha=.12,label='Two central bonds (j=8,9)')
    ax.set(xlabel='Bond left endpoint j (zero based)',ylabel=r'$\langle\mathbf{S}_j\cdot\mathbf{S}_{j+1}\rangle$',
           title='Full nearest-neighbour profiles, N=20, chi=64')
    ax.set_xticks(range(0,19,2)); ax.legend(fontsize=8,ncol=3); ax.grid(alpha=.2)
    save(fig,'bond_profiles')


def append_optional(doc,d):
    long=d['long_chains']; scan=d['dimer_scan']; limit=d['thermodynamic_energy']
    doc.section('选做 3：更长开链与热力学极限')
    doc.p(r'固定 $J_1=1,\Delta=1,J_2=0$，将同一传统 DMRG 扩展到 $N=40,60$，分别取 $\chi=32,64$。仅使用保持磁化的截断块，不展开长链的完整自旋空间。题给无限均匀链能量密度为：')
    doc.math(r'e_\infty=\frac14-\ln2='+e(limit)+'.')
    doc.table(['$N$',r'$\chi$','最终 $E$','$E/N$',r'$E/N-e_\infty$','最大丢弃权重','轮数'],[
        [r['n'],r['chi'],e(r['energy']),e(r['energy_per_site']),s(r['difference_from_infinite']),
         s(r['eps_max']),len(r['sweeps'])] for r in long])
    doc.p(r'所有长链计算均达到相邻完整 sweep 中点能量变化小于 $10^{-9}$ 的停止条件。下表把同一尺寸增加保留维数的变化，与有限开链能量密度距无限链的差分开：')
    rows=[]
    for n in (40,60):
        hi=next(r for r in long if r['n']==n and r['chi']==64)
        lo=next(r for r in long if r['n']==n and r['chi']==32)
        rows.append([n,s(abs(hi['energy_per_site']-lo['energy_per_site'])),
                     s(hi['difference_from_infinite']),e(n*hi['difference_from_infinite'])])
    doc.table(['$N$',r'$\chi=32\to64$ 的 $|\Delta(E/N)|$',r'$\chi=64$ 的 $E/N-e_\infty$',r'$N(E/N-e_\infty)$'],rows)
    doc.p(r'有限开链缺少跨越两端的键，端点附近的关联也随之调整；总能量含有有限的边界贡献，除以 $N$ 后表现为约 $1/N$ 的偏离，并叠加其他有限尺寸修正。本次增大 $N$ 明显缩小偏差，而同一尺寸增大 $\chi$ 的影响小得多，说明表中距无限链值的差主要来自有限长度和边界。')
    doc.p(r'这里没有把有限开链与无限链的差直接当作 DMRG 算法误差，也没有把两个长度的结果拟合成已知精度的热力学极限。两个长度、两种保留维数只能展示误差变化；若要求严格的极限精度，还需要更多尺寸和更系统的截断收敛分析。')
    doc.figure('thermodynamic','开链能量密度逐渐接近无限链值；右图比较有限长度偏差与增加保留维数带来的变化。')
    doc.sub('长链的独立物理校检')
    doc.p(r'从保存的块等距矩阵逐格点恢复物理 MPS，再以独立定义的局域 $S^x,S^y,S^z$ 做左右环境收缩，计算每条最近邻和次近邻关联，并重新求和得到能量。这条路径不调用重整化哈密顿量和边缘算符；漏掉键、右块方向错误或算符投影不一致时，会与超块能量不符。每轮完整扫描都执行该检查，并核对 MPS 范数。')
    doc.table(['$N$',r'$\chi$','物理关联求和能量','与超块能量之差','MPS 范数'],[
        [r['n'],r['chi'],e(r['physical_energy']),s(abs(r['physical_energy']-r['energy'])),e(r['norm'])] for r in long])
    doc.p(r'新增测试以小系统原始比特态核对全部键，包括左右长度不同的随机态和任意虚拟基变换，避免反射对称掩盖位序错误。另以 40 格点显式单重态乘积 MPS 核对解析的强弱键剖面。长链张量保存于 output/data/mps_N*.npz，可直接重建并复测，不需要指数空间。')

    doc.section('选做 4：二聚化关联与有限尺寸限制')
    doc.p(r'固定 $\Delta=1$，扫描 $J_2=0,0.1,\ldots,1.0$。主计算使用 $N=20,\chi=64$ 的有限 DMRG，并逐点与独立精确对角化对照；另计算 $N=12,16$ 的精确结果作为有限尺寸比较。定义：')
    doc.math(r'C_j=\langle\mathbf S_j\cdot\mathbf S_{j+1}\rangle,\qquad D_N=\left|C_{N/2-2}-C_{N/2-1}\right|.')
    doc.p(r'格点与键均从 0 开始编号。$N=20$ 时比较的是 $C_8$ 和 $C_9$，即紧邻中点的两条相邻键。保存带符号的差和绝对值，绘图用绝对值；完整逐键关联在 output/data/dimer_bonds.csv，原始结果与校检在 results.json。')
    dm=[r for r in scan if r['method']=='DMRG']
    doc.table(['$J_2$','$C_8$','$C_9$','$D_{20}$',r'与 ED 的 $|\Delta D|$','最大逐键误差'],[
        [r['j2'],e(r['central_values'][0]),e(r['central_values'][1]),e(r['dimer']),s(r['dimer_error']),s(r['bond_error'])] for r in dm])
    doc.sub('精确有限尺寸对照')
    ed=lambda n,j2:next(r for r in scan if r['method']=='ED' and r['n']==n and r['j2']==j2)
    doc.table(['$J_2$','$D_{12}$（ED）','$D_{16}$（ED）','$D_{20}$（ED）'],[
        [j2,e(ed(12,j2)['dimer']),e(ed(16,j2)['dimer']),e(ed(20,j2)['dimer'])] for j2 in [r['j2'] for r in dm]])
    best=max(dm,key=lambda r:r['dimer'])
    doc.p(r'本次有限尺寸曲线在 $J_2\approx0.2$ 至 $0.5$ 的区间交替明显增强，网格上的最大值出现在 $J_2='+str(best['j2'])+r'$。之后交替强度降低，不能把它简单理解为随挫折耦合单调增长。MG 点 $J_2=0.5$ 的强键关联为 $-3/4$、弱键为零，因此 $D_N=3/4$，与全部三个尺寸的计算一致。')
    doc.p(r'“首次出现非零交替”不能用作本组有限开链的相变判据：即使 $J_2=0$，边界也诱导交替，其中心值依次为 $'+e(ed(12,0.)['dimer'])+'$、$'+e(ed(16,0.)['dimer'])+'$、$'+e(ed(20,0.)['dimer'])+r'$，随长度变化。本结果能说明有限系统的键交替随耦合增强及其尺寸依赖；不能单独证明热力学极限存在非零自发序参量，也不能从 0.1 的扫描间隔确定临界耦合。')
    doc.p(r'若要定位真正的二聚化转变，还需更长链、更多尺寸、更细耦合网格，并对边界诱导振荡和保留维数做系统分析。本次不把平滑增强的有限尺寸曲线标成精确相变点。')
    doc.figure('dimerization','中心键交替强度随耦合的变化；DMRG 与精确结果重合，低耦合区仍可见有限尺寸和边界效应。')
    doc.figure('bond_profiles','代表性耦合下的全部最近邻键关联，阴影标出用于定义二聚化强度的两条键。')
    from review_report import append_phase_baseline
    append_phase_baseline(doc,d)
    doc.sub('独立校检与精度')
    doc.p(r'每个耦合点以三条路径交叉核验：DMRG 的物理 MPS 收缩、同一近似态展开后的比特关联、独立 ED 基态关联。每个尺寸的两条中心键再用局域 2×2 张量作用复核，并用全部键关联重组 ED 能量。')
    doc.table(['$J_2$','DMRG 能量','ED 能量','能量绝对误差','最大丢弃权重'],[
        [r['j2'],e(r['energy']),e(r['ed_energy']),s(r['energy_error']),s(r['eps_max'])] for r in dm])
    mutation=d['optional34_mutation']
    doc.p('对实际 MPS 测量程序注入横向系数加倍的错误后，单重态键关联从期望的 '+e(mutation['expected'])+' 变成 '+e(mutation['wrong_measured'])+'，被解析关联检查捕获；随后恢复正确算符。全部新增校检连同期望、实测和针对的错误类型，均已并入 output/validation.md。')


def write_tables(d):
    path=ROOT/'output'/'data'/'dimer_bonds.csv'
    with path.open('w',newline='',encoding='utf-8-sig') as stream:
        writer=csv.writer(stream)
        writer.writerow(['N','J2','method','chi','bond_j','site_i','site_j','nearest_correlation'])
        for row in d['dimer_scan']:
            for j,value in enumerate(row['nearest']):
                writer.writerow([row['n'],row['j2'],row['method'],row.get('chi',''),j,j,j+1,format(value,'.16g')])
