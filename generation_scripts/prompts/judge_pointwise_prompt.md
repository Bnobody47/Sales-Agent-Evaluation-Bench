# Pointwise Judge Prompt (v0.1)

You are grading a sales-agent task for Tenacious-Bench.

Score each dimension from 1 to 5:
- input_coherence
- ground_truth_verifiability
- rubric_application_clarity

Definitions:
- 1 = clearly invalid
- 3 = acceptable but weak
- 5 = strong and unambiguous

Return strict JSON:
{
  "input_coherence": <int 1-5>,
  "ground_truth_verifiability": <int 1-5>,
  "rubric_application_clarity": <int 1-5>,
  "notes": "<short rationale>"
}

Reject task if any score < 3.
