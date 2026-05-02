# Final Submission Report (Week 11)

## Delivered artifacts

- Audit memo: `audit_memo.md`
- Schema + evaluator: `schema.json`, `scoring_evaluator.py`
- Dataset: `tenacious_bench_v0.1/{train,dev,held_out}/tasks.jsonl`
- Datasheet: `datasheet.md`
- Methodology: `methodology.md`, `methodology_rationale.md`
- Generation + judge pipeline: `generation_scripts/build_tenacious_bench.py`
- Contamination checks: `generation_scripts/run_contamination_checks.py`, `contamination_check.json`
- Inter-rater analysis: `inter_rater_agreement.md`
- Training data prep: `training_data/build_path_b_pairs.py`, `training_data/path_b_pairs.jsonl`
- Training script: `training/train_path_b_orpo.py`
- Trained adapter (from Colab): `training/artifacts/lora_adapter/`
- Training log: `training/training_run.log`
- Ablation harness: `ablations/run_ablations.py`, `ablations/ablation_results.json`
- Cost log: `cost_log.md`

## Path choice

Path selected: **B** (preference-tuned judge/critic), chosen for inconsistency-detection failures observed in Week 10 traces and probes.

## Current benchmark composition

Source: `generation_scripts/seed_counts.json`

- Total tasks: 210
- Partition: 105 / 63 / 42 (train/dev/held_out)
- Source-mode: 63 / 63 / 52 / 32 (trace/programmatic/multi-LLM/adversarial)
- Dimensions: all five target dimensions present

## Cost-first training recommendation

- Use provided notebook guidance: `training/unsloth_colab_runner.md`
- Start with low-cost backbone (`Qwen/Qwen2.5-0.5B-Instruct`) + LoRA-only ORPO
- Keep eval-tier model calls only for held-out calibration passes
- Use 30-minute kill criterion if no validation lift

## Training completion status

- Colab GPU run completed and exported LoRA adapter package.
- Adapter imported into repo at `training/artifacts/lora_adapter/`.
- Verified adapter config:
  - base model: `Qwen/Qwen2.5-0.5B-Instruct`
  - LoRA rank: `r=16`
  - alpha: `32`
  - dropout: `0.05`
  - target modules: `q_proj`, `k_proj`, `v_proj`, `o_proj`
- Adapter weight file:
  - `adapter_model.safetensors` (~8.68 MB)

## Ablation summary snapshot

Source: `ablations/ablation_results.json`

- Delta A (trained vs baseline):
  - observed delta: `+2.98`
  - 95% CI: `[+0.60, +5.36]`
  - p-value: `0.008`
- Delta B (trained vs prompt-only):
  - observed delta: `+2.98`
  - 95% CI: `[+0.60, +5.36]`
  - p-value: `0.008`
- Delta C (informational vs stored tau2 reference):
  - observed delta: `+4.86`
  - 95% CI: `[+2.48, +7.24]`
  - p-value: `0.000`
- Cost-Pareto (mean cost/task estimate):
  - trained: `5.23e-05`
  - baseline: `5.23e-05`
  - prompt-only: `6.07e-05`

## Repro steps

1. `python generation_scripts/build_tenacious_bench.py`
2. `python generation_scripts/run_contamination_checks.py`
3. `python training_data/build_path_b_pairs.py`
4. `python training/train_path_b_orpo.py --max_steps 200`
5. `python ablations/run_ablations.py`

## Publication links

- HF dataset URL: https://huggingface.co/datasets/Bnobody/tenacious_bench_v0.1
- Blog URL: https://dev.to/bnobody47/tenacious-bench-v01-a-small-b2b-sales-outreach-benchmark-with-contamination-checks-4foj
- Community URL (GitHub issue): https://github.com/Bnobody47/Sales-Agent-Evaluation-Bench/issues/1
- Community URL (HF dataset discussion): https://huggingface.co/datasets/Bnobody/tenacious_bench_v0.1/discussions/2
