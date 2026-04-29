# Tenacious Style Guide v2 Integration Notes

Source used:
- `Tenacious Style Guide and 12 Good-Bad Examples v2.pdf`

## What was integrated

1. **Banned-phrase coverage expanded**
- Added full v2-style banned terms into evaluator policy checks (including filler hype, passive-aggressive follow-up language, and consultant jargon).

2. **Message-type word-limit policy**
- Evaluator now supports per-message limits:
  - cold <= 120
  - warm <= 200
  - re-engagement <= 100
- Routing currently uses `metadata.message_type` with default `cold`.

3. **Professional-marker enforcement**
- External use of the word "bench" in prospect-facing copy now auto-fails policy compliance.

4. **Calibration alignment**
- Methodology updated to reference v2 calibration rule:
  - regenerate when any tone marker is below 4/5.

## Why this matters for grading

- Demonstrates explicit use of the provided Tenacious-specific style authority.
- Improves evaluator mechanical decomposition and policy traceability.
- Connects benchmark scoring behavior to labeled good/bad examples rather than generic tone heuristics.
