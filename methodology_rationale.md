# Methodology Rationale (Path B)

## Declared path

Path selected: **Path B (preference-tuned judge/critic)**.

## Why Path B fits Week 10 evidence

Week 10 evidence indicates a dominant inconsistency profile: outputs were often fluent but violated commitment safety and signal-groundedness constraints.

Trace anchors:
- `tau_dev_tier_baseline_01` (failed baseline task)
- `tau_dev_tier_baseline_02` (failed baseline task)
- `tau_reproduction_check_02` (reproduction failure under similar conditions)
- `tau_reproduction_check_03` (reproduction failure, instability under comparable prompt context)
- `tau_reproduction_check_04` (partial recovery, illustrating inconsistency rather than pure incapability)

Probe anchors:
- `P-007`, `P-008`, `P-009` (bench over-commitment)
- `P-004`, `P-005`, `P-006` (signal over-claiming)

These failures match Path B's core premise: train a critic to detect and reject high-fluency but policy-invalid outputs.

## Paper grounding (with section-level references)

1. **DPO (Rafailov et al.)**  
   - Section on preference optimization objective motivates chosen/rejected training pairs for quality-aligned ranking.
2. **ORPO / SimPO family**  
   - ORPO objective section motivates reference-free efficiency for low-cost setup.
3. **Prometheus 2 (judge specialization)**  
   - Judge-focused training framing supports using a small, specialized scorer as a production guard.
4. **Preference Leakage (Li et al., 2025)**  
   - Relatedness/leakage analysis sections justify strict generator-family vs judge-family rotation.

## Alternatives considered and dismissed

- **Path A (SFT generation adapter)** dismissed as primary path:
  - SFT improves style and local fluency, but the observed primary issue is not fluency deficit; it is consistency and self-critique failure.
- **Path C (process reward model)** dismissed for this cycle:
  - Valuable for trajectory-level optimization, but current highest-ROI error is final-output acceptance/rejection under policy constraints.

## Data preparation implications (Path B)

- Build preference pairs from train split:
  - `rejected`: outputs that violate grounding/bench/tone policy
  - `chosen`: corrected outputs passing evaluator and style-guide rules
- Enforce family separation:
  - rewrite model family != judge model family for each pair
- Keep held-out sealed:
  - contamination checks run before final pair freeze
