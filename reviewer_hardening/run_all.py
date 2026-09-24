from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path

def run(cmd, cwd):
    p=subprocess.run(cmd,cwd=cwd,check=True,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    return {'command':cmd,'output_tail':p.stdout[-4000:]}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,default=Path('results/reviewer-hardening/all'))
    ap.add_argument('--include-external-oracle',action='store_true')
    a=ap.parse_args();root=Path(__file__).resolve().parents[1];out=(root/a.output).resolve() if not a.output.is_absolute() else a.output
    out.mkdir(parents=True,exist_ok=True);runs=[]
    runs.append(run([sys.executable,'reproduce_review.py','--output',str(out/'differential')],root))
    runs.append(run([sys.executable,'-m','reviewer_hardening.metamorphic_validation','--output',str(out/'metamorphic.json')],root))
    if a.include_external_oracle:
        runs.append(run([sys.executable,'-m','reviewer_hardening.external_oracle_validation','--output',str(out/'external-oracle.json')],root))
    manifest={'status':'PASS','external_oracle_included':a.include_external_oracle,'runs':runs}
    (out/'run-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
if __name__=='__main__':main()
