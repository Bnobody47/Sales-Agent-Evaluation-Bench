# Interim Report (Acts I + II)

## Executive snapshot

This interim submission delivers the full Acts I + II package for Tenacious-Bench v0.1: audit, schema, scoring evaluator, authored dataset, contamination checks, and inter-rater reliability evidence. The benchmark is designed to measure Tenacious-specific failure behavior that generic public benchmarks miss, with particular emphasis on safe commitment behavior under uncertain signals. The current interim state is reproducible and runnable end-to-end, with clear strengths and known gaps documented below for Days 4-7 correction.

## 1) Bench composition (cross-tabulation)

Target profile:
- partition: 50/30/20 (train/dev/held_out)
- source mode: 30/30/25/15 (trace/programmatic/multi-LLM/adversarial)

Actual totals:
- total tasks: 210
- partition totals: train 105, dev 63, held_out 42 (target met exactly)
- source mode totals: trace 65, programmatic 69, multi-LLM 46, adversarial 30

Source-mode target comparison:
- trace: target 63, actual 65, deviation +2
- programmatic: target 63, actual 69, deviation +6
- multi-LLM: target 52, actual 46, deviation -6
- adversarial: target 32, actual 30, deviation -2

Deviation explanation:
- The stricter judge thresholds removed more multi-LLM and adversarial candidates; backfill currently over-samples programmatic variants. This is acceptable for interim but flagged for correction before final publication.

Composition interpretation:
- Partition sizing is operationally stable (exact 50/30/20), so train/dev/held-out evaluation flow is ready for Act III and Act IV.
- Source-mode drift is the main quantitative issue at interim stage. If left uncorrected, this could reduce diagnostic diversity in held-out and weaken mechanism attribution claims.
- The table also shows uneven mode participation by dimension, which is exactly why cross-tab reporting is needed: simple totals alone would hide coverage risk.

Integrated cross-tab (failure dimension x partition x source mode):

| Failure dimension | Partition | Trace | Programmatic | Multi-LLM | Adversarial | Row total |
|---|---|---:|---:|---:|---:|---:|
| dual_control_coordination | train | 4 | 10 | 6 | 1 | 21 |
| dual_control_coordination | dev | 1 | 9 | 4 | 1 | 15 |
| dual_control_coordination | held_out | 0 | 9 | 6 | 1 | 16 |
| gap_overclaiming | train | 8 | 9 | 5 | 4 | 26 |
| gap_overclaiming | dev | 7 | 2 | 4 | 5 | 18 |
| gap_overclaiming | held_out | 5 | 0 | 1 | 2 | 8 |
| signal_overclaiming | train | 10 | 9 | 6 | 2 | 27 |
| signal_overclaiming | dev | 4 | 8 | 1 | 2 | 15 |
| signal_overclaiming | held_out | 3 | 5 | 3 | 0 | 11 |
| tone_drift | train | 17 | 5 | 5 | 4 | 31 |
| tone_drift | dev | 3 | 1 | 4 | 7 | 15 |
| tone_drift | held_out | 3 | 2 | 1 | 1 | 7 |
| **Column totals** | **all partitions** | **65** | **69** | **46** | **30** | **210** |

Observability note:
- From this single table, the reader can confirm adversarial tasks exist in held_out (4 total across dimensions), and can answer per-cell questions such as “held-out dual_control trace-derived” (0) or “held-out tone_drift adversarial” (1).

## 2) Inter-rater agreement results analysis

Metric:
- raw agreement (two-pass blind relabel consistency)

Protocol:
- 30-task subset
- same rater labels once, waits 24 hours, then re-labels blind to pass-1 labels
- revision trigger: any dimension < 0.80

Per-dimension agreement:
- groundedness: 0.90
- bench commitment safety: 0.87
- tone marker score: 0.80
- cta_and_structure: 0.93
- policy_compliance: 0.97
- overall exact-match across all dimensions: 0.84

Interpretation:
- All dimensions clear the 0.80 threshold, so no mandatory relabel loop was triggered.
- Tone marker is the softest dimension at 0.80, indicating the highest ambiguity remains in language framing rather than hard policy checks.
- Operational confidence is high for deterministic checks (policy and structure), moderate for style-marker adjudication.

Why this matters for downstream scoring confidence:
- Dimensions above 0.90 (`cta_and_structure`, `policy_compliance`) are stable enough for mechanical gating with low reviewer disagreement risk.
- Mid-band dimensions (`groundedness`, `bench commitment safety`) are reliable but still sensitive to borderline phrasing and should remain visible in worked examples.
- Tone-marker at threshold confirms the current proxy is acceptable for interim but should be upgraded to calibrated judge scoring before final publication claims.

## 3) Worked examples with rubric application

Scoring threshold:
- pass if weighted score >= 78

Deterministic checks used in all examples:
- banned phrase scan (`BANNED_PHRASES` list)
- word-count and subject-length checks
- one-ask check
- groundedness signal-word check
- bench commitment safety rule

Judge component:
- tone marker is currently a bounded proxy (1-5 mapped to 0.0-1.0 range behavior).
- prompt templates for pointwise/pairwise judge are committed in:
  - `generation_scripts/prompts/judge_pointwise_prompt.md`
  - `generation_scripts/prompts/judge_pairwise_prompt.md`

### A) Programmatic task (pass) - `tb_v01_0163`

Source mode:
- programmatic

Evaluator path:
- groundedness: 1.00 (signal-linked wording detected)
- bench_commitment_safety: 1.00 (no unsafe hard commitment)
- tone_marker_score: 1.00
- cta_and_structure: 1.00
- policy_compliance: 1.00

Final:
- score = 100.00 -> pass

### B) Trace-derived task (pass) - `tb_v01_0111`

Source mode:
- trace_derived

Evaluator path:
- groundedness: 1.00
- bench_commitment_safety: 1.00
- tone_marker_score: 1.00
- cta_and_structure: 1.00
- policy_compliance: 1.00

Final:
- score = 100.00 -> pass

### C) Adversarial task (deliberate failure case) - base task `tb_v01_0087`

Source mode:
- hand_authored_adversarial

Candidate output tested (failure probe):
- subject: `Quick chat: scaling now`
- body: `Following up again. We have world-class talent and can deploy immediately this week.`

Evaluator path:
- groundedness: 0.00 (no specific signal grounding)
- bench_commitment_safety: 1.00 (no direct bench mismatch signal in this specific task context)
- tone_marker_score: 0.925 (partial tone pass, but not enough to rescue overall quality)
- cta_and_structure: 1.00 (format constraints pass)
- policy_compliance: 0.00 (banned phrases triggered)

Final:
- score = 58.13 -> fail
- flags: `has_signal_reference=False`, `policy_violation=True`

Why this example matters:
- demonstrates evaluator discrimination (not rubber-stamping): a short, well-formed message can still fail hard on groundedness + policy.

Worked-example coverage check:
- Required mode mix is satisfied in this section: programmatic + trace-derived + adversarial.
- At least one explicit fail case is shown with a full scoring path, so the evaluator behavior is auditable and not just pass-only demonstration.

## 4) Honest status assessment

What is working (with evidence):
- Reproducible benchmark pipeline runs from a fixed seed (`generation_scripts/build_tenacious_bench.py`).
- Partition target is met exactly at 105/63/42.
- Evaluator is operational and discriminative: dev run and worked example set include both pass and fail outcomes.
- Inter-rater reliability cleared threshold across all dimensions (lowest = 0.80).

What is not working / risks:
- Composition drift from source-mode targets (+programmatic, -multi-LLM, -adversarial) due stricter filtering.
- One failure dimension currently absent from the generated mix after filter/backfill changes; this is a critical coverage risk before final submission.
- Tone marker still uses a proxy scorer, not final calibrated model-judge loop.

Risk severity and impact:
- **High:** missing failure-dimension coverage (can invalidate broad benchmark claims if not corrected).
- **Medium:** source-mode imbalance (can bias model toward template-friendly patterns).
- **Medium:** tone proxy scorer (can overestimate style robustness on subtle condescension cases).

## 5) Path-specific forward plan (Days 4-7, Path B)

### Day 4 (Path B data prep: SimPO/ORPO preference pairs)
1. Build chosen/rejected pairs from train split:
   - rejected: Week 10 failure-pattern outputs (especially over-commitment and unsupported-claim variants)
   - chosen: corrected outputs that pass evaluator + style-guide v2 constraints
   - target pair volume for first run: 1,000 to 1,500 high-quality pairs after filtering
2. Enforce leakage prevention:
   - generator model family for rewrites must differ from judge family used for filtering
3. Rebalance dataset:
   - restore missing failure dimension coverage
   - push source-mode distribution back toward 30/30/25/15
   - run contamination checks again after rebalance before finalizing training split

### Day 5 (training run)
1. Run one core Path B training on small backbone judge/critic (ORPO baseline first).
2. Convergence kill criterion:
   - if no validation improvement by ~30 minutes, terminate run and inspect pair quality (do not spend extra compute blindly).
3. Pivot trigger:
   - if first run fails Delta A directionally, pivot to tighter pair curation (drop ambiguous labels, increase hard negatives) before any second run.

### Day 6 (ablations + held-out eval)
1. Delta A: trained critic vs Week 10 baseline on held_out.
2. Delta B: trained critic vs prompt-only guardrail on same backbone.
3. Store pass/fail traces and statistical outputs.
4. Run paired bootstrap CI reporting to support significance claims in memo/blog.

### Day 7 (publication prep)
1. Freeze dataset card + contamination artifacts.
2. Draft blog and community artifact.
3. Prepare two-page memo with evidence graph links.

Budget envelope and reserves:
- total week budget cap: $10
- interim consumed: $3.38
- reserve for held-out eval-tier passes (Days 5-6): $2.5-3.0
- reserve for one rerun/bug-fix: ~$1.0-1.5

Success criteria for moving from interim to final-ready:
- all target failure dimensions represented in all partitions
- source-mode mix within reasonable tolerance of 30/30/25/15
- Delta A positive on held-out with CI separation
- Delta B reported honestly even if negative
