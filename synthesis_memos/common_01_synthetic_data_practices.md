# Synthesis Memo - Best Practices on Synthetic Data

## Paper position (what I keep)

The strongest takeaway is that synthetic data quality is mostly a pipeline-design problem, not a model-size problem. Generation diversity, rubric quality, and post-generation filtering dominate naive scale.

## Point of disagreement

Specific design choice I disagree with: prioritizing broad diversity early in authoring before hard domain constraints are encoded (data-diversity emphasis, Section 4; operational recommendations, Section 6). For Tenacious outreach, unconstrained diversity increases fluent but commercially invalid outputs (over-commitments, unsupported claims). In this domain, constraint-first generation with narrower controlled variation should come before maximal diversity.

## Evidence against the paper's default posture

Week 10 evidence:
- Probes `P-007`, `P-008`, `P-009`: over-commitment under bench mismatch.
- Probes `P-004`, `P-005`, `P-006`: unsupported claims under weak public signal.
- Traces `tau_dev_tier_baseline_01`, `tau_dev_tier_baseline_02`, `tau_reproduction_check_02`: fluent language but policy-invalid commitments.

This evidence contradicts an "expand diversity first" pipeline for this domain. The failure mechanism appears before phrasing diversity matters.

## Week 11 design decisions driven by this memo

1. Added explicit bench-availability and signal-confidence fields in each task.
2. Weighted deterministic rule checks heavily in evaluator scoring.
3. Kept adversarial hand-authored slice for edge failures under objections.

## Risk if ignored

The benchmark would over-reward style and under-penalize false operational commitments.
