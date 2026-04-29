import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple, Any


BANNED_PHRASES = [
    "world-class talent",
    "world-class",
    "top talent",
    "a-players",
    "rockstar",
    "ninja",
    "wizard",
    "skyrocket",
    "supercharge",
    "10x",
    "i hope this email finds you well",
    "just following up",
    "circling back",
    "quick question",
    "quick chat",
    "synergize",
    "synergy",
    "leverage",
    "ecosystem",
    "game-changer",
    "disruptor",
    "paradigm shift",
    "you'll regret missing this",
    "don't miss out",
    "per my last email",
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


def _validate_inputs(task: Dict[str, Any], agent_output: Dict[str, Any]) -> Tuple[str, str, str, Dict[str, Any]]:
    if not isinstance(task, dict) or not isinstance(agent_output, dict):
        raise ValueError("task and agent_output must both be dictionaries")
    if "input_fields" not in task:
        raise ValueError("task missing input_fields")
    body = str(agent_output.get("body", ""))
    subject = str(agent_output.get("subject", ""))
    cta = str(agent_output.get("cta", ""))
    input_fields = task.get("input_fields", {})
    return body, subject, cta, input_fields


def evaluate_task(task: Dict[str, Any], agent_output: Dict[str, Any]) -> ScoreBreakdown:
    """
    Numerical scoring contract:
    - Inputs: task object + agent_output object
    - Output: ScoreBreakdown with score in [0, 100]

    Calibration guide (dimension-level):
    - 1.0 ~= "5/5 quality": constraint clearly satisfied
    - 0.6-0.8 ~= "3/5 quality": borderline / partially satisfied
    - 0.0 ~= "1/5 quality": clear failure
    """
    try:
        body, subject, cta, input_fields = _validate_inputs(task, agent_output)
    except Exception:
        # Default-on-failure behavior for malformed agent output.
        return ScoreBreakdown(
            score=0.0,
            passed=False,
            dimensions={
                "groundedness": 0.0,
                "bench_commitment_safety": 0.0,
                "tone_marker_score": 0.0,
                "cta_and_structure": 0.0,
                "policy_compliance": 0.0,
            },
            flags={
                "has_signal_reference": False,
                "unsafe_commitment": True,
                "policy_violation": True,
                "malformed_output": True,
            },
        )

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
    message_type = str(task.get("metadata", {}).get("message_type", "cold")).lower()
    max_words = 120 if message_type == "cold" else (200 if message_type == "warm" else 100)
    cta_and_structure = 1.0 if _word_count(body) <= max_words and one_ask and len(subject) <= 60 else 0.0

    policy_compliance = 0.0 if _contains_any(body, BANNED_PHRASES) else 1.0
    if " bench " in f" {body.lower()} ":
        policy_compliance = 0.0

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
            result = evaluate_task(task, task.get("candidate_output", {}))
            if result.passed:
                passed += 1
    pass_rate = (passed / rows) if rows else 0.0
    return rows, pass_rate


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    if len(sys.argv) > 1:
        sample = Path(sys.argv[1])
    else:
        sample = root / "tenacious_bench_v0.1" / "dev" / "tasks.jsonl"
    n, pr = evaluate_file(sample)
    print(f"Evaluated {n} tasks from {sample.name}. pass_rate={pr:.3f}")
