# Sales Agent Evaluation Bench - Week 11 Interim

This repository contains the Week 11 interim submission artifacts (Acts I + II) for the Tenacious sales-domain benchmark build.

## Scope (Interim)

- Act I: audit, schema, and machine-verifiable evaluator
- Act II: dataset authoring, partitioning, contamination checks, and documentation

## Current status

- `audit_memo.md` complete
- `schema.json` complete with task schema and examples
- `scoring_evaluator.py` complete and runnable
- `tenacious_bench_v0.1/` generated with `train`, `dev`, `held_out`
- `datasheet.md` complete (interim version)
- `methodology.md` complete (path declaration + protocol)
- `contamination_check.json` generated
- `inter_rater_agreement.md` complete
- `generation_scripts/` complete with deterministic generation script and logs
- `synthesis_memos/` includes two common-reading memos
- `cost_log.md` includes all interim spend entries

## Dataset quick facts

- Total tasks: 210
- Partition split:
  - Train: 105 (50%)
  - Dev: 63 (30%)
  - Held-out: 42 (20%)
- Source mode mix:
  - Trace-derived: 63
  - Programmatic: 63
  - Multi-LLM synthesis: 52
  - Hand-authored adversarial: 32

## Reproducibility

1. Generate dataset artifacts:
   - `python generation_scripts/build_tenacious_bench.py`
2. Evaluate a partition quickly:
   - `python scoring_evaluator.py`
3. Validate contamination summary:
   - inspect `contamination_check.json`

## Directory map

- `audit_memo.md`: Tenacious-specific benchmark gap analysis
- `schema.json`: machine-validated task schema
- `scoring_evaluator.py`: deterministic evaluator (interim)
- `tenacious_bench_v0.1/`: benchmark partitions
- `datasheet.md`: dataset documentation
- `methodology.md`: design, routing, contamination, and path rationale
- `generation_scripts/`: generation pipeline + judge logs
- `inter_rater_agreement.md`: rubric agreement and revisions
- `synthesis_memos/`: reading synthesis memos
- `reports/bench_composition.json`: composition stats used in report
- `cost_log.md`: interim cost log

## What is next (Days 4-7)

- Convert train partition to Path B preference pairs
- Train preference-tuned judge/critic
- Run Delta A and Delta B ablations on held-out
- Prepare publication artifacts (HF dataset + blog + community post)
