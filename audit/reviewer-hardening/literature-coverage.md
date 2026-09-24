# Literature coverage gate

This gate checks actual manuscript use, bibliographic identity hygiene, and the calibration counts required by the project brief. It does not substitute citation identity for a novelty judgment.

- Bibliography entries: **62**
- Unique cited entries: **61**
- TPDS entries cited: **0**
- Systems/network venue entries cited: **33**
- Topically adjacent entries cited: **44**
- Entries with stable identifiers: **16/61**

## Gates

- PASS: `at_least_50_unique_citations`
- FAIL: `all_bib_entries_used`
- PASS: `no_missing_keys`
- FAIL: `at_least_12_tpds`
- PASS: `at_least_5_systems_venues`
- PASS: `at_least_5_topically_adjacent`
- FAIL: `all_cited_have_stable_identifier`
- FAIL: `no_placeholders`
- PASS: `no_implausible_years`
- PASS: `no_duplicate_doi`
- PASS: `no_duplicate_title`

## Interpretation limits

Venue and keyword categories are transparent coverage checks, not impact scores. The separate metadata verifier records DOI/URL/ISBN resolution and retains network failures rather than silently treating them as verified. Novelty still depends on claim-level comparison in the manuscript and supplement.
