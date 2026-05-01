# Sales Agent Evaluation Bench - Week 11 Final

This repository contains Week 11 final-submission artifacts for the Tenacious sales-domain benchmark build, including benchmark authoring, Path B training scripts, and ablation harness code.

## Scope

- Act I: audit, schema, and machine-verifiable evaluator
- Act II: dataset authoring, partitioning, contamination checks, and documentation
- Act III: Path B preference data preparation and rationale
- Act IV: training + ablation harness scripts
- Act V: publication scaffolding

## Current status

- Benchmark generation and scoring pipeline implemented.
- Path B data-prep and training script implemented.
- Ablation harness with Delta A/B/C + cost/latency instrumentation implemented.
- Contamination checker script implemented for held-out vs train/dev.
- Final public URLs section scaffolded (replace placeholders before hand-in).

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
- Dependencies pinned in `requirements.txt`

Install command:
- `python -m pip install --upgrade pip`
- `python -m pip install -r requirements.txt`

1. Generate dataset artifacts:
   - `python generation_scripts/build_tenacious_bench.py`
2. Run contamination checks:
   - `python generation_scripts/run_contamination_checks.py`
3. Evaluate a partition quickly:
   - `python scoring_evaluator.py`
   - `python scoring_evaluator.py examples/example_tasks.jsonl`
4. Build Path B preference pairs:
   - `python training_data/build_path_b_pairs.py`
5. Train Path B ORPO (LoRA only):
   - `python training/train_path_b_orpo.py --max_steps 200`
6. Run ablations:
   - `python ablations/run_ablations.py`

## Directory map

- `audit_memo.md`: Tenacious-specific benchmark gap analysis
- `schema.json`: machine-validated task schema
- `scoring_evaluator.py`: deterministic evaluator (interim)
- `tenacious_bench_v0.1/`: benchmark partitions
- `datasheet.md`: dataset documentation
- `methodology.md`: design, routing, contamination, and path rationale
- `methodology_rationale.md`: path-choice justification with trace/paper grounding
- `generation_scripts/`: generation pipeline + judge logs
- `examples/`: committed sample tasks for evaluator inspection
- `inter_rater_agreement.md`: rubric agreement and revisions
- `synthesis_memos/`: reading synthesis memos
- `reports/bench_composition.json`: composition stats used in report
- `reports/style_guide_v2_integration.md`: how the provided style-guide v2 PDF was integrated
- `reports/evaluator_examples.md`: how evaluator applies to 3 committed example tasks
- `reports/final_submission_report.md`: final submission checklist and run summary
- `training_data/build_path_b_pairs.py`: Path B chosen/rejected pair construction
- `training/train_path_b_orpo.py`: ORPO LoRA training script
- `training/unsloth_colab_runner.md`: low-cost runbook using provided notebook
- `training/path_b_colab_run.ipynb`: Colab-ready training notebook (used for final adapter export)
- `training/artifacts/lora_adapter/`: imported trained LoRA adapter files
- `training/training_run.log`: training execution records
- `ablations/run_ablations.py`: Delta A/B/C + cost-pareto harness
- `cost_log.md`: interim cost log
- `requirements.txt`: dependency pinning
- `LICENSE.md`: CC-BY-4.0 license

## Key artifacts

- Audit memo: `audit_memo.md`
- Schema: `schema.json`
- Evaluator: `scoring_evaluator.py`
- Methodology rationale: `methodology.md`
- Datasheet: `datasheet.md`
- Synthesis memos: `synthesis_memos/common_01_synthetic_data_practices.md`, `synthesis_memos/common_02_llm_as_judge_and_contamination.md`

## Public artifact references

Replace these placeholders before final hand-in:
- HuggingFace dataset URL: `https://huggingface.co/datasets/<your-handle>/tenacious_bench_v0.1`
- HuggingFace model URL (Path A/C only): `N/A (Path B selected)`
- Blog post URL: `https://<your-blog-domain>/<post-slug>`
- Community engagement URL: `https://github.com/<org-or-user>/<repo>/issues/<id>`

## Current result snapshot

- Adapter trained and imported (`training/artifacts/lora_adapter/`).
- Latest ablation result (`ablations/ablation_results.json`):
  - Delta A observed: `+2.98` (p=`0.008`)
  - Delta B observed: `+2.98` (p=`0.008`)

## Attribution and credits

- Week 10 evidence source: `Z Conversion Engine` trace/probe artifacts.
- Style calibration source: `Tenacious Style Guide and 12 Good-Bad Examples v2.pdf`.
- Method references: DPO, ORPO/SimPO, Prometheus 2, and Li et al. (2025) preference leakage.
