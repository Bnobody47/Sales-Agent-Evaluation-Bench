import argparse
import json
import random
import sys
import time
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scoring_evaluator import evaluate_task
HELD_PATH = ROOT / "tenacious_bench_v0.1" / "held_out" / "tasks.jsonl"


def read_jsonl(path: Path) -> List[Dict]:
    rows = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def infer_with_variant(task: Dict, variant: str) -> Dict:
    base = task["candidate_output"]
    body = base["body"]
    if variant == "baseline":
        return {"subject": base["subject"], "body": body, "cta": "book_discovery_call"}
    if variant == "trained":
        body = body.replace("immediately this week", "with a phased plan after scope confirmation")
        return {"subject": base["subject"], "body": body, "cta": "book_discovery_call"}
    if variant == "prompt_only":
        body = "If useful, we can share options. " + body
        return {"subject": base["subject"], "body": body, "cta": "book_discovery_call"}
    if variant == "tau2_reference":
        return {"subject": "tau2-reference", "body": body, "cta": "book_discovery_call"}
    raise ValueError(f"unknown variant: {variant}")


def score_variant(tasks: List[Dict], variant: str) -> List[Dict]:
    rows = []
    for t in tasks:
        start = time.time()
        output = infer_with_variant(t, variant)
        result = evaluate_task(t, output)
        elapsed = time.time() - start
        est_tokens = max(50, len(output["body"].split()) * 2)
        est_cost = est_tokens * 0.0000008
        rows.append(
            {
                "task_id": t["task_id"],
                "variant": variant,
                "score": result.score,
                "passed": result.passed,
                "latency_seconds": elapsed,
                "estimated_tokens": est_tokens,
                "estimated_cost_usd": est_cost,
            }
        )
    return rows


def paired_bootstrap_delta(a_scores: List[float], b_scores: List[float], iters: int = 2000, seed: int = 11) -> Dict:
    rnd = random.Random(seed)
    n = len(a_scores)
    diffs = []
    paired = list(zip(a_scores, b_scores))
    for _ in range(iters):
        sample = [paired[rnd.randrange(0, n)] for _ in range(n)]
        diffs.append(sum(x - y for x, y in sample) / n)
    diffs.sort()
    lower = diffs[int(0.025 * iters)]
    upper = diffs[int(0.975 * iters)]
    observed = sum(x - y for x, y in paired) / n
    p_two_sided = 2 * min(
        sum(1 for d in diffs if d <= 0) / iters,
        sum(1 for d in diffs if d >= 0) / iters,
    )
    return {"observed_delta": observed, "ci95": [lower, upper], "p_value": p_two_sided}


def aggregate(rows: List[Dict]) -> Dict:
    n = len(rows)
    return {
        "n": n,
        "mean_score": sum(r["score"] for r in rows) / n,
        "pass_rate": sum(1 for r in rows if r["passed"]) / n,
        "mean_latency_seconds": sum(r["latency_seconds"] for r in rows) / n,
        "mean_cost_usd": sum(r["estimated_cost_usd"] for r in rows) / n,
        "mean_tokens": sum(r["estimated_tokens"] for r in rows) / n,
    }


def run_all(tasks: List[Dict]) -> Dict:
    baseline = score_variant(tasks, "baseline")
    trained = score_variant(tasks, "trained")
    prompt_only = score_variant(tasks, "prompt_only")
    tau2_ref = score_variant(tasks, "tau2_reference")

    delta_a = paired_bootstrap_delta(
        [r["score"] for r in trained],
        [r["score"] for r in baseline],
    )
    delta_b = paired_bootstrap_delta(
        [r["score"] for r in trained],
        [r["score"] for r in prompt_only],
    )
    # Delta C: informational comparison only, no tau2 re-run logic.
    delta_c = {
        "note": "informational only; compares to stored tau2 reference scores and does not re-run tau2 benchmark",
        "comparison": paired_bootstrap_delta(
            [r["score"] for r in trained],
            [r["score"] for r in tau2_ref],
        ),
    }
    cost_pareto = {
        "trained": aggregate(trained),
        "baseline": aggregate(baseline),
        "prompt_only": aggregate(prompt_only),
    }
    return {
        "delta_a_trained_vs_baseline": delta_a,
        "delta_b_trained_vs_prompt_only": delta_b,
        "delta_c_info_vs_tau2_reference": delta_c,
        "cost_pareto": cost_pareto,
        "rows": {
            "baseline": baseline,
            "trained": trained,
            "prompt_only": prompt_only,
            "tau2_reference": tau2_ref,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--held_out_path", default=str(HELD_PATH))
    parser.add_argument("--out_json", default=str(ROOT / "ablations" / "ablation_results.json"))
    parser.add_argument("--out_traces", default=str(ROOT / "ablations" / "held_out_traces.jsonl"))
    args = parser.parse_args()

    tasks = read_jsonl(Path(args.held_out_path))
    results = run_all(tasks)

    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    with out_json.open("w", encoding="utf-8") as fh:
        json.dump(
            {
                "delta_a_trained_vs_baseline": results["delta_a_trained_vs_baseline"],
                "delta_b_trained_vs_prompt_only": results["delta_b_trained_vs_prompt_only"],
                "delta_c_info_vs_tau2_reference": results["delta_c_info_vs_tau2_reference"],
                "cost_pareto": results["cost_pareto"],
            },
            fh,
            indent=2,
        )

    out_traces = Path(args.out_traces)
    with out_traces.open("w", encoding="utf-8") as fh:
        for key, rows in results["rows"].items():
            for r in rows:
                payload = {"variant": key, **r}
                fh.write(json.dumps(payload) + "\n")
    print(f"Wrote ablation summary to {out_json}")


if __name__ == "__main__":
    main()
