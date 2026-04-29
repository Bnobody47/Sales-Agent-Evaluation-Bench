# Generation Scripts (Acts I + II)

## Contents

- `build_tenacious_bench.py` - deterministic generator for benchmark partitions and reports
- `seed_counts.json` - generated counts by source mode and partition
- `judge_filter_log.json` - routing and filtering metadata
- `ROUTING_POLICY.md` - explicit model routing rationale
- `prompts/judge_pointwise_prompt.md` - pointwise prompt
- `prompts/judge_pairwise_prompt.md` - pairwise prompt

## Routing design (interim)

- Frontier-class model role: hard-seed authoring for difficult cases
- Dev-tier model role: high-volume variation generation
- Dev-tier judge role: bulk filter scoring
- Eval-tier judge role: calibration spot checks only

Policy: generator model family must differ from judge family for each task batch.

Judge filter thresholds:
- input coherence >= 3/5
- ground-truth verifiability >= 3/5
- rubric-application clarity >= 3/5

Near-duplicate handling:
- run pairwise comparison for candidate pairs
- keep the candidate with stronger aggregate judge utility

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
