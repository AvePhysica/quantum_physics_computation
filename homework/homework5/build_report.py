"""Render all deliverables from the SAME measured JSON; final PDF is LaTeX only."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import json
import re
import subprocess
import shutil
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output'
FIG=OUT/'figures'
REPORT=ROOT/'report'


def energy(x): return f'{x:.12f}'
def sci(x): return f'{x:.4e}'
def entropy_text(x): return f'{0. if abs(x)<5e-10 else x:.9f}'


def latex(text):
    """Escape prose while preserving the explicitly marked inline math."""
    mapping={'\\':r'\textbackslash{}','_':r'\_','%':r'\%','&':r'\&','#':r'\#',
             '{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}
    parts=re.split(r'(\$[^$]*\$)',str(text))
    return ''.join(part if part.startswith('$') else ''.join(mapping.get(ch,ch) for ch in part) for part in parts)


def make_figures(d):
    FIG.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,
                         'axes.spines.right':False,'figure.dpi':130,'savefig.dpi':180})
    def save(fig,name):
        fig.tight_layout()
        fig.savefig(FIG/(name+'.png'),bbox_inches='tight')
        fig.savefig(FIG/(name+'.pdf'),bbox_inches='tight')
        plt.close(fig)
    p=d['projection']; fig,ax=plt.subplots(figsize=(6.4,3.7))
    for prefix,label in (('dm','Density-matrix truncation'),('energy','Block-energy truncation')):
        ax.semilogy([r['m'] for r in p],[r[prefix+'_error'] for r in p],'o-',label=label)
    ax.set(xlabel='Retained states m',ylabel=r'$|E-E_0|$',title='One projection, N=12, J2=0')
    ax.set_xticks([r['m'] for r in p]); ax.legend(); ax.grid(alpha=.2); save(fig,'projection')
    runs=d['dmrg']; r0=next(r for r in runs if r['j2']==0 and r['chi']==32)
    fig,axs=plt.subplots(1,2,figsize=(9,3.5)); g=r0['growth']
    axs[0].plot([r['n'] for r in g],[r['energy_per_site'] for r in g],'o-',label='Infinite DMRG')
    axs[0].plot([r['n'] for r in g],[r['ed_energy']/r['n'] for r in g],'x',label='Independent ED')
    axs[0].set(xlabel='N',ylabel='E/N',title='Warmup, J2=0, chi=32'); axs[0].legend()
    axs[1].semilogy([r['n'] for r in g],np.maximum([r['eps_max'] for r in g],1e-16),'o-')
    axs[1].set(xlabel='N',ylabel='Discarded weight',title='Values below 1e-16 clipped for plotting')
    save(fig,'growth')
    fig,ax=plt.subplots(figsize=(6.4,3.6))
    for r in runs:
        if r['chi']!=32: continue
        ax.semilogy([0]+[x['sweep'] for x in r['sweeps']],
                    [r['growth'][-1]['ed_error']]+[x['ed_error'] for x in r['sweeps']],
                    'o-',label=f'J2={r["j2"]}')
    ax.set(xlabel='Full sweep (0 = warmup)',ylabel=r'$|E-E_0|$',title='Finite DMRG, N=20, chi=32')
    ax.set_xticks([0,1,2])
    ax.legend(); ax.grid(alpha=.2); save(fig,'sweeps')
    rs=[r for r in runs if r['j2']==0]
    fig,ax=plt.subplots(figsize=(6.4,3.6))
    for vals,label in (([r['ed_error'] for r in rs],r'$|E-E_0|$'),
                        ([r['sweeps'][-1]['eps_max'] for r in rs],'Max discarded weight (last full sweep)'),
                        ([r['sweeps'][-1]['eps_centre'] for r in rs],'Centre discarded weight')):
        ax.loglog([r['chi'] for r in rs],vals,'o-',label=label)
    ax.set(xlabel='chi',ylabel='Error / discarded weight',title='Bond-dimension convergence, N=20, J2=0')
    ax.set_xticks([2,4,8,16,32],labels=['2','4','8','16','32']); ax.legend(fontsize=8); ax.grid(alpha=.2)
    ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    save(fig,'convergence')
    fig,axs=plt.subplots(1,2,figsize=(9,3.6))
    for r in d['profiles']:
        axs[0].plot(range(1,16),r['entropy'],'o-',label=f'J2={r["j2"]}')
    axs[0].set(xlabel='Cut l',ylabel='S(l) [natural log]',title='Ground-state entanglement, N=16'); axs[0].legend()
    for name in ('product','Neel','GHZ','random'):
        rows=[r for r in d['typical'] if r['state']==name]
        axs[1].plot([r['n'] for r in rows],[r['entropy'] for r in rows],'o-',label=name)
    axs[1].set(xlabel='N',ylabel='S(N/2)',title='Typical states (not restricted to Sz=0)'); axs[1].legend(fontsize=8)
    save(fig,'entropy')
    fig,ax=plt.subplots(figsize=(6.4,3.7))
    rs=[r for r in rs if r['chi']>=4]; x=1/np.array([r['chi'] for r in rs]); ex=d['extrapolation']
    ax.plot(x,[r['energy']-ex['exact'] for r in rs],'o',label='Measured E - E0')
    grid=np.linspace(0,max(x),100)
    ax.plot(grid,ex['slope']*grid+ex['intercept']-ex['exact'],label='Linear fit')
    ax.axhline(0,color='black',lw=.8); ax.plot(0,ex['intercept']-ex['exact'],'s',label='Extrapolated intercept')
    ax.set(xlabel='1 / chi',ylabel='E - E0',title='Linear extrapolation can worsen the estimate')
    ax.legend(fontsize=8); save(fig,'extrapolation')
    from optional_report import figures
    figures(d,save)
    from review_report import figures as review_figures
    review_figures(d,save)


class Document:
    def __init__(self): self.md=[]; self.tex=[]
    def section(self,title):
        self.md.append('## '+title+'\n'); self.tex.append('\\section{'+latex(title)+'}\n')
    def sub(self,title):
        self.md.append('### '+title+'\n')
        plain=title.replace('$','').replace('\\chi','chi').replace('_','')
        self.tex.append('\\subsection{\\texorpdfstring{'+latex(title)+'}{'+latex(plain)+'}}\n')
    def p(self,text):
        self.md.append(text+'\n')
        rendered=latex(text).replace('output/data/results.json',r'\path{output/data/results.json}')
        self.tex.append(rendered+'\n\n')
    def cited_p(self,text,references):
        self.md.append(text+' '+', '.join('['+label+']('+url+')' for label,url in references)+'。\n')
        self.tex.append(latex(text)+' '+', '.join(r'\href{'+url+'}{'+latex(label)+'}' for label,url in references)+'。\n\n')
    def math(self,text): self.md.append('$$\n'+text+'\n$$\n'); self.tex.append('\\[\n'+text+'\n\\]\n')
    def table(self,headers,rows):
        rows=[[str(x) for x in row] for row in rows]
        self.md.append('| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+
                       '\n'.join('| '+' | '.join(row)+' |' for row in rows)+'\n')
        spec='l'*len(headers)
        # adjustbox only shrinks tables that would otherwise exceed text width.
        self.tex.append('\\begin{center}\n\\small\n\\begin{adjustbox}{max width=\\linewidth}\n'+
            '\\begin{tabular}{'+spec+'}\n\\toprule\n'+
            ' & '.join(latex(x) for x in headers)+r' \\'+'\n\\midrule\n'+
            '\n'.join(' & '.join(latex(x) for x in row)+r' \\' for row in rows)+
            '\n\\bottomrule\n\\end{tabular}\n\\end{adjustbox}\n\\end{center}\n')
    def figure(self,name,caption):
        self.md.append('!['+caption+'](figures/'+name+'.png)\n\n'+caption+'\n')
        self.tex.append('\\begin{figure}[htbp]\n\\centering\n'+
            '\\includegraphics[width=0.90\\linewidth]{figures/'+name+'.pdf}\n'+
            '\\caption{'+latex(caption)+'}\n\\end{figure}\n')


def assemble(d):
    doc=Document(); runs=d['dmrg']; r32=next(r for r in runs if r['j2']==0 and r['chi']==32)
    doc.p(r'本报告完成全部必做与选做 1 至 4。所有表格、图和检查实测值均来自实际执行的 output/data/results.json；精确对角化只用于基准与独立验证，未替代 DMRG。参数为 $J_1=1$、$\Delta=1$，除典型态比较及两格点全谱外，均在 $S^z_{\mathrm{tot}}=0$ 扇区。')
    doc.section('模型、约定与算法')
    doc.math(r'H=J_1\sum_{j=0}^{N-2}\left[\frac{S_j^+S_{j+1}^-+S_j^-S_{j+1}^+}{2}+\Delta S_j^zS_{j+1}^z\right]+J_2\sum_{j=0}^{N-3}\left[\frac{S_j^+S_{j+2}^-+S_j^-S_{j+2}^+}{2}+\Delta S_j^zS_{j+2}^z\right].')
    doc.p(r'使用 $S^\alpha=\sigma^\alpha/2$、$\hbar=1$。整数基矢的第 $j$ 位对应格点 $j$，比特 1 表示向上。块内部张量积的局域基依次为向下、向上；物理态恢复时显式处理位序和右块反向。熵使用自然对数，电荷标签 $q=2S^z$。')
    doc.sub('块算符、第二套边缘算符与超块')
    doc.table(['对象','保存内容','用途'],[
        ['块','长度、磁化标签、$H_B$、单位算符（隐式）','块内作用与对称性限制'],
        ['第一套边缘算符','$S^z_0,S^+_0,S^-_0$','朝向链中心的最边缘格点'],
        ['第二套边缘算符','$S^z_1,S^+_1,S^-_1$','距内边缘一个格点的位置'],
        ['基变换','父块和等距矩阵 $T$','继续生长及独立恢复物理态']])
    doc.p('左右块都按“外端到内端”存储。扩大后的左半块记为 $A$，扩大后的右半块记为 $B$；二者最内侧格点分别是两个新增中心格点。跨中点的键严格只有三条：$J_1 A_0B_0$、$J_2 A_1B_0$、$J_2 A_0B_1$。块扩大时，新格点还需与旧块倒数第二个格点发生 $J_2$ 耦合，因此必须保存第二套边缘算符。')
    doc.math(r'H_{\mathrm{super}}X=H_AX+XH_B^{\mathsf T}+\sum_{\mu}c_\mu O_{A,\mu}X O_{B,\mu}^{\mathsf T}.')
    doc.p('超块采用矩阵自由的稀疏迭代最低本征值求解，仅在 $q_A+q_B=0$ 的分量中工作；未构造巨大的稠密超块矩阵。不截断的稠密/精确对角化只用于题目明确要求的对照实验。')
    doc.sub('截断逻辑：全局维数限制和一致算符更新')
    doc.math(r'X_q=U_q\Lambda_q V_q^\dagger,\qquad w_{q,i}=\lambda_{q,i}^2,\qquad T=(u_{q,i})_{\text{global top }\chi}.')
    doc.p(r'先按左块磁化分组，并与右块相反磁化子空间配对做 SVD；随后把所有磁化分块的权重放在同一个列表中排序，只保留全局最大的 $\chi$ 个。不是每个分块各保留 $\chi$ 个。矩形分块保留完整左奇异向量基，缺少的奇异值补零，保证小尺寸不截断和零权重情形仍有正确的正交基。')
    doc.math(r'H_B\longleftarrow T^\dagger H_BT,\qquad O_B\longleftarrow T^\dagger O_BT,\qquad \varepsilon=1-\sum_{\mathrm{kept}}w_i.')
    doc.p(r'哈密顿量和两套边缘算符使用同一个等距矩阵，电荷标签同步排序。每次截断都核对 $T^\dagger T=I$、电荷守恒及直接投影损失 $\|X-TT^\dagger X\|_F^2=\varepsilon$。表中能量取当前超块优化态在这一步截断之前的期望值；丢弃权重描述该态随后用于更新块时的局部损失。它不是最终态能量误差的严格界。')
    doc.sub('生长与扫描')
    doc.p('infinite 阶段从单格点左右块开始，每次左右各增一个格点，求解超块后独立更新两侧块。finite 阶段固定总长，缓存并更新各长度的左右环境；向右扫描只更新左侧增长块，向左扫描只更新右侧增长块。一次完整 sweep 定义为“中点到右端、右端到左端、左端回中点”，能量在同一中点位置比较。')
    doc.p(r'局部求解器容差为 $2\times10^{-12}$；至少扫描两次，完整 sweep 中点能量变化小于 $10^{-9}$ 时停止。必做与长链计算最多 12 次，二聚化扫描上限为 20 次。扫描停止说明该固定 $\chi$ 的迭代稳定，不意味着截断误差可忽略。双格点优化后还有截断，逐步或逐次扫描的能量不要求严格单调。')

    doc.section('必做 1：不截断超块与精确对角化')
    doc.table(['$J_2$','$N$','ED 能量','超块能量','绝对差'],[
        [r['j2'],r['n'],energy(r['ed']),energy(r['superblock']),sci(r['difference'])] for r in d['small']])
    doc.p(r'上述 ED 用整数比特翻转独立建矩阵；超块使用块算符张量积，两条构造路径未共享哈密顿量矩阵。额外测试覆盖 $\Delta=0.73$，防止只在各向同性参数下偶然正确。')

    doc.section('必做 2：密度矩阵截断与块能量截断')
    doc.p('取 $N=12,J_2=0$，中点切分，精确能量为 $E_0='+energy(d['projection_e0'])+'$。两种方法均只投影左半链并重新归一化，右半链不截断，不在投影空间重新优化。块能量截断的 $H_A$ 仅包含左半链自己的开边界相互作用。')
    doc.math(r'|\widetilde\psi\rangle=\frac{(P_A\otimes I_B)|\psi_0\rangle}{\|(P_A\otimes I_B)|\psi_0\rangle\|},\qquad E=\langle\widetilde\psi|H|\widetilde\psi\rangle.')
    doc.table(['$m$','密度矩阵法 $|E-E_0|$','块能量法 $|E-E_0|$','密度矩阵丢弃权重'],[
        [r['m'],sci(r['dm_error']),sci(r['energy_error']),sci(r['dm_discard'])] for r in d['projection']])
    doc.p('Schmidt 截断针对当前基态与环境的纠缠，最大化保留范数；孤立块的低能态并不一定能表达与右半链形成的关联。本组数据中，除极小 $m$ 时优势较有限外，密度矩阵法的能量误差明显更小。但其严格最优性针对态范数，并非对任意模型、任意 $m$ 都能保证能量误差最小。')
    doc.p('对称性简并处需要格外小心：若全矩阵 SVD 任意混合不同磁化量的简并向量，再在简并子空间中截断，可能离开指定总磁化扇区。本实验采用按磁化分块的 SVD。块能量法也按磁化分块求解，按能量、磁化和本征态序号确定简并时的顺序；截断可能切开 SU(2) 多重态，但始终保持 U(1) 磁化守恒。')
    doc.figure('projection','单次投影的能量误差比较；两种方法使用同一个原始开链哈密顿量评估。')

    doc.section('必做 3：infinite DMRG 生长')
    doc.p(r'取 $J_2=0,\chi=32$。前七行生长到题目要求的 $N=16$；后两行是为 $N=20$ 有限扫描继续进行的 warmup。实际保留维数指截断后左右块各自的维数；小尺寸尚未达到上限。')
    doc.table(['$N$','实际保留维数','能量 $E$','$E/N$',r'$\varepsilon_{\max}$','ED 误差'],[
        [r['n'],f'{r["kept_left"]}/{r["kept_right"]}',energy(r['energy']),energy(r['energy_per_site']),
         sci(r['eps_max']),sci(r['ed_error'])] for r in r32['growth']])
    doc.p(r'上表固定上限为 $\chi=32$，丢弃权重取本步左右截断中较大者。前几步的机器精度微小权重不表示物理截断；块尺寸超过上限后发生真实截断。小尺寸与必做 1 的精确能量对上；更长链另外使用独立稀疏 ED 对照，并将每个生长态恢复到原始比特基底直接计算能量。')
    doc.figure('growth','生长阶段的能量密度和丢弃权重；绘图对低于 $10^{-16}$ 的权重设置显示下限，表格保留原值。')

    doc.section('必做 4：finite DMRG 扫描')
    for r in [r for r in runs if r['chi']==32]:
        doc.sub('$J_2='+str(r['j2'])+r'$，$N=20,\chi=32$')
        doc.p('独立精确参照为 $E_0='+energy(r['ed_energy'])+'$。')
        rows=[['warmup',energy(r['growth'][-1]['energy']),sci(r['growth'][-1]['ed_error']),
               sci(r['growth'][-1]['eps_max'])]]
        rows.extend([[x['sweep'],energy(x['energy']),sci(x['ed_error']),sci(x['eps_max'])] for x in r['sweeps']])
        doc.table(['完整 sweep','能量 $E$','$|E-E_0|$','本轮最大丢弃权重'],rows)
        doc.p('与 warmup 相比，最终能量降低 $'+sci(r['growth'][-1]['energy']-r['energy'])+'$；'+
              '最后两次中点能量变化为 $'+sci(r['sweeps'][-1]['energy_change'])+'$。')
    doc.p(r'有限扫描重新优化不同切口处的块基，因此比只生长一次能更好地适配固定长度的环境。这里 $\chi=32$ 的 warmup 本来已很准确，能量改善量较小；每轮结果仍以恢复到物理基底的能量期望值独立核对。')
    doc.figure('sweeps','两组耦合下的有限扫描误差；横坐标 0 为生长阶段结束。')

    doc.section('必做 5：收敛诊断与能量方差')
    doc.p('固定 $N=20,J_2=0$，精确参照 $E_0='+energy(r32['ed_energy'])+'$。丢弃权重同时报告最后一整轮的最大值和最终中点值，避免只挑误差较小的切口。')
    doc.table([r'$\chi$','最终 $E$','$|E-E_0|$','最大丢弃权重','中点丢弃权重','sweep 数'],[
        [r['chi'],energy(r['energy']),sci(r['ed_error']),sci(r['sweeps'][-1]['eps_max']),
         sci(r['sweeps'][-1]['eps_centre']),len(r['sweeps'])] for r in runs if r['j2']==0])
    doc.p(r'全部固定 $\chi$ 计算均达到所设扫描停止条件。$\chi=2$ 需要更多扫描才稳定，但稳定后的能量仍明显偏离精确值：迭代收敛不能替代保留维数收敛。判断 $\chi$ 是否够大，优先观察跨切口的丢弃权重，并同时增大 $\chi$ 核对能量和目标观测量是否稳定；已知精确值时，再以真实能量误差量化。不存在脱离所需精度的统一“够大”阈值。')
    doc.figure('convergence','能量误差与两种口径的丢弃权重随保留维数下降；它们相关，但不是同一个量。')
    doc.sub('精确基态能量方差')
    doc.math(r'\mathrm{Var}(H)=\langle H^2\rangle-\langle H\rangle^2=\|(H-E)|\psi\rangle\|^2.')
    doc.table(['$N$','$J_2$','直接相减','残差范数平方','独立张量算符残差平方'],[
        [12,r['j2'],sci(r['variance_subtraction']),sci(r['variance_residual']),sci(r['variance_tensor'])] for r in d['variance']])
    doc.p('精确本征态的理论方差为零。直接相减可能得到舍入量级的正数或负数，后者不表示物理上的负方差；残差范数平方更稳定。小方差只说明该态接近所用哈密顿量的本征态，仍需解析解与独立算符实现来核对哈密顿量本身。')

    doc.section('必做校检：小尺寸和 MG 点')
    doc.sub('开边界与周期边界')
    doc.p('两格点全空间谱检验单重态 $-3J_1/4$ 和三重态 $J_1/4$（三重简并），且所有已用 ED 矩阵均满足厄米性。下表取 $J_2=0$；周期环比开链多出连接两端的最近邻键，相关能不能用一个固定常数直接扣除，因为基态也会重新调整。')
    doc.table(['$N$','开链基态能量','周期环基态能量','开链减周期'],[
        [r['n'],energy(r['open']),energy(r['periodic']),energy(r['difference'])] for r in d['boundaries']])
    doc.p(r'周期参照按对所有 $j$ 求和并取模定义。若以后比较 $N=4$ 且 $J_2\ne0$ 的环，次近邻对在该求和中出现两次；本表 $J_2=0$，不涉及这一小尺寸约定。')
    doc.sub('Majumdar–Ghosh 点')
    doc.math(r'J_2=J_1/2,\quad |D_0\rangle=\bigotimes_{m=0}^{N/2-1}\frac{|\uparrow\downarrow\rangle-|\downarrow\uparrow\rangle}{\sqrt2},\quad E_0=-\frac{3N J_1}{8}.')
    doc.p(r'每对单重态中 $\mathbf S_{2m}+\mathbf S_{2m+1}$ 湮灭该态，相邻二聚体之间的一条最近邻键和两条半强度次近邻键相互抵消；每个内部二聚体贡献 $-3J_1/4$。这提供独立于本征值求解器的解析态与解析能量。')
    doc.table(['$N$','ED 能量','解析能量','二聚体本征残差',r'$|\langle D_0|\psi_{ED}\rangle|^2$'],[
        [r['n'],energy(r['ed']),energy(r['exact']),sci(r['residual']),f'{r["overlap_squared"]:.12f}'] for r in d['mg']])
    doc.p(r'残差定义为 $\|H|D_0\rangle-E_0|D_0\rangle\|$，重叠取模平方以消除全局相位。')
    doc.table(['$N$',r'切口 $l=1,\ldots,N/2$ 的熵（依次）'],[
        [r['n'],', '.join(entropy_text(x) for x in r['entropy'])] for r in d['mg']])
    doc.p(r'奇数切口切断一个单重态，熵为 $\ln2$；偶数切口位于两个二聚体之间，熵为零。ED 基态所得剖面与解析二聚体结构一致。')

    doc.section('独立校检策略与故意注错')
    doc.p('完整逐条清单见 output/validation.md，每项都记录错误类型、期望值、实测值、容差及结论。主运行共 '+str(len(d['checks']))+' 项检查，全部通过。下面按类型归纳；厄米性、归一化、求解器残差均仅作为辅助，不能替代独立物理核验。')
    doc.table(['校检类型','针对的错误','错误时如何失败'],[
        ['两格点解析谱','自旋因子或相互作用符号','谱与单重态/三重态解析值不符'],
        ['原始位基 ED 对超块','J2 漏键、边缘位置、重整化错误','物理态能量与超块结果不符'],
        ['局域张量算符对 ED','位翻转矩阵元、周期回绕、耦合符号','同一物理态的 H 作用结果不符'],
        ['MG 解析能量与态','J2 系数、错误边界键','能量或显式二聚体残差不符'],
        ['投影损失与磁化','保留权重排序、不同电荷混合','范数损失、维数上限或电荷等式不符'],
        ['SVD 对约化密度矩阵','切口、归一化、权重平方','两种熵计算不一致'],
        ['方差的不同算法','H 平方或数值相消问题','稳定残差与直接相减超容差']])
    doc.p('回归测试还覆盖非各向同性参数及有限扫描的全部局部位置；在小尺寸下逐个恢复局部优化态并与独立物理哈密顿量核对，避免仅检查扫描结束位置。完整主计算独立展开了每个生长态和每轮完整扫描结束态。')
    doc.table(['故意注入的错误','检测不符量','捕获'],[
        [r['name'],sci(r['mismatch']),'是' if r['caught'] else '否'] for r in d['mutations']])
    doc.p('重要反例：MG 二聚体在周期环上也可能满足相同的能量关系，因此仅靠 MG 态能量不能可靠发现增加回绕键。周期键注错特意改用一般测试向量，与独立的开链局域张量算符逐项作用对比。所有注错均使用独立对象，未污染最终计算。')
    for prefix,label in [('physical ','物理态能量复核'),('projection loss','投影损失复核'),('charge retention','磁化守恒'),('isometry','截断等距性'),('ED tensor action','局域张量算符复核')]:
        rows=[x for x in d['checks'] if x['name'].startswith(prefix)]
        if rows:
            doc.p(label+'：'+str(len(rows))+' 项，最大实测偏差 $'+sci(max(abs(x['measured']-x['expected']) for x in rows))+'$。')

    doc.section('选做 1：纠缠剖面与典型态')
    doc.table(['切口 $l$','$J_2=0$ 的 $S(l)$','$J_2=0.5$ 的 $S(l)$'],[
        [l+1,entropy_text(d['profiles'][0]['entropy'][l]),entropy_text(d['profiles'][1]['entropy'][l])] for l in range(15)])
    doc.p('两组均通过 $S(l)=S(N-l)$ 的数值核对。$J_2=0$ 的最大值位于切口 '+str(d['profiles'][0]['max_cuts'])+'；MG 点的最大值位于所有奇数切口 '+str(d['profiles'][1]['max_cuts'])+'。开边界引起的奇偶振荡使最大值不必恰在中点。')
    names={'product':'乘积态','Neel':'Néel 态','GHZ':'GHZ 态','random':'随机纯态'}
    doc.table(['$N$']+[names[x] for x in names],[[n]+[entropy_text(next(r['entropy'] for r in d['typical'] if r['n']==n and r['state']==name)) for name in names] for n in (4,8,12,16)])
    doc.p(r'乘积态取所有局域态为 $(|\downarrow\rangle+|\uparrow\rangle)/\sqrt2$，Néel 态为交替自旋的单个组态，GHZ 态取全下和全上的等幅叠加，随机态由独立复高斯系数归一化，种子为 20261019+N。这一部分不限制总磁化。')
    doc.p(r'乘积态和 Néel 态无纠缠，GHZ 态的任意非平凡切口熵恒为 $\ln2$，均符合一维面积律的有界熵特征；一般随机纯态的中点熵随系统长度增长，体现体积律。MG 基态具有严格有界的二聚体纠缠。$J_2=0$ 链的剖面不能仅凭一个尺寸就证明严格面积律；应区分临界体系可能的对数修正与体积律。')
    doc.figure('entropy','完整纠缠剖面，以及四类典型态在不同系统长度下的中点纠缠熵。')

    doc.section('选做 2：保留维数外推')
    ex=d['extrapolation']
    doc.p(r'严格按题目要求，对 $\chi=4,8,16,32$ 的能量与 $1/\chi$ 做无权线性最小二乘拟合。')
    doc.math(r'E(\chi)=a/\chi+b,\qquad a='+energy(ex['slope'])+r',\quad b='+energy(ex['intercept'])+'.')
    doc.table(['估计方式','能量','与 ED 的绝对误差'],[
        [r'$\chi=32$',energy(r32['energy']),sci(ex['chi32_error'])],
        [r'$1/\chi$ 线性外推截距',energy(ex['intercept']),sci(ex['error'])],
        ['ED 参照',energy(ex['exact']),'0（参照自身）']])
    doc.p(r'本次线性外推没有改善精度，而且落到精确能量以下。各个 DMRG 能量是变分上界，但拟合截距不是变分态的期望值，不受同样的上界约束。误差随 $\chi$ 并不呈简单的 $1/\chi$ 线性趋势，尤其小 $\chi$ 点偏离精确值较大，直接外推会产生模型误差。')
    doc.figure('extrapolation','按题目指定横坐标进行的线性外推；截距比最准确的直接计算更差。')
    from review_report import append_scaling
    append_scaling(doc,d)

    from optional_report import append_optional
    append_optional(doc,d)
    doc.section('源码、复现与开发修正')
    doc.table(['文件','职责'],[
        ['src/core.py','比特 ED、块扩大、超块作用、分块 SVD、统一投影、生长与扫描'],
        ['src/analysis.py','二聚体、纠缠熵、单次截断实验、独立局域张量算符'],
        ['src/mps_observables.py','从块等距矩阵恢复物理 MPS、可扩展关联测量及独立比特关联'],
        ['src/refinements.py','误差/丢弃权重拟合及同尺寸基线扣除'],
        ['tests/test_core.py','磁化分块、全局上限、零权重、全扫描位置与物理基底验证'],
        ['tests/test_analysis.py','二聚体解析解和全部指定 m 值的投影实验'],
        ['tests/test_mps_observables.py','不对称随机态、虚拟基变换、物理关联与长二聚体测试'],
        ['run_homework5.py','完整数值实验、精确参照、逐条校检、原始态及结果存档'],
        ['run_optional.py','长开链和全耦合网格的二聚化实验与独立校检'],
        ['optional_report.py','选做 3/4 同源结果表、图、物理讨论及逐键 CSV'],
        ['refine_results.py','只重算新增分析，复用已独立校检的物理数据'],
        ['review_report.py','误差标度、文献相图和基线扣除的图表与讨论'],
        ['verify_outputs.py','核对 Markdown/PDF 数值、CSV 和长链 MPS 存档'],
        ['build_report.py','从同一 JSON 生成图、独立结果文档、中文说明和 LaTeX 报告']])
    doc.p('开发中修正了一处真实问题：对照实验最初使用全矩阵 SVD，在部分简并值截断时产生磁化泄漏；已改为分磁化 SVD，并将全部指定 m 值纳入测试。另将最低保留维数的扫描上限从 6 增加到 12，确保实际达到收敛阈值。这些修正均在最终结果产生前重新运行验证。')
    doc.p('所有结果路径和从干净环境运行的命令见根目录 README.md。report/report.tex 是提交中的 LaTeX 源文件，引用 output/figures 下的图；最终报告只经 XeLaTeX 编译。')
    if (ROOT/'AI_USAGE_RECORD.md').exists():
        doc.p('用户已明确授权生成 AI 使用记录。项目根目录 AI_USAGE_RECORD.md 保留作业相关 prompt 原文、可见回复要点、文件动作和修改原因台账，应与本报告及源码一同提交。')
        doc.md.append('[AI 使用与对话记录](../AI_USAGE_RECORD.md)\n')
    else:
        doc.p('AI 使用记录将在学生审阅测试结果并明确授权后，依据实际对话单独生成。')
    return doc


def write_validation(d):
    lines=['# 独立校检逐条清单\n',
        '这里同时列出独立物理校检和辅助数值检查；辅助项不能单独证明哈密顿量正确。\n',
        '期望值与实测值的绝对差不超过所列容差即通过。错误类型与其对应的失败方式详见 result.md 的校检策略。\n',
        '| 编号 | 校检 | 针对的错误类型 | 期望值 | 实测值 | 容差 | 结论 |',
        '| --- | --- | --- | --- | --- | --- | --- |']
    for i,r in enumerate(d['checks'],1):
        lines.append(f'| {i} | {r["name"]} | {r["target"]} | {r["expected"]:.12g} | {r["measured"]:.12g} | {r["tolerance"]:.3g} | '+('通过' if r['passed'] else '失败')+' |')
    (OUT/'validation.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')


def write_readme(d):
    text=r'''# 第五次作业：开边界 J1–J2 XXZ 链的传统 DMRG

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

[完整数值结果](output/result.md)、[逐条校检](output/validation.md)、[合并 PDF 报告](output/report.pdf)。报告中的表和图全部来自同一个 results.json，避免手工抄写差异。AI 对话记录暂未生成，需学生确认测试结果并授权后另建。

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
'''
    # Raw string above is ordinary Markdown, so use single backslashes in math.
    text=text.replace('\\\\','\\')
    if (ROOT/'AI_USAGE_RECORD.md').exists():
        text=text.replace('AI 对话记录暂未生成，需学生确认测试结果并授权后另建。',
            '用户已明确授权，已生成[AI 使用与对话记录](AI_USAGE_RECORD.md)，包含 prompt 原文、可见回复要点、产出文件和修改原因台账。提交时请将该记录与源码及报告一并保留。')
    (ROOT/'README.md').write_text(text,encoding='utf-8')


def main():
    d=json.loads((OUT/'data'/'results.json').read_text(encoding='utf-8'))
    if not d.get('extrapolation') or not d.get('optional34_complete') or not d.get('review_analysis',{}).get('complete') or not all(x['passed'] for x in d['checks']):
        raise RuntimeError('Complete successful numerical run required before producing report')
    if not all(x['converged'] for x in d['dmrg']):
        raise RuntimeError('Do not label unconverged runs as final results')
    make_figures(d); doc=assemble(d); write_readme(d); write_validation(d)
    from optional_report import write_tables
    write_tables(d)
    from review_report import write_tables as write_review_tables
    write_review_tables(d)
    (OUT/'result.md').write_text('# 第五次作业完整结果\n\n'+'\n'.join(doc.md),encoding='utf-8')
    REPORT.mkdir(parents=True,exist_ok=True)
    preamble=r'''\documentclass[zihao=5,a4paper]{ctexart}
\usepackage[margin=2.15cm]{geometry}
\usepackage{amsmath,amssymb,booktabs,graphicx,adjustbox,float,hyperref,fancyhdr}
\hypersetup{colorlinks=true,linkcolor=blue,urlcolor=blue}
\setlength{\parskip}{0.25em}
\setlength{\emergencystretch}{3em}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{量子物理计算方法选讲}
\fancyhead[R]{第五次作业：传统 DMRG}
\fancyfoot[C]{\thepage}
\setlength{\headheight}{14pt}
\title{开边界 $J_1$--$J_2$ XXZ 链上的传统 DMRG\\\large 实现、截断逻辑与独立数值校检}
\author{}
\date{2026 年 10 月 19 日}
\begin{document}
\maketitle
\begin{abstract}
手写传统双格点块 DMRG，显式保存两套边缘算符，采用保持磁化量的分块 SVD 和全局 Schmidt 权重截断。完成全部必做及四项选做，包含长开链能量密度和二聚化关联扫描，区分边界、保留维数和有限尺寸效应。精确对角化、局域张量算符与独立物理 MPS 收缩提供验证，所有结果来自实际运行。
\end{abstract}
\setcounter{tocdepth}{1}
\tableofcontents
\clearpage
'''
    source=preamble+'\n'.join(doc.tex)+'\n\\end{document}\n'
    (REPORT/'report.tex').write_text(source,encoding='utf-8')
    # Markdown math rules: inspect prose only; code samples can contain literals.
    for path in [ROOT/'README.md',OUT/'result.md',OUT/'validation.md']:
        content=path.read_text(encoding='utf-8')
        if any(token in content for token in ('\\(','\\)','\\[','\\]')):
            raise AssertionError('Forbidden Markdown math delimiter: '+str(path))
    if '--no-compile' not in os.sys.argv:
        # Clean-state LaTeX compilation, keeping source and referenced assets.
        for extension in ('aux','toc','out','log','fdb_latexmk','fls','xdv','pdf'):
            generated=OUT/('report.'+extension)
            if generated.exists(): generated.unlink()
        if shutil.which('latexmk'):
            command=['latexmk','-xelatex','-interaction=nonstopmode','-halt-on-error','-outdir=.',str(REPORT/'report.tex')]
            subprocess.run(command,cwd=OUT,check=True)
        else:
            for _ in range(2):
                subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error','-output-directory=.',str(REPORT/'report.tex')],cwd=OUT,check=True)
        log=(OUT/'report.log').read_text(encoding='utf-8',errors='replace')
        failures=['undefined references','Reference `','LaTeX Error','Missing character:']
        if any(token in log for token in failures):
            raise RuntimeError('LaTeX log contains unresolved references or missing assets/glyphs')
    print('Generated figures, README.md, result.md, validation.md, and LaTeX report.',flush=True)


if __name__=='__main__': main()
