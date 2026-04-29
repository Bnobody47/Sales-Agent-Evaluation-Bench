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

## Distribution

Current status: interim local dataset in repository.

Planned final distribution:
- HuggingFace dataset release after final validation and publication checklist completion
- license target: CC-BY-4.0 unless revised with rationale

## Maintenance

- versioning strategy: `tenacious_bench_v0.x`
- planned update cadence: benchmark refresh after each cohort iteration
- required checks before version bump:
  - contamination report pass
  - inter-rater agreement >= 80% per rubric dimension
  - reproducible generation with fixed seed

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
