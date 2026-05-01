# Interim Cost Log (Acts I + II)

| Timestamp (UTC) | Bucket | Cost (USD) | Purpose |
|---|---:|---:|---|
| 2026-04-28T16:00:00Z | Dataset authoring | 0.80 | Dev-tier generation prompt routing dry run |
| 2026-04-28T16:18:00Z | Dataset authoring | 0.65 | Judge-filter prompt calibration |
| 2026-04-28T16:42:00Z | Dataset authoring | 0.74 | Variance sweep for template expansion |
| 2026-04-28T17:05:00Z | Dataset authoring | 0.58 | Spot-check prompts for tone-marker adjudication |
| 2026-04-28T17:30:00Z | Dataset authoring | 0.61 | Dedup and quality-filter verification |
| 2026-05-01T19:00:00Z | Training | 0.00 | Colab T4 Path B LoRA run (adapter exported) |
| 2026-05-01T19:20:00Z | Held-out evaluation | 0.00 | Local ablation harness execution on held-out |

## Totals (interim to date)

- Dataset authoring subtotal: **$3.38**
- Training: **$0.00** (Colab free tier)
- Held-out evaluation: **$0.00** (local harness run)
- Reserve consumed: **$0.00**
- Grand total: **$3.38**

## Notes

- No eval-tier model spend during Acts I + II.
- No tau2-bench retail rerun costs booked in Week 11.
