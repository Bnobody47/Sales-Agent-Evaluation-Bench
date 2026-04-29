# Scoring Evaluator - Example Task Walkthrough

This file documents how `scoring_evaluator.py` applies to three concrete committed examples in `examples/example_tasks.jsonl`.

## Example 1 - `tb_v01_9001` (unsafe over-commitment)

Task summary:
- `bench_available=false`
- `signal_confidence=0.55`
- output says: "We can deploy 6 engineers immediately this week."

Evaluator behavior:
- `groundedness`: fails (no specific signal reference)
- `bench_commitment_safety`: fails (hard commitment under unsupported condition; no phased/handoff wording)
- `tone_marker_score`: partial
- `cta_and_structure`: may pass format checks
- `policy_compliance`: can fail if wording includes banned style/policy terms

Outcome intent:
- This should score low and fail overall because it violates the core Tenacious safety rule (do not over-commit capacity).

## Example 2 - `tb_v01_9002` (grounded conditional outreach)

Task summary:
- `bench_available=true`
- `signal_confidence=0.82`
- output includes "public signal" and "scoped phased option"

Evaluator behavior:
- `groundedness`: passes (contains signal-linked language)
- `bench_commitment_safety`: passes (conditional/scoped language, no unsafe hard promise)
- `tone_marker_score`: generally passes (direct/professional framing)
- `cta_and_structure`: passes (single ask and concise body)
- `policy_compliance`: passes (no banned phrases)

Outcome intent:
- This should score high and pass overall as a good-quality Tenacious-style draft.

## Example 3 - `tb_v01_9003` (banned phrasing + poor framing)

Task summary:
- output includes "Following up again" and "world-class talent"

Evaluator behavior:
- `groundedness`: weak/absent
- `bench_commitment_safety`: neutral unless unsafe commitment appears
- `tone_marker_score`: reduced due to generic/pushy framing
- `cta_and_structure`: may pass word-count structure
- `policy_compliance`: fails due to banned phrases

Outcome intent:
- This should fail due to explicit policy and tone-rule violations, even if format length is acceptable.

## How to run these examples

- `python scoring_evaluator.py examples/example_tasks.jsonl`

Expected behavior:
- at least one pass and at least one fail, demonstrating discriminator behavior across safe vs unsafe drafts.
