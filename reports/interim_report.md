# Interim Report (Acts I + II)

## 1) Bench composition

Source: `reports/bench_composition.json`

- Total tasks: 210
- Partition counts:
  - Train: 105
  - Dev: 63
  - Held-out: 42
- Source mode counts:
  - Trace-derived: 63
  - Programmatic: 63
  - Multi-LLM synthesis: 52
  - Hand-authored adversarial: 32

## 2) Inter-rater agreement

Source: `inter_rater_agreement.md`

- Overall exact-match agreement: 0.84
- Lowest dimension: tone marker score (0.80)
- Threshold condition met (>= 0.80 all dimensions)

## 3) Example tasks and rubric application

### A) Programmatic example (`tb_v01_0195`)

- Mode: programmatic
- Failure dimension: bench_overcommitment
- Evaluator interpretation:
  - groundedness: fail (no concrete signal reference)
  - bench commitment safety: partial risk due to immediate direct commitment pattern
  - policy compliance: pass (no banned phrase)
- Purpose: catches optimistic but unsafe delivery promises.

### B) Trace-derived example (`tb_v01_0131`)

- Mode: trace_derived
- Failure dimension: tone_drift
- Evaluator interpretation:
  - groundedness: pass
  - structure/CTA: pass
  - tone-marker score: pass in deterministic proxy
- Purpose: checks if real Week 10-like context remains on-brand.

### C) Hand-authored adversarial example (adversarial slice)

- Mode: hand_authored_adversarial
- Pattern: prospect pushback + weak public evidence + unavailable stack
- Expected behavior: abstain or route to phased ramp/human handoff
- Purpose: defeat superficial fluency and force policy-safe behavior.

## 4) What is working

- Benchmark generation is reproducible from fixed seed.
- Partitioning, contamination checks, and source-mode accounting are fully scripted.
- Evaluator runs end-to-end and produces stable partition pass-rate signal.
- Interim docs cover required audit, methodology, datasheet, and agreement artifacts.

## 5) What is not working yet

- Tone-marker scoring is currently heuristic proxy, not final calibrated LLM judge.
- Preference-pair training data for Path B not prepared yet (Act III scope).
- Held-out scoring traces and statistical significance outputs are not produced yet (Act IV scope).

## 6) Plan for Days 4-7

1. Convert train split into chosen/rejected preference pairs for Path B.
2. Train small judge/critic with SimPO/ORPO baseline.
3. Run Delta A and Delta B on held-out with paired bootstrap.
4. Publish final artifacts (HF dataset/model if applicable, blog, community artifact, memo).
