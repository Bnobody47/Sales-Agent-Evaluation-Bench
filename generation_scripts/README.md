# Generation Scripts (Acts I + II)

## Contents

- `build_tenacious_bench.py` - deterministic generator for benchmark partitions and reports
- `seed_counts.json` - generated counts by source mode and partition
- `judge_filter_log.json` - routing and filtering metadata

## Routing design (interim)

- Frontier-class model role: hard-seed authoring for difficult cases
- Dev-tier model role: high-volume variation generation
- Dev-tier judge role: bulk filter scoring
- Eval-tier judge role: calibration spot checks only

Policy: generator model family must differ from judge family for each task batch.

## Dedup logic

Current dedup signal:
- synthetic hash uniqueness across generated rows
- overlap checks against held-out split via hash and threshold policies

Threshold checks:
- max n-gram overlap < 8
- max embedding similarity < 0.85
- time-shift verification pass

## Re-run

`python generation_scripts/build_tenacious_bench.py`
