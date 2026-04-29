# Synthesis Memo - Best Practices on Synthetic Data

## Paper position (what I keep)

The strongest takeaway is that synthetic data quality is mostly a pipeline-design problem, not a model-size problem. Generation diversity, rubric quality, and post-generation filtering dominate naive scale.

## Point of disagreement

I disagree with broad recommendations that maximize synthetic diversity before domain constraints are fully encoded. For Tenacious outreach, unconstrained diversity increases fluent but commercially invalid outputs (over-commitments, unsupported claims). In this domain, constraint-first generation with narrower controlled variation should come before maximal diversity.

## Evidence against the paper's default posture

Week 10 probe categories show failures are often "good language, wrong commitment." This means realism constraints must be hard-coded earlier than some generic synthetic-data recipes suggest.

## Week 11 design decisions driven by this memo

1. Added explicit bench-availability and signal-confidence fields in each task.
2. Weighted deterministic rule checks heavily in evaluator scoring.
3. Kept adversarial hand-authored slice for edge failures under objections.

## Risk if ignored

The benchmark would over-reward style and under-penalize false operational commitments.
