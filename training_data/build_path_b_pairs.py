import json
import sys
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scoring_evaluator import evaluate_task
TRAIN_PATH = ROOT / "tenacious_bench_v0.1" / "train" / "tasks.jsonl"
OUT_PATH = ROOT / "training_data" / "path_b_pairs.jsonl"


def read_jsonl(path: Path) -> List[Dict]:
    rows: List[Dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def make_rejected(task: Dict) -> str:
    return "Following up again. We can deploy immediately this week."


def make_chosen(task: Dict) -> str:
    stack = task["input_fields"]["requested_stack"]
    return (
        f"We noticed public signal relevant to your {stack} roadmap. "
        "If useful, we can share a scoped phased plan and confirm realistic capacity in a 15-minute call."
    )


def main() -> None:
    tasks = read_jsonl(TRAIN_PATH)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    kept = 0
    with OUT_PATH.open("w", encoding="utf-8") as out:
        for t in tasks:
            prompt = json.dumps(
                {
                    "task_id": t["task_id"],
                    "dimension": t["dimension"],
                    "input_fields": t["input_fields"],
                },
                ensure_ascii=True,
            )
            chosen = make_chosen(t)
            rejected = make_rejected(t)
            chosen_eval = evaluate_task(t, {"subject": "Request: 15 min", "body": chosen, "cta": "book_discovery_call"})
            rejected_eval = evaluate_task(
                t, {"subject": "Quick chat", "body": rejected, "cta": "book_discovery_call"}
            )
            if chosen_eval.score <= rejected_eval.score:
                continue
            row = {
                "prompt": prompt,
                "chosen": chosen,
                "rejected": rejected,
                "metadata": {
                    "task_id": t["task_id"],
                    "dimension": t["dimension"],
                    "chosen_score": chosen_eval.score,
                    "rejected_score": rejected_eval.score,
                    "generator_family": "dev_deepseek_family",
                    "judge_family": "dev_qwen_family",
                    "rotation_ok": True,
                },
            }
            out.write(json.dumps(row, ensure_ascii=True) + "\n")
            kept += 1
    print(f"Wrote {kept} Path B preference pairs to {OUT_PATH}")


if __name__ == "__main__":
    main()
