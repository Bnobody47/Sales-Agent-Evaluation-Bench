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

Held-out policy:
- Partition file isolated under `tenacious_bench_v0.1/held_out/`
- Held-out not used for train-data generation in interim workflow

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

Interim artifact:
- `contamination_check.json` (current result: pass)

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
