# Methodology (Interim Draft)

## 1) Path declaration

Chosen path: **Path B (preference-tuned judge/critic)**.

### Justification from Week 10 evidence

Week 10 failures were predominantly inconsistency and self-monitoring failures: outputs were often fluent yet wrong under bench constraints or weak-signal conditions. The selected target (`bench_overcommitment`) indicates the model frequently fails to detect when it should reject or downgrade a commitment.

Evidence anchors:
- Probe IDs: `P-007`, `P-008`, `P-009` (bench over-commitment)
- Trace IDs used for rationale grounding: `tau_dev_tier_baseline_01`, `tau_dev_tier_baseline_02`, `tau_reproduction_check_02`

Paper anchors supporting Path B:
- Direct Preference Optimization (Rafailov et al.)
- SimPO / ORPO (reference-free preference optimization)
- Prometheus 2 (judge specialization)
- Preference leakage guidance (Li et al.)
- Tenacious Style Guide v2 with 12 good/12 bad labeled drafts (used as calibration corpus for tone-preservation and banned-phrase checks)

## 2) Tenacious-Bench schema dimensions

Dimensions scored per task:
1. Groundedness to provided signals
2. Bench commitment safety
3. Tone-marker fidelity (direct, grounded, honest, professional, non-condescending)
4. CTA and formatting constraints
5. Policy compliance (banned phrases, no fabricated totals)

Scoring evaluator:
- Deterministic weighted score, threshold = 78/100
- Rule-based checks for verifiable constraints
- Judge-hook placeholder for richer tone adjudication
- Rule calibration aligned to Style Guide v2:
  - tone marker threshold: regenerate if any marker < 4/5
  - banned phrase scan expanded to full v2 list
  - external "bench" wording treated as Professional-marker failure

## 3) Dataset construction plan and implementation

Target size: 210 tasks (interim executable set in required 200-300 range).

Authoring mode allocation:
- Trace-derived: 63 (~30%)
- Programmatic templates: 63 (~30%)
- Multi-LLM synthesis: 52 (~25%)
- Hand-authored adversarial: 32 (~15%)

Implementation:
- Script: `generation_scripts/build_tenacious_bench.py`
- Fixed seed: 11
- Source mode recorded in each row metadata

## 4) Partitioning protocol

Split:
- Train: 105 (50%)
- Dev: 63 (30%)
- Held-out: 42 (20%)

Stratification approach:
- First stratify by failure dimension to keep equal coverage across partitions.
- Within each dimension, stratify by source mode so each partition preserves the 30/30/25/15 composition target closely.
- Within each stratum, sample by difficulty (`easy`, `medium`, `hard`) to prevent held-out from becoming artificially easier than train.

Why this supports failure-mode coverage:
- Prevents a false lift where improvements on one dimension are hidden by imbalance.
- Ensures held-out contains all target failure families, not only high-frequency easy cases.
- Preserves adversarial examples in every partition for robustness checks.

Held-out policy:
- Partition file isolated under `tenacious_bench_v0.1/held_out/`.
- Held-out not used for train-data generation in interim workflow.

## 5) LLM routing and judge filtering protocol

Rotation policy:
- generator family must not equal judge family for the same task
- bulk quality filter uses dev-tier judge
- calibration spot-check uses eval-tier judge on sampled subset

Interim logs:
- `generation_scripts/judge_filter_log.json`
- `generation_scripts/seed_counts.json`

## 6) Contamination prevention protocol

Required checks and thresholds:
- n-gram overlap: < 8
- embedding similarity: < 0.85
- time-shift verification: pass for public-signal references

Contamination results (interim run):
- N-gram overlap check:
  - flagged candidate pairs before resolution: 25
  - resolution: 19 rewritten, 6 dropped
  - final max overlap: 0 (threshold < 8)
- Embedding similarity check:
  - flagged candidate pairs before resolution: 25 (same overlap set)
  - resolution: same rewrite/drop actions
  - final max cosine similarity: 0.79 (threshold < 0.85)
- Time-shift verification:
  - flagged tasks: 0
  - final status: pass

Final contamination status: pass.

Interim artifact:
- `contamination_check.json` (contains per-check values and resolution summary)

## 7) Inter-rater agreement protocol

Procedure:
1. Label 30 sampled tasks with rubric
2. Re-label after 24h without seeing first labels
3. If any dimension < 80% agreement, revise rubric and relabel

Current interim matrix and notes:
- `inter_rater_agreement.md`

## 8) Cost discipline log policy

All LLM and compute charges logged with:
- timestamp
- budget bucket
- purpose

Artifact:
- `cost_log.md`
