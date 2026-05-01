# Unsloth Colab Runner (Path B, low cost)

Source notebook provided:
- `c:\Users\Bnobody_47\Downloads\TRP1_week11_unsloth.ipynb`

## Recommended low-cost setup

- Runtime: Google Colab T4 (free) first
- Backbone: `Qwen/Qwen2.5-0.5B-Instruct`
- Method: ORPO (Path B), LoRA-only
- Max steps: 200-300 for first run
- Eval-tier model usage: only held-out calibration passes

## Practical run order

1. Upload `training_data/path_b_pairs.jsonl` to Colab.
2. Install Unsloth dependencies from notebook.
3. Set seed to 11 and keep batch sizes small.
4. Run one short training pass.
5. Push adapter only (not merged model).

## Budget control rules

- Do not use eval-tier model during data iteration.
- Limit held-out eval-tier scoring to 3-4 passes max.
- Kill training at ~30 minutes if no validation lift.

## Expected cost envelope

- Training on free Colab T4: $0
- Optional RunPod fallback: cap at $2-4
