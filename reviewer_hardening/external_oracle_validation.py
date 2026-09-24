from __future__ import annotations
import json, random, sys
from fractions import Fraction as F
from pathlib import Path
from .affine_minimax import AffinePiece, solve_affine_minimax, verify_certificate

def main(out:Path,seed:int=271828,cases:int=320):
    import scipy, numpy as np
    from scipy.optimize import linprog
    rng=random.Random(seed);max_gap=0.0;checked=0
    for _ in range(cases):
        n=rng.randint(2,6)
        lo=[F(rng.randint(0,2),rng.randint(1,6)) for _ in range(n)]
        slack=F(rng.randint(1,8),rng.randint(1,5));cap=sum(lo,F(0))+slack
        hi=[lo[i]+slack+F(rng.randint(0,4),rng.randint(1,6)) for i in range(n)]
        pcs=[]
        for __ in range(rng.randint(n+1,n+7)):
            pcs.append(AffinePiece.make(F(rng.randint(-9,9),rng.randint(1,8)),[F(rng.randint(-8,8),rng.randint(1,8)) for _ in range(n)]))
        cert=solve_affine_minimax(pcs,lo,hi,cap);verify_certificate(pcs,lo,hi,cap,cert)
        # Variables x_0..x_{n-1}, z; b*x-z <= -a.
        c=np.array([0.0]*n+[1.0])
        Aub=[];bub=[]
        for p in pcs:
            Aub.append([float(x) for x in p.coefficients]+[-1.0]);bub.append(-float(p.intercept))
        Aeq=np.array([[1.0]*n+[0.0]]);beq=np.array([float(cap)])
        bounds=[(float(lo[i]),float(hi[i])) for i in range(n)]+[(None,None)]
        res=linprog(c,A_ub=np.array(Aub),b_ub=np.array(bub),A_eq=Aeq,b_eq=beq,bounds=bounds,method='highs')
        assert res.success,res.message
        gap=abs(float(cert.objective)-float(res.fun));max_gap=max(max_gap,gap)
        assert gap <= 2e-8*(1+abs(float(cert.objective)))
        checked+=1
    data={'instances':checked,'max_absolute_objective_gap':max_gap,'scipy_version':scipy.__version__,'oracle':'scipy.optimize.linprog(method=highs)','authority':'exact rational certificate remains authoritative'}
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(data,indent=2),encoding='utf-8')
if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();main(a.output)
