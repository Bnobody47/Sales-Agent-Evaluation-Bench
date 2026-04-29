# Pairwise Judge Prompt (v0.1)

You are choosing the more diagnostic benchmark task between Task A and Task B.

Prefer the task that is:
1. More clearly tied to Tenacious failure mode.
2. More mechanically gradable with provided rubric.
3. Less redundant with common template patterns.

Return strict JSON:
{
  "winner": "A" | "B",
  "reason": "<one sentence>"
}
