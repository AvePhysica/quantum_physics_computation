"""Postprocessing only: error/discard scaling and finite-size baseline differences."""
import numpy as np


def affine(x,y):
    """Closed-form least squares, independently audited against a scaled solve."""
    x=np.asarray(x,dtype=float); y=np.asarray(y,dtype=float)
    dx=x-x.mean(); dy=y-y.mean()
    if len(x)<2 or np.dot(dx,dx)==0: raise ValueError('Distinct samples required')
    slope=float(np.dot(dx,dy)/np.dot(dx,dx)); intercept=float(y.mean()-slope*x.mean())
    fit=slope*x+intercept
    r2=float(1-np.sum((y-fit)**2)/np.sum(dy**2)) if np.sum(dy**2)>0 else 1.
    scale=float(np.max(abs(x)))
    independent=np.linalg.lstsq(np.column_stack([x/scale,np.ones(len(x))]),y,rcond=None)[0]
    return slope,intercept,r2,float(independent[0]/scale),float(independent[1])


def scaling_fit(epsilon,errors,signed_errors=None):
    x=np.asarray(epsilon,dtype=float); y=np.asarray(errors,dtype=float)
    if x.shape!=y.shape or x.ndim!=1 or np.any(x<=0) or np.any(y<=0):
        raise ValueError('Matching one-dimensional strictly positive samples required')
    p,log_a,r2,other_p,other_log_a=affine(np.log(x),np.log(y))
    signed=y if signed_errors is None else np.asarray(signed_errors,dtype=float)
    if signed.shape!=y.shape: raise ValueError('Signed energy errors must match samples')
    slope,intercept,_,other_slope,other_intercept=affine(x,signed)
    return dict(power=p,amplitude=float(np.exp(log_a)),r2_log=r2,
        origin_slope=float(np.dot(x,y)/np.dot(x,x)),
        linear_slope=slope,linear_intercept=intercept,
        ratio_min=float(np.min(y/x)),ratio_max=float(np.max(y/x)),
        independent_power_difference=abs(p-other_p),
        independent_log_amplitude_difference=abs(log_a-other_log_a),
        independent_r2_difference=abs(r2-float(np.corrcoef(np.log(x),np.log(y))[0,1]**2)),
        independent_intercept_difference=abs(intercept-other_intercept),
        independent_slope_difference=abs(slope-other_slope))


def baseline_subtraction(scan):
    """D(J)-D(0), same N/method/chi. Do not interchange abs and subtraction."""
    key=lambda row:(row['n'],row['method'],row.get('chi'))
    anchors={key(row):row for row in scan if row['j2']==0}
    out=[]
    for row in scan:
        base=anchors[key(row)]
        direct=abs(row['central_values'][0]-row['central_values'][1])-abs(base['central_values'][0]-base['central_values'][1])
        out.append(dict(n=row['n'],j2=row['j2'],method=row['method'],chi=row.get('chi'),
            baseline=base['dimer'],dimer=row['dimer'],enhancement=row['dimer']-base['dimer'],
            direct_from_bonds=float(direct)))
    return out


def enrich(data):
    def length(row):
        return row.get('n',row['growth'][-1]['n'] if row.get('growth') else None)
    rows=[r for r in data['dmrg'] if length(r)==20 and r['j2']==0 and r['chi'] in (4,8,16,32)]
    if len(rows)!=4 or sorted(r['chi'] for r in rows)!=[4,8,16,32]:
        raise ValueError('Need one N=20 J2=0 run for each chi=4,8,16,32')
    rows.sort(key=lambda r:r['chi'])
    inputs=[dict(chi=r['chi'],error=r['ed_error'],energy=r['energy'],
                 eps_max=r['sweeps'][-1]['eps_max'],eps_centre=r['sweeps'][-1]['eps_centre'],
                 ratio=r['ed_error']/r['sweeps'][-1]['eps_max']) for r in rows]
    errors=[r['error'] for r in inputs]
    signed=[r['energy']-r['ed_energy'] for r in rows]
    fits={key:scaling_fit([r[key] for r in inputs],errors,signed_errors=signed) for key in ('eps_max','eps_centre')}
    for fit in fits.values():
        fit['extrapolated_energy']=rows[0]['ed_energy']+fit['linear_intercept']
        fit['extrapolated_error']=abs(fit['linear_intercept'])
    baselines=baseline_subtraction(data['dimer_scan'])
    data['review_analysis']=dict(complete=True,error_scaling=dict(n=20,j2=0,chi=[4,8,16,32],
        epsilon_definition='maximum discarded weight in last complete sweep',inputs=inputs,fits=fits),
        baseline_definition='abs(C_left(J2)-C_right(J2)) - abs(C_left(0)-C_right(0)), same N/method/chi',
        baselines=baselines,phase_reference=dict(critical_ratio_approx=.2411,
            source='https://arxiv.org/abs/cond-mat/9602126',
            transition_source='https://doi.org/10.1088/0305-4470/27/17/012'),
        scaling_source='https://arxiv.org/abs/cond-mat/0508709')
    data['checks']=[r for r in data['checks'] if r.get('section')!='review_analysis']
    def check(name,target,expected,measured,tolerance):
        passed=bool(abs(measured-expected)<=tolerance)
        data['checks'].append(dict(name=name,target=target,expected=float(expected),measured=float(measured),
                                  tolerance=tolerance,passed=passed,section='review_analysis'))
        if not passed: raise AssertionError(f'{name}: {measured} != {expected}')
    for name,fit in fits.items():
        for field in ('independent_power_difference','independent_log_amplitude_difference',
                      'independent_r2_difference','independent_intercept_difference','independent_slope_difference'):
            check('scaling '+name+' '+field,'incorrect fit coordinates, coefficient or intercept',0,fit[field],1e-10)
    for row in baselines:
        check(f'baseline N={row["n"]} J2={row["j2"]} {row["method"]}',
              'mixing sizes/methods or swapping absolute value and baseline subtraction',
              row['direct_from_bonds'],row['enhancement'],2e-13)
    return data
