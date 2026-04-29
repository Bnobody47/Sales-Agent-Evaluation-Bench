# Synthesis Memo - LLM-as-a-Judge and Contamination

## Paper positions (what I keep)

Two points are critical and adopted:
1. Judge calibration needs sampled human/strong-model spot checks.
2. Contamination control must be an explicit protocol, not a post-hoc claim.

## Point of disagreement

I disagree with workflows that lean too heavily on a single robust judge model for both high-volume filtering and final adjudication. For this benchmark, that centralizes error and increases leakage risk when generation families overlap. A split judge protocol is safer.

## Evidence from our context

Tenacious tasks require subtle policy distinctions (e.g., phased ramp vs unsafe commitment) where judge drift can silently pass invalid outputs. A single-judge architecture could hide this until held-out evaluation.

## Week 11 design decisions driven by this memo

1. Enforced family-rotation policy: generator family != judge family.
2. Logged judge routing metadata for each generation batch.
3. Added contamination checks (hash overlap proxy, n-gram threshold, embedding threshold, time-shift validation) before held-out sealing.

## Risk if ignored

Preference leakage and contamination would inflate benchmark scores and break mechanism attribution in Act IV.
