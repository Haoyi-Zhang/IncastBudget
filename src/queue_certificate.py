#!/usr/bin/env python3
"""Local exact queue admission and two-tenant optimality certificate interface."""
from pathlib import Path
from fractions import Fraction
import argparse,json,sys
from exact import rational
from queues import Burst,validate,shadow_fast,shadow_reference,witness,simulate
from allocation import optimize_two,verify_two

def encode(value):
    if isinstance(value,Fraction):return str(value)
    if isinstance(value,(tuple,list)):return [encode(v) for v in value]
    if isinstance(value,dict):return {k:encode(v) for k,v in value.items()}
    return value

def pairs(items):
    out={}
    for k,v in items:
        if k in out:raise ValueError('duplicate JSON key')
        out[k]=v
    return out

def load(path):
    if path.stat().st_size>2*1024**2:raise ValueError('input exceeds 2 MiB local-interface limit')
    def bad(value):raise ValueError('non-finite JSON number')
    return json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=pairs,parse_constant=bad)

def instance(data):
    bs=[Burst(**v) for v in data['bursts']]
    if len(bs)>10000:raise ValueError('local-interface burst limit exceeded')
    rates=[rational(v) for v in data['rates']];validate(bs,rates)
    C=rational(data['capacity']);floors=[rational(v) for v in data['floors']]
    if len(floors)!=len(rates) or C<0 or any(v<0 for v in floors):raise ValueError('invalid capacity/floors')
    if sum(rates)>C or any(r<g for r,g in zip(rates,floors)):raise ValueError('rates violate service contract')
    return bs,rates,C,floors

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['check','optimize','verify']);p.add_argument('input',type=Path)
    p.add_argument('certificate',type=Path,nargs='?');p.add_argument('--output',type=Path)
    args=p.parse_args()
    try:
        bs,rates,C,floors=instance(load(args.input))
        if args.action=='check':
            out=shadow_fast(bs,rates);ref=shadow_reference(bs,rates,record=True)
            if out['pool']!=ref['pool'] or out['private']!=ref['private']:raise ArithmeticError('producer/checker mismatch')
            out['attaining_releases']=witness(bs,out['time'])
            out['upper_bound_rows']=ref['trace'];out['model']='independent-windows-fixed-reservations'
        elif args.action=='optimize':
            if len(bs)>32:raise ValueError('bounded optimizer accepts at most 32 bursts')
            out=optimize_two(bs,C,floors)['certificate']
        else:
            if args.certificate is None:raise ValueError('verify requires a certificate file')
            verify_two(bs,C,floors,load(args.certificate))
            out={'valid':True,'model':'independent-windows-fixed-reservations','scope':'two-tenant exact optimum'}
        text=json.dumps(encode(out),indent=2)+'\n'
        if args.output:args.output.write_text(text,encoding='utf-8')
        else:print(text,end='')
    except (ValueError,KeyError,TypeError,OSError,ArithmeticError) as exc:
        print(f'error: {exc}',file=sys.stderr);return 2
    return 0
if __name__=='__main__':raise SystemExit(main())
