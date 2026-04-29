# Synthesis Memo - LLM-as-a-Judge and Contamination

## Paper positions (what I keep)

Two points are critical and adopted:
1. Judge calibration needs sampled human/strong-model spot checks.
2. Contamination control must be an explicit protocol, not a post-hoc claim.

## Point of disagreement

Specific design choice I disagree with: reusing one judge backbone for both high-volume filtering and final adjudication (judge architecture discussion in survey sections on system design and bias controls, Sections 5-6). For this benchmark, that centralizes error and increases leakage risk when generation families overlap. A split judge protocol is safer.

## Evidence from our context

Tenacious tasks require subtle policy distinctions (e.g., phased ramp vs unsafe commitment) where judge drift can silently pass invalid outputs.

Week 10 / interim evidence:
- Probes `P-010`, `P-011`, `P-012` show tone and framing drift under pressure.
- Probes `P-007`, `P-008`, `P-009` show operational commitment failures.
- Trace anchors `tau_reproduction_check_03` and `tau_reproduction_check_04` show instability across similar task conditions.

With these failure types, a single judge can produce consistent but wrong acceptance behavior that is hard to detect without model-family rotation.

## Week 11 design decisions driven by this memo

1. Enforced family-rotation policy: generator family != judge family.
2. Logged judge routing metadata for each generation batch.
3. Added contamination checks (hash overlap proxy, n-gram threshold, embedding threshold, time-shift validation) before held-out sealing.

## Risk if ignored

Preference leakage and contamination would inflate benchmark scores and break mechanism attribution in Act IV.
