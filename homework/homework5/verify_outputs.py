"""Audit submitted numeric tokens, links, PDF log, CSV and serialized long MPS."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path
import numpy as np
from src.mps_observables import Measurements

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output'


def main():
    raw=OUT/'data'/'results.json'; d=json.loads(raw.read_text(encoding='utf8'))
    assert d.get('optional34_complete'),'Optional computations incomplete'
    assert d.get('review_analysis',{}).get('complete'),'Review analysis incomplete'
    assert all(r['passed'] for r in d['checks'])
    assert all(r['converged'] for r in d['dmrg']+d['long_chains'])
    assert all(r.get('converged',True) for r in d['dimer_scan'])
    md=(OUT/'result.md').read_text(encoding='utf8')
    result=subprocess.run(['pdftotext','-layout',str(OUT/'report.pdf'),'-'],
                          capture_output=True,check=True)
    pdf=result.stdout.decode('utf8').replace('\u2212','-')
    expected=[]
    e=lambda x:f'{x:.12f}'
    s=lambda x:f'{x:.4e}'
    for r in d['small']:
        expected.extend([e(r['ed']),e(r['superblock']),s(r['difference'])])
    for r in d['projection']:
        expected.extend(s(r[k]) for k in ('dm_error','energy_error','dm_discard'))
    for r in d['boundaries']:
        expected.extend(e(r[k]) for k in ('open','periodic','difference'))
    for r in d['variance']:
        expected.extend(s(r[k]) for k in ('variance_subtraction','variance_residual','variance_tensor'))
    for r in d['dmrg']:
        expected.extend([e(r['energy']),e(r['ed_energy']),s(r['ed_error']),s(r['sweeps'][-1]['eps_max'])])
        if r['chi']==32:
            for row in r['sweeps']:
                expected.extend([e(row['energy']),s(row['ed_error']),s(row['eps_max'])])
            if r['j2']==0:
                for row in r['growth']:
                    expected.extend([e(row['energy']),e(row['energy_per_site']),s(row['eps_max']),s(row['ed_error'])])
    for r in d['mg']:
        expected.extend([e(r['ed']),e(r['exact']),s(r['residual']),e(r['overlap_squared'])])
    expected.extend(e(d['extrapolation'][k]) for k in ('slope','intercept','exact'))
    for r in d['long_chains']:
        expected.extend(e(r[k]) for k in ('energy','energy_per_site','physical_energy','norm'))
        expected.extend([s(r['difference_from_infinite']),s(r['eps_max']),s(abs(r['energy']-r['physical_energy']))])
    for r in d['dimer_scan']:
        expected.append(e(r['dimer']))
        if r['method']=='DMRG':
            expected.extend(e(x) for x in r['central_values'])
            expected.extend([e(r['energy']),e(r['ed_energy'])])
            expected.extend(s(r[k]) for k in ('dimer_error','bond_error','energy_error','eps_max'))
    scaling=d['review_analysis']['error_scaling']
    for r in scaling['inputs']:
        expected.append(f'{r["ratio"]:.6f}')
    for fit in scaling['fits'].values():
        expected.extend(f'{fit[key]:.6f}' for key in ('power','r2_log'))
    fit=scaling['fits']['eps_max']
    expected.extend(f'{fit[key]:.6f}' for key in ('amplitude','origin_slope','linear_slope','ratio_min','ratio_max'))
    expected.extend([e(fit['extrapolated_energy']),s(fit['extrapolated_error'])])
    for r in d['review_analysis']['baselines']:
        expected.append(e(r['enhancement']))
    for label,content in (('Markdown',md),('PDF',pdf)):
        missing=sorted(set(token for token in expected if token not in content))
        assert not missing,(label,missing)
    for path in ROOT.rglob('*.md'):
        content=path.read_text(encoding='utf8')
        prose=re.sub(r'```[\s\S]*?```','',content)
        assert not any(x in prose for x in (r'\(',r'\)',r'\[',r'\]')),path
        assert not any(ord(ch)<32 and ch not in '\n\r\t' for ch in content),path
        for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',content):
            if '://' not in target: assert (path.parent/target).exists(),(path,target)
    log=(OUT/'report.log').read_text(encoding='utf8',errors='replace')
    assert not any(token in log for token in ('Overfull','Underfull','Warning','Missing character',
                                             'undefined references','LaTeX Error'))
    csv_rows=list(csv.DictReader((OUT/'data'/'dimer_bonds.csv').open(encoding='utf-8-sig')))
    index={(int(row['N']),float(row['J2']),row['method'],int(row['bond_j'])):row for row in csv_rows}
    csv_count=0
    for r in d['dimer_scan']:
        for j,value in enumerate(r['nearest']):
            row=index[(r['n'],r['j2'],r['method'],j)]
            assert abs(float(row['nearest_correlation'])-value)<1e-14
            csv_count+=1
    assert len(csv_rows)==csv_count
    baseline_rows=list(csv.DictReader((OUT/'data'/'dimer_baseline.csv').open(encoding='utf-8-sig')))
    assert len(baseline_rows)==len(d['review_analysis']['baselines'])
    for saved,original in zip(baseline_rows,d['review_analysis']['baselines']):
        assert int(saved['n'])==original['n'] and float(saved['j2'])==original['j2']
        assert saved['method']==original['method']
        for key in ('dimer','baseline','enhancement','direct_from_bonds'):
            assert abs(float(saved[key])-original[key])<1e-14
    mps_checks=[]
    for r in d['long_chains']:
        archive=np.load(OUT/'data'/f'mps_N{r["n"]}_J2_0.0_chi_{r["chi"]}.npz')
        tensors=[archive[key] for key in sorted(archive.files)]
        assert len(tensors)==r['n']
        meter=Measurements(tensors)
        energy=float(meter.bonds(1).sum())
        assert abs(energy-r['energy'])<5e-9
        mps_checks.append(dict(n=r['n'],chi=r['chi'],energy=energy,
                               difference=abs(energy-r['energy']),norm=meter.norm))
    tests=(OUT/'test_results.log').read_text(encoding='utf8',errors='replace')
    match=re.search(r'Ran (\d+) tests',tests)
    assert match and '\nOK' in tests,'Run regression tests and save output/test_results.log first'
    summary=dict(numerical_checks_passed=len(d['checks']),regression_tests_passed=int(match.group(1)),
        reported_numeric_tokens_checked=len(expected),unique_numeric_tokens=len(set(expected)),
        markdown_and_pdf_match_json=True,markdown_math_and_links_checked=True,latex_log_clean=True,
        dimer_csv_values_checked=csv_count,baseline_csv_rows_checked=len(baseline_rows),serialized_long_mps_checks=mps_checks,
        all_dmrg_runs_converged=True,source_data_sha256=hashlib.sha256(raw.read_bytes()).hexdigest())
    (OUT/'submission_audit.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
    print(json.dumps(summary,indent=2))


if __name__=='__main__': main()
