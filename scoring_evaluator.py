import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple


BANNED_PHRASES = [
    "world-class talent",
    "rockstar",
    "ninja",
    "you are clearly behind competitors",
    "following up again",
]

SIGNAL_WORDS = [
    "funding",
    "layoff",
    "leadership",
    "hiring",
    "public signal",
    "peer",
    "bench",
    "capacity",
]


@dataclass
class ScoreBreakdown:
    score: float
    passed: bool
    dimensions: Dict[str, float]
    flags: Dict[str, bool]


def _contains_any(text: str, terms) -> bool:
    t = text.lower()
    return any(term in t for term in terms)


def _word_count(text: str) -> int:
    return len(re.findall(r"\S+", text))


def evaluate_task(task: Dict) -> ScoreBreakdown:
    body = task["candidate_output"]["body"]
    subject = task["candidate_output"]["subject"]
    cta = task["candidate_output"].get("cta", "")
    input_fields = task["input_fields"]

    grounded = 1.0 if _contains_any(body, SIGNAL_WORDS) else 0.0

    bench_available = bool(input_fields.get("bench_available", False))
    asks_handoff = _contains_any(body, ["phased", "scope", "discovery", "handoff"])
    hard_commit = _contains_any(body, ["immediately", "this week", "we can deploy"]) and not asks_handoff
    if not bench_available:
        bench_commitment_safety = 1.0 if asks_handoff else 0.0
    else:
        bench_commitment_safety = 0.0 if hard_commit and input_fields.get("signal_confidence", 0) < 0.60 else 1.0

    # Lightweight proxy for style markers; full LLM judge plugs in here later.
    direct = 1.0 if len(subject) <= 60 and "request:" in subject.lower() else 0.7
    professional = 0.0 if _contains_any(body, ["!!", "hey there", "just checking in again"]) else 1.0
    non_condescending = 0.0 if _contains_any(body, ["you are behind", "you clearly need us"]) else 1.0
    honest = 0.0 if _contains_any(body, ["guarantee", "always", "definitely"]) and not _contains_any(body, SIGNAL_WORDS) else 1.0
    tone_marker_score = (direct + professional + non_condescending + honest) / 4.0

    one_ask = cta == "book_discovery_call"
    cta_and_structure = 1.0 if _word_count(body) <= 120 and one_ask and len(subject) <= 60 else 0.0

    policy_compliance = 0.0 if _contains_any(body, BANNED_PHRASES) else 1.0

    dims = {
        "groundedness": grounded,
        "bench_commitment_safety": bench_commitment_safety,
        "tone_marker_score": tone_marker_score,
        "cta_and_structure": cta_and_structure,
        "policy_compliance": policy_compliance,
    }
    weights = {
        "groundedness": 0.30,
        "bench_commitment_safety": 0.25,
        "tone_marker_score": 0.25,
        "cta_and_structure": 0.10,
        "policy_compliance": 0.10,
    }
    score = sum(dims[name] * weights[name] for name in dims) * 100.0
    passed = score >= 78.0

    flags = {
        "has_signal_reference": grounded == 1.0,
        "unsafe_commitment": bench_commitment_safety == 0.0,
        "policy_violation": policy_compliance == 0.0,
    }
    return ScoreBreakdown(score=round(score, 2), passed=passed, dimensions=dims, flags=flags)


def evaluate_file(path: Path) -> Tuple[int, float]:
    rows = 0
    passed = 0
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            rows += 1
            task = json.loads(line)
            result = evaluate_task(task)
            if result.passed:
                passed += 1
    pass_rate = (passed / rows) if rows else 0.0
    return rows, pass_rate


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    sample = root / "tenacious_bench_v0.1" / "dev" / "tasks.jsonl"
    n, pr = evaluate_file(sample)
    print(f"Evaluated {n} tasks from {sample.name}. pass_rate={pr:.3f}")
