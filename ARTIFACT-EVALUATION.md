# Artifact evaluation guide

## Minimal path

```bash
python3 -m unittest discover -s tests -v
python3 reproduce.py --part first  --output /tmp/incast-main
python3 reproduce.py --part second --output /tmp/incast-main
python3 reproduce_review.py --output /tmp/incast-review
```

The first two reproduction commands regenerate the manuscript-facing evidence.
The last command runs independent exact oracles, differential checks, fractional
and degenerate cases, and certificate/witness mutation tests.

## What a successful run establishes

A successful run establishes that the supplied implementation agrees with its
bounded exact oracles on the recorded inputs; that serialized certificates pass
exact checkers; that selected malformed certificates are rejected; and that the
published result tables can be regenerated from local source and data.

It does **not** establish that an untested theorem is true, that the model matches
a particular production network, or that the paper has passed independent peer
review.

## Expected outputs

* `results/` — manuscript-facing scientific results;
* `results/reviewer-hardening/scientific-summary.json` — deterministic new
  validation counts and conclusions;
* `results/reviewer-hardening/*.csv` — every generated exact case;
* `results/reviewer-hardening/runtime-environment.json` — diagnostic timings and
  environment, deliberately separated from scientific conclusions;
* `audit/reviewer-hardening/` — reference, source, PDF, and package audits.

## Failure interpretation

Any nonzero exit is a failed artifact gate.  Do not copy an older result over a
failed run.  Bibliographic network failures are recorded separately because the
scientific reproduction is offline; an identity mismatch is a hard reference
gate, while a transient network failure is explicit unresolved metadata reachability.
