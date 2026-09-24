#!/usr/bin/env python3
"""Run the independent reviewer-hardening validation suite."""
from __future__ import annotations
import argparse, subprocess, sys
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,default=Path('results/reviewer-hardening')); a=ap.parse_args()
    root=Path(__file__).resolve().parent
    subprocess.run([sys.executable,'-m','unittest','-v','tests.test_reviewer_hardening','tests.test_reviewer_hardening_adversarial'],cwd=root,check=True)
    subprocess.run([sys.executable,str(root/'reviewer_hardening'/'run_validation.py'),'--output',str(a.output.resolve())],cwd=root,check=True)
if __name__=='__main__': main()
