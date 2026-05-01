# Datasheet for Tenacious-Bench v0.1 (Interim)

## Motivation

Tenacious-Bench v0.1 is designed to evaluate sales-agent behavior that generic public benchmarks miss: bench realism, signal-grounded outreach, style-guide fidelity, and conversion-safe interaction control. The benchmark is meant for Week 11 model-improvement experiments on Tenacious-specific failure modes, with initial focus on bench over-commitment.

## Composition

- Total tasks: 210
- Partitions:
  - train: 105
  - dev: 63
  - held_out: 42
- Authoring modes:
  - trace-derived: 63
  - programmatic templates: 63
  - multi-LLM synthesis: 52
  - hand-authored adversarial: 32
- Main dimensions: bench_overcommitment, tone_drift, signal_overclaiming, gap_overclaiming, dual_control_coordination

Failure-dimension counts:
- bench_overcommitment: 42
- tone_drift: 42
- signal_overclaiming: 42
- gap_overclaiming: 42
- dual_control_coordination: 42

Per-mode examples:
- Trace-derived: task reconstructed from Week 10 run behavior where agent made an unsafe commitment under weak confidence.
- Programmatic: template-expanded task where stack, headcount, confidence, and bench state are swept combinatorially.
- Multi-LLM synthesis: hard seed authored by frontier family then diversified by dev-tier model, judge-filtered for rubric clarity.
- Hand-authored adversarial: manually written edge case that forces abstain/handoff behavior under mixed constraints.

## Collection Process

Source materials:
- Week 10 trace and probe artifacts
- Tenacious style guide, bench summary, pricing and case-study seed documents
- programmatic prompt templates for controlled variation

Collection strategy:
- mixed authoring mode generation with deterministic seed
- judge filtering prior to inclusion
- metadata retained for source mode and synthetic hash

## Preprocessing / Cleaning / Labeling

- standardized JSONL task schema (`schema.json`)
- deterministic field normalization by script
- rubric attached per task
- contamination checks before held-out sealing:
  - n-gram overlap
  - embedding-similarity threshold
  - time-shift verification

## Uses

Intended uses:
- evaluate Week 10 baseline and Week 11 interventions on Tenacious-specific failure
- compare trained intervention vs prompt-only intervention
- produce reproducible delta metrics for internal decisioning

Out-of-scope uses:
- direct production truth labels for all industries
- legal/compliance decision automation without human review

## Limitations and Biases

1. **Synthetic-construction bias**
- A large portion of tasks are synthetic or synthetic-augmented. Even with trace-derived seeds, task phrasing may over-represent benchmark-style prompt structures and under-represent true inbox variance.

2. **Public-signal lossiness**
- Ground truth is constrained to publicly observable hiring and company signals. Some high-value internal context (board pressure, private staffing realities, confidential roadmap shifts) is unavailable and therefore ungraded.

3. **Judge-policy bias**
- The benchmark intentionally encodes Tenacious style policy (e.g., banned phrases, non-condescending framing). This improves domain alignment but may penalize stylistic variants that are acceptable outside this workflow.

4. **Model-family filtering bias**
- Judge filtering and anti-leakage rotation reduce contamination risk but can also produce selective retention of examples that score well under current filter logic.

5. **Temporal drift risk**
- Market language and hiring patterns shift over time; tasks tied to a prior signal window can age, reducing diagnostic value if not refreshed.

Mitigations used:
- contamination checks across held-out vs train/dev,
- inter-rater protocol with rubric revision notes,
- explicit versioning and maintenance plan for periodic refresh.

## Distribution

Current status: interim local dataset in repository.

Planned final distribution:
- HuggingFace dataset release after final validation and publication checklist completion
- license target: CC-BY-4.0 unless revised with rationale

License rationale:
- CC-BY-4.0 is chosen to maximize reuse for benchmarking while preserving attribution to the benchmark author.

## Maintenance

- versioning strategy: `tenacious_bench_v0.x`
- planned update cadence: benchmark refresh after each cohort iteration
- required checks before version bump:
  - contamination report pass
  - inter-rater agreement >= 80% per rubric dimension
  - reproducible generation with fixed seed
- ownership:
  - primary maintainer: trainee author for Week 11
  - review/sign-off: program staff before public artifact release

## Data Card Layering (Pushkarna-style)

### Telescopic view (high-level)

Tenacious-Bench v0.1 is a sales-domain benchmark for evaluating grounded, policy-safe outreach in Tenacious workflows.

### Periscopic view (component-level)

- task schema with machine-verifiable constraints
- partitioned benchmark with sealed held-out
- evaluator script with weighted dimensions
- contamination and agreement artifacts

### Microscopic view (field-level)

Each task includes:
- prospect context and segment
- signal confidence and bench availability
- candidate outreach output
- expected action constraints
- rubric details
- provenance metadata (source mode, synthetic hash)
