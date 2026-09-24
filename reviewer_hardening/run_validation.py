#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, platform, random, sys, time
from dataclasses import asdict
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path

from reviewer_hardening.affine_minimax import AffinePiece, MinimaxCertificate, solve_exact_minimax, verify_minimax_certificate
from reviewer_hardening.finite_domain_ve import Factor, brute_force_max, variable_elimination_max, verify_assignment


def fs(x): return f"{x.numerator}/{x.denominator}"


def independent_two_tenant_oracle(pieces, lower, upper, cap):
    lo=max(lower[0],cap-upper[1]); hi=min(upper[0],cap-lower[1])
    candidates={lo,hi}
    lines=[]
    for p in pieces:
        c=p.intercept+p.slope[1]*cap; d=p.slope[0]-p.slope[1]; lines.append((c,d))
    for (c1,d1),(c2,d2) in combinations(lines,2):
        if d1!=d2:
            x=(c2-c1)/(d1-d2)
            if lo<=x<=hi: candidates.add(x)
    scored=[]
    for x in candidates:
        rates=(x,cap-x); z=max(p.intercept+sum(a*b for a,b in zip(p.slope,rates)) for p in pieces)
        scored.append((z,rates))
    return min(scored)


def run_affine(rng):
    rows=[]; mutation_attempts=0; mutation_rejections=0
    for n in range(2,6):
        for case in range(60):
            cap=F(rng.randint(n,3*n),rng.choice((1,2,3)))
            lower=[F(0)]*n; upper=[cap]*n
            pieces=[AffinePiece.make(F(rng.randint(-8,14),rng.choice((1,2,3,5))),
                     [F(rng.randint(-5,3),rng.choice((1,2,3,5))) for _ in range(n)],f"p{k}") for k in range(n+4)]
            t=time.perf_counter(); cert=solve_exact_minimax(pieces,lower,upper,cap); elapsed=time.perf_counter()-t
            ok,errors=verify_minimax_certificate(pieces,lower,upper,cap,cert)
            if not ok: raise AssertionError(errors)
            if n==2:
                oz,ox=independent_two_tenant_oracle(pieces,lower,upper,cap)
                if oz!=cert.value: raise AssertionError((oz,cert.value,ox,cert.rates))
            mutations=[
              MinimaxCertificate(cert.rates,cert.value+F(1,97),cert.piece_multipliers,cert.lower_multipliers,cert.upper_multipliers,cert.equality_multiplier),
              MinimaxCertificate(tuple([cert.rates[0]+F(1,101)]+list(cert.rates[1:])),cert.value,cert.piece_multipliers,cert.lower_multipliers,cert.upper_multipliers,cert.equality_multiplier),
              MinimaxCertificate(cert.rates,cert.value,tuple(-x for x in cert.piece_multipliers),cert.lower_multipliers,cert.upper_multipliers,cert.equality_multiplier),
            ]
            for bad in mutations:
                mutation_attempts+=1
                if not verify_minimax_certificate(pieces,lower,upper,cap,bad)[0]: mutation_rejections+=1
            rows.append({'n':n,'case':case,'pieces':len(pieces),'capacity':fs(cap),'value':fs(cert.value),'active_piece_multipliers':sum(x!=0 for x in cert.piece_multipliers),'seconds':elapsed})
    if mutation_attempts!=mutation_rejections: raise AssertionError('a corrupted minimax certificate was accepted')
    return rows,{'instances':len(rows),'mutation_attempts':mutation_attempts,'mutation_rejections':mutation_rejections}


def cycle_instance(rng,n,q):
    domains={i:tuple(range(q)) for i in range(n)}; factors=[]
    if n==1:
        scope=(0,); factors.append(Factor(scope,{(x,):F(rng.randint(-9,9),rng.choice((1,2,3))) for x in domains[0]},'unary'))
    else:
        for i in range(n):
            scope=(i,(i+1)%n)
            factors.append(Factor(scope,{vals:F(rng.randint(-9,9),rng.choice((1,2,3))) for vals in product(*(domains[v] for v in scope))},f'e{i}'))
    return domains,factors


def run_ve(rng):
    rows=[]; mutation_attempts=0; mutation_rejections=0
    for q in (2,3,4):
        for n in range(1,8):
            for case in range(18):
                d,f=cycle_instance(rng,n,q)
                t=time.perf_counter(); bv,ba=brute_force_max(d,f); brute_t=time.perf_counter()-t
                order=tuple(range(n)); t=time.perf_counter(); tr=variable_elimination_max(d,f,order); ve_t=time.perf_counter()-t
                if tr.objective!=bv or not verify_assignment(d,f,tr.assignment,bv): raise AssertionError('VE/brute-force disagreement')
                bad=dict(tr.assignment); v=next(iter(d)); bad[v]=max(d[v])+1  # guaranteed out of domain
                mutation_attempts+=2
                mutation_rejections+=int(not verify_assignment(d,f,bad,bv))
                mutation_rejections+=int(not verify_assignment(d,f,tr.assignment,bv+F(1,103)))
                rows.append({'domain':q,'n':n,'case':case,'objective':fs(bv),'induced_width':tr.induced_width,'max_table_entries':tr.max_table_entries,'bruteforce_seconds':brute_t,'ve_seconds':ve_t})
    # Scalability sanity check on a long path; no brute force.
    n=96; q=3; d={i:tuple(range(q)) for i in range(n)}; f=[]
    for i in range(n-1):
        scope=(i,i+1); f.append(Factor(scope,{vals:F((vals[0]-vals[1])**2) for vals in product(*(d[v] for v in scope))},f'p{i}'))
    tr=variable_elimination_max(d,f,tuple(range(n)))
    if tr.induced_width!=1 or not verify_assignment(d,f,tr.assignment,tr.objective): raise AssertionError('path scaling check failed')
    if mutation_attempts!=mutation_rejections: raise AssertionError('a corrupted phase witness was accepted')
    return rows,{'differential_instances':len(rows),'mutation_attempts':mutation_attempts,'mutation_rejections':mutation_rejections,'long_path_variables':n,'long_path_domain':q,'long_path_induced_width':tr.induced_width,'long_path_max_table_entries':tr.max_table_entries,'long_path_objective':fs(tr.objective)}


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,required=True); ap.add_argument('--seed',type=int,default=20260920); a=ap.parse_args(); a.output.mkdir(parents=True,exist_ok=True)
    rng=random.Random(a.seed); affine,asum=run_affine(rng); ve,vsum=run_ve(rng)
    for name,rows in [('affine-minimax-cases.csv',affine),('finite-domain-ve-cases.csv',ve)]:
        with (a.output/name).open('w',newline='') as fh:
            w=csv.DictWriter(fh,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    scientific={'schema_version':1,'seed':a.seed,'affine_summary':asum,'ve_summary':vsum}
    runtime={'python':sys.version,'platform':platform.platform(),'affine_total_seconds':sum(r['seconds'] for r in affine),'ve_total_seconds':sum(r['ve_seconds'] for r in ve),'bruteforce_total_seconds':sum(r['bruteforce_seconds'] for r in ve)}
    (a.output/'scientific-summary.json').write_text(json.dumps(scientific,indent=2,sort_keys=True))
    (a.output/'runtime-environment.json').write_text(json.dumps(runtime,indent=2,sort_keys=True))
    lines=['# Independent exact-validation results','',f"Deterministic seed: `{a.seed}`",'',
      f"- Exact affine minimax instances: **{asum['instances']}**",f"- Corrupted minimax certificates rejected: **{asum['mutation_rejections']}/{asum['mutation_attempts']}**",f"- Finite-domain VE vs. full-enumeration instances: **{vsum['differential_instances']}**",f"- Corrupted phase witnesses rejected: **{vsum['mutation_rejections']}/{vsum['mutation_attempts']}**",f"- Long-path check: {vsum['long_path_variables']} variables, domain {vsum['long_path_domain']}, induced width {vsum['long_path_induced_width']}",'',
      'The affine oracle uses exact vertex enumeration and an exact KKT checker. Two-tenant cases are cross-checked by a separate one-dimensional breakpoint oracle. The phase oracle uses a generic factor-table representation and is cross-checked against full assignment enumeration. Timings are diagnostic only and are kept outside the scientific summary.']
    (a.output/'README.md').write_text('\n'.join(lines)+'\n')

if __name__=='__main__': main()
