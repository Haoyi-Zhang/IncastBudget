# Independent reviewer-hardening oracles

This directory contains deliberately small, exact implementations that do **not**
import the production algorithms.

* `affine_minimax.py` enumerates exact vertices of a finite affine minimax LP,
  reconstructs rational KKT multipliers, and independently checks primal
  feasibility, multiplier signs, stationarity, complementary slackness, and
  primal/dual objective equality.
* `finite_domain_ve.py` implements a generic finite-domain max-sum variable
  elimination oracle with deterministic witness recovery. Tests compare it
  against full enumeration for binary, ternary, and four-valued domains.
* `tests/test_reviewer_hardening.py` includes randomized differential tests,
  degenerate instances, fractional data, MAX-CUT factors, and deliberately
  corrupted certificates/witnesses.

These are validation oracles, not scalability claims. Their exponential work is
intentional and is restricted to bounded test instances.
