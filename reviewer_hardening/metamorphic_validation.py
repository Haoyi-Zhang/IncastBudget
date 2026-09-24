from __future__ import annotations
import json, random
from fractions import Fraction as F
from pathlib import Path
from .affine_minimax import AffinePiece, solve_affine_minimax, verify_certificate
from .finite_domain_ve import Factor, brute_force_max, variable_elimination_max, verify_witness


def affine_suite(seed:int=90210,cases:int=160):
    rng=random.Random(seed); checked=0
    for _ in range(cases):
        n=rng.randint(2,5)
        lo=tuple(F(rng.randint(0,2),rng.randint(1,5)) for _ in range(n))
        slack=F(rng.randint(2,8),rng.randint(1,4))
        cap=sum(lo,F(0))+slack
        hi=tuple(lo[i]+slack+F(rng.randint(0,3),rng.randint(1,5)) for i in range(n))
        pieces=[]
        for __ in range(rng.randint(n+1,n+5)):
            a=F(rng.randint(-7,9),rng.randint(1,7))
            b=tuple(F(rng.randint(-6,8),rng.randint(1,7)) for _ in range(n))
            pieces.append(AffinePiece.make(a,b))
        base=solve_affine_minimax(pieces,lo,hi,cap); verify_certificate(pieces,lo,hi,cap,base)
        # Constraint permutation.
        pp=list(pieces); rng.shuffle(pp)
        perm=solve_affine_minimax(pp,lo,hi,cap); verify_certificate(pp,lo,hi,cap,perm)
        assert perm.objective==base.objective
        # Duplicate and a pointwise dominated upward piece cannot improve the minimum.
        dup=solve_affine_minimax(tuple(pieces)+(pieces[0],),lo,hi,cap)
        assert dup.objective==base.objective
        dominated=AffinePiece.make(pieces[0].intercept-F(5),pieces[0].coefficients)
        dom=solve_affine_minimax(tuple(pieces)+(dominated,),lo,hi,cap)
        assert dom.objective==base.objective
        # Common intercept translation shifts only the objective.
        c=F(rng.randint(-5,5),rng.randint(1,5))
        shifted=tuple(AffinePiece.make(p.intercept+c,p.coefficients) for p in pieces)
        sh=solve_affine_minimax(shifted,lo,hi,cap)
        assert sh.objective==base.objective+c
        # Variable permutation preserves objective.
        order=list(range(n));rng.shuffle(order)
        plo=tuple(lo[i] for i in order);phi=tuple(hi[i] for i in order)
        ppcs=tuple(AffinePiece.make(p.intercept,tuple(p.coefficients[i] for i in order)) for p in pieces)
        pv=solve_affine_minimax(ppcs,plo,phi,cap)
        assert pv.objective==base.objective
        checked+=1
    return {'instances':checked,'relations_per_instance':5,'checks':checked*5}


def phase_suite(seed:int=314159,cases:int=180):
    rng=random.Random(seed); checked=0
    for _ in range(cases):
        n=rng.randint(1,7);q=rng.randint(2,4)
        domains={i:tuple(range(q)) for i in range(n)}
        factors=[]
        for i in range(n):
            tab={(x,):rng.randint(-5,8) for x in domains[i]}
            factors.append(Factor((i,),tab))
        for i in range(n-1):
            if rng.random()<.8:
                tab={(x,y):rng.randint(-5,8) for x in domains[i] for y in domains[i+1]}
                factors.append(Factor((i,i+1),tab))
        base=brute_force_max(domains,factors)
        order=list(range(n));rng.shuffle(order)
        ve=variable_elimination_max(domains,factors,order)
        assert ve.objective==base.objective and verify_witness(domains,factors,ve.witness,ve.objective)
        # Factor permutation invariance.
        pf=list(factors);rng.shuffle(pf)
        assert brute_force_max(domains,pf).objective==base.objective
        # Add a nullary constant and check exact shift.
        c=rng.randint(-7,7)
        cf=factors+[Factor((),{():c})]
        cb=brute_force_max(domains,cf)
        assert cb.objective==base.objective+c
        # Relabel each finite domain by a cyclic permutation and transform tables.
        maps={i:{x:(x+1)%q for x in domains[i]} for i in domains}
        inv={i:{v:k for k,v in maps[i].items()} for i in maps}
        rf=[]
        for f in factors:
            tab={}
            import itertools
            for ass in itertools.product(*(domains[v] for v in f.scope)):
                old=tuple(inv[v][ass[j]] for j,v in enumerate(f.scope))
                tab[ass]=f.table[old]
            rf.append(Factor(f.scope,tab))
        assert brute_force_max(domains,rf).objective==base.objective
        checked+=1
    return {'instances':checked,'relations_per_instance':4,'checks':checked*4}


def main(out:Path):
    data={'affine':affine_suite(),'finite_domain':phase_suite()}
    data['total_checks']=sum(x['checks'] for x in data.values())
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(data,indent=2),encoding='utf-8')

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();main(a.output)
