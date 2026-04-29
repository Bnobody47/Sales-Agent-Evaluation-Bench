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

Environment requirements:
- Python 3.11+
- Standard library only for interim scripts (`json`, `hashlib`, `random`, `pathlib`, `re`)

Install command:
- `python -m pip install --upgrade pip`

1. Generate dataset artifacts:
   - `python generation_scripts/build_tenacious_bench.py`
2. Evaluate a partition quickly:
   - `python scoring_evaluator.py`
   - `python scoring_evaluator.py examples/example_tasks.jsonl`
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
- `examples/`: committed sample tasks for evaluator inspection
- `inter_rater_agreement.md`: rubric agreement and revisions
- `synthesis_memos/`: reading synthesis memos
- `reports/bench_composition.json`: composition stats used in report
- `reports/style_guide_v2_integration.md`: how the provided style-guide v2 PDF was integrated
- `reports/evaluator_examples.md`: how evaluator applies to 3 committed example tasks
- `cost_log.md`: interim cost log

## Key artifacts

- Audit memo: `audit_memo.md`
- Schema: `schema.json`
- Evaluator: `scoring_evaluator.py`
- Methodology rationale: `methodology.md`
- Datasheet: `datasheet.md`
- Synthesis memos: `synthesis_memos/common_01_synthetic_data_practices.md`, `synthesis_memos/common_02_llm_as_judge_and_contamination.md`

## What is next (Days 4-7)

- Convert train partition to Path B preference pairs
- Train preference-tuned judge/critic
- Run Delta A and Delta B ablations on held-out
- Prepare publication artifacts (HF dataset + blog + community post)
