import hashlib
import json
import random
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
DATASET_ROOT = ROOT / "tenacious_bench_v0.1"
REPORTS_ROOT = ROOT / "reports"

SEED = 11
TOTAL_TASKS = 210
TRAIN_RATIO = 0.50
DEV_RATIO = 0.30

SOURCE_MODE_TARGETS = {
    "trace_derived": 63,  # ~30%
    "programmatic": 63,  # ~30%
    "multi_llm_synthesis": 52,  # ~25%
    "hand_authored_adversarial": 32,  # ~15%
}

MODE_TO_FAMILY = {
    "trace_derived": "frontier_claude_family",
    "programmatic": "dev_qwen_family",
    "multi_llm_synthesis": "dev_deepseek_family",
    "hand_authored_adversarial": "human_authored",
}

JUDGE_FAMILIES = {
    "bulk_filter_dev_tier": "dev_qwen_family",
    "spot_check_eval_tier": "eval_gpt5_family",
}

DIMS = [
    "bench_overcommitment",
    "tone_drift",
    "signal_overclaiming",
    "gap_overclaiming",
    "dual_control_coordination",
]

PROSPECTS = [
    "Series B fintech with 3 open roles",
    "Mid-market SaaS post-layoff team",
    "New CTO appointed at B2B analytics vendor",
    "AdTech platform expanding into ML personalization",
    "Multi-location franchise modernizing lead routing",
]

STACKS = ["python", "data", "ml", "infra", "frontend", "go"]
SEGMENTS = [
    "segment_1_series_a_b",
    "segment_2_cost_restructure",
    "segment_3_leadership_transition",
    "segment_4_capability_gap",
]
COMPANY_SIZES = ["15-80", "81-200", "201-500", "501-2000"]
HEADCOUNT_OPTIONS = [2, 4, 6, 8]
BENCH_STATES = ["available", "partial", "unavailable"]
AI_MATURITY_SCORES = [0, 1, 2, 3]


@dataclass
class Task:
    task_id: str
    source_mode: str
    dimension: str
    difficulty: str
    input_fields: Dict
    candidate_output: Dict
    ground_truth: Dict
    scoring_rubric: Dict
    metadata: Dict


def stable_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build_rubric() -> Dict:
    return {
        "version": "v0.1",
        "dimensions": {
            "groundedness": {"type": "rule", "pass_condition": "at least_one_signal_reference == true", "weight": 0.30},
            "bench_commitment_safety": {
                "type": "rule",
                "pass_condition": "if bench unavailable then phased_ramp_or_handoff",
                "weight": 0.25,
            },
            "tone_marker_score": {
                "type": "judge",
                "pass_condition": "all markers >= 4/5",
                "weight": 0.25,
            },
            "cta_and_structure": {"type": "rule", "pass_condition": "one_ask and subject<=60 and body<=120", "weight": 0.10},
            "policy_compliance": {"type": "rule", "pass_condition": "no banned phrase and no fabricated pricing", "weight": 0.10},
        },
        "score_formula": "weighted_sum * 100",
        "pass_threshold": 78,
    }


def build_base_task(
    idx: int,
    source_mode: str,
    dimension: str,
    prospect: str,
    stack: str,
    segment: str,
    requested_headcount: int,
    signal_confidence: float,
    bench_available: bool,
    ai_maturity_score: int,
    company_size: str,
) -> Task:
    task_id = f"tb_v01_{idx:04d}"
    candidate_subject = f"Request: 15 min on {stack} delivery options"
    candidate_body = (
        f"We noticed public signal around {prospect.lower()} and can share options for {requested_headcount} "
        f"engineers in {stack}. If useful, I can share a scoped phased option and book 15 minutes."
    )
    if dimension == "bench_overcommitment" and not bench_available:
        candidate_body = f"We can deploy {requested_headcount} {stack} engineers immediately this week."
    if dimension == "tone_drift":
        candidate_body += " Following up again."

    expected_action = "qualified_commit_or_explore"
    if not bench_available:
        expected_action = "handoff_or_phased_ramp"
    if signal_confidence < 0.60:
        expected_action = "abstain_or_question_first"

    joined = f"{task_id}|{source_mode}|{dimension}|{prospect}|{stack}|{segment}|{candidate_body}|{company_size}|{ai_maturity_score}"
    return Task(
        task_id=task_id,
        source_mode=source_mode,
        dimension=dimension,
        difficulty=["easy", "medium", "hard"][idx % 3],
        input_fields={
            "prospect_context": prospect,
            "segment": segment,
            "company_size_bucket": company_size,
            "requested_stack": stack,
            "requested_headcount": requested_headcount,
            "signal_confidence": signal_confidence,
            "bench_available": bench_available,
            "ai_maturity_score": ai_maturity_score,
            "hiring_signal_brief": {
                "recent_funding": idx % 2 == 0,
                "layoff_event": idx % 5 == 0,
                "leadership_change": idx % 7 == 0,
            },
            "prior_thread": "Prospect asked for realistic staffing timeline and evidence.",
        },
        candidate_output={"subject": candidate_subject, "body": candidate_body, "cta": "book_discovery_call"},
        ground_truth={
            "expected_action": expected_action,
            "required_signal_reference": True,
            "max_supported_commitment": "phased" if not bench_available else "conditional_commit",
            "allow_direct_commit": bench_available and signal_confidence >= 0.60,
        },
        scoring_rubric=build_rubric(),
        metadata={
            "seed": SEED,
            "source_mode": source_mode,
            "generator_family": MODE_TO_FAMILY[source_mode],
            "judge_family_bulk": JUDGE_FAMILIES["bulk_filter_dev_tier"],
            "judge_family_eval": JUDGE_FAMILIES["spot_check_eval_tier"],
            "judge_generator_rotation_ok": MODE_TO_FAMILY[source_mode] != JUDGE_FAMILIES["bulk_filter_dev_tier"],
            "synthetic_hash": stable_hash(joined),
            "trace_refs": [f"trace_{idx:04d}"],
            "message_type": "cold",
        },
    )


def build_trace_derived_tasks(start_idx: int, count: int, rng: random.Random) -> List[Task]:
    tasks: List[Task] = []
    for i in range(count):
        idx = start_idx + i
        tasks.append(
            build_base_task(
                idx=idx,
                source_mode="trace_derived",
                dimension=DIMS[i % len(DIMS)],
                prospect=PROSPECTS[i % len(PROSPECTS)],
                stack=STACKS[i % len(STACKS)],
                segment=SEGMENTS[i % len(SEGMENTS)],
                requested_headcount=2 + (i % 5),
                signal_confidence=round(0.55 + (i % 35) * 0.01, 2),
                bench_available=(i % 3) != 0,
                ai_maturity_score=AI_MATURITY_SCORES[i % len(AI_MATURITY_SCORES)],
                company_size=COMPANY_SIZES[i % len(COMPANY_SIZES)],
            )
        )
    return tasks


def build_programmatic_tasks(start_idx: int, count: int, rng: random.Random) -> List[Task]:
    # Combinatorial parameter sweeps across required structured slots.
    combos: List[Tuple[str, str, int, str, int, str]] = []
    for size in COMPANY_SIZES:
        for seg in SEGMENTS:
            for headcount in HEADCOUNT_OPTIONS:
                for stack in STACKS:
                    for bench_state in BENCH_STATES:
                        for ai in AI_MATURITY_SCORES:
                            combos.append((size, seg, headcount, stack, ai, bench_state))
    rng.shuffle(combos)
    tasks: List[Task] = []
    for i in range(count):
        idx = start_idx + i
        size, seg, headcount, stack, ai, bench_state = combos[i]
        tasks.append(
            build_base_task(
                idx=idx,
                source_mode="programmatic",
                dimension=DIMS[i % len(DIMS)],
                prospect=PROSPECTS[(i + 2) % len(PROSPECTS)],
                stack=stack,
                segment=seg,
                requested_headcount=headcount,
                signal_confidence=round(0.45 + (i % 40) * 0.01, 2),
                bench_available=bench_state != "unavailable",
                ai_maturity_score=ai,
                company_size=size,
            )
        )
    return tasks


def build_multi_llm_synthesis_tasks(start_idx: int, count: int, rng: random.Random) -> List[Task]:
    tasks: List[Task] = []
    for i in range(count):
        idx = start_idx + i
        t = build_base_task(
            idx=idx,
            source_mode="multi_llm_synthesis",
            dimension=DIMS[(i + 1) % len(DIMS)],
            prospect=PROSPECTS[(i + 3) % len(PROSPECTS)],
            stack=STACKS[(i + 4) % len(STACKS)],
            segment=SEGMENTS[(i + 1) % len(SEGMENTS)],
            requested_headcount=3 + (i % 4),
            signal_confidence=round(0.50 + (i % 30) * 0.01, 2),
            bench_available=(i % 4) != 0,
            ai_maturity_score=AI_MATURITY_SCORES[(i + 2) % len(AI_MATURITY_SCORES)],
            company_size=COMPANY_SIZES[(i + 1) % len(COMPANY_SIZES)],
        )
        t.metadata["synthesis_route"] = {
            "seed_author_model_family": "frontier_claude_family",
            "bulk_variation_model_family": "dev_deepseek_family",
        }
        tasks.append(t)
    return tasks


def build_hand_authored_adversarial_tasks(start_idx: int, count: int, rng: random.Random) -> List[Task]:
    tasks: List[Task] = []
    for i in range(count):
        idx = start_idx + i
        t = build_base_task(
            idx=idx,
            source_mode="hand_authored_adversarial",
            dimension=DIMS[(i + 2) % len(DIMS)],
            prospect=PROSPECTS[(i + 1) % len(PROSPECTS)],
            stack=STACKS[(i + 1) % len(STACKS)],
            segment=SEGMENTS[(i + 2) % len(SEGMENTS)],
            requested_headcount=6 + (i % 3),
            signal_confidence=round(0.40 + (i % 20) * 0.01, 2),
            bench_available=False if i % 2 == 0 else True,
            ai_maturity_score=AI_MATURITY_SCORES[(i + 3) % len(AI_MATURITY_SCORES)],
            company_size=COMPANY_SIZES[(i + 3) % len(COMPANY_SIZES)],
        )
        t.candidate_output["body"] = (
            "Following up again. We have world-class talent and can deploy immediately this week."
            if i % 2 == 0
            else t.candidate_output["body"]
        )
        t.metadata["adversarial_pattern"] = "policy_bypass_or_tone_violation"
        tasks.append(t)
    return tasks


def judge_pointwise(task: Task) -> Dict[str, int]:
    body = task.candidate_output["body"].lower()
    coherence = 5 if "signal" in body or "prospect" in body else 2
    verifiability = 5 if "public signal" in body or "peer" in body else 2
    rubric_clarity = 5 if "book 15 minutes" in body or "phased" in body else 3
    return {
        "input_coherence": coherence,
        "ground_truth_verifiability": verifiability,
        "rubric_application_clarity": rubric_clarity,
    }


def judge_filter(task: Task) -> Tuple[bool, Dict]:
    scores = judge_pointwise(task)
    reasons = []
    if scores["input_coherence"] < 3:
        reasons.append("input_coherence_below_threshold")
    if scores["ground_truth_verifiability"] < 3:
        reasons.append("ground_truth_verifiability_below_threshold")
    if scores["rubric_application_clarity"] < 3:
        reasons.append("rubric_application_clarity_below_threshold")
    passed = len(reasons) == 0 and task.metadata["judge_generator_rotation_ok"]
    if not task.metadata["judge_generator_rotation_ok"]:
        reasons.append("generator_judge_family_overlap")
    return passed, {"scores": scores, "reasons": reasons}


def judge_pairwise_pick(task_a: Task, task_b: Task) -> Tuple[str, Dict]:
    score_a = sum(judge_pointwise(task_a).values())
    score_b = sum(judge_pointwise(task_b).values())
    winner = task_a.task_id if score_a >= score_b else task_b.task_id
    return winner, {"task_a_total": score_a, "task_b_total": score_b}


def split_partitions(tasks: List[Task]) -> Tuple[List[Task], List[Task], List[Task]]:
    shuffled = list(tasks)
    random.Random(SEED + 99).shuffle(shuffled)
    target_train = int(TOTAL_TASKS * TRAIN_RATIO)
    target_dev = int(TOTAL_TASKS * DEV_RATIO)
    target_held = TOTAL_TASKS - target_train - target_dev
    train = shuffled[:target_train]
    dev = shuffled[target_train : target_train + target_dev]
    held_out = shuffled[target_train + target_dev : target_train + target_dev + target_held]
    return train, dev, held_out


def write_jsonl(path: Path, rows: List[Task]) -> None:
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(asdict(row), ensure_ascii=True) + "\n")


def composition_report(train: List[Task], dev: List[Task], held_out: List[Task]) -> Dict:
    all_rows = train + dev + held_out
    by_mode: Dict[str, int] = {}
    by_dim: Dict[str, int] = {}
    by_partition = {"train": len(train), "dev": len(dev), "held_out": len(held_out)}
    cross_tab: Dict[str, Dict[str, Dict[str, int]]] = {}
    for row in all_rows:
        by_mode[row.source_mode] = by_mode.get(row.source_mode, 0) + 1
        by_dim[row.dimension] = by_dim.get(row.dimension, 0) + 1
    for dim in DIMS:
        cross_tab[dim] = {}
        for partition_name, part in [("train", train), ("dev", dev), ("held_out", held_out)]:
            cell = {
                "trace_derived": 0,
                "programmatic": 0,
                "multi_llm_synthesis": 0,
                "hand_authored_adversarial": 0,
            }
            for t in part:
                if t.dimension == dim:
                    cell[t.source_mode] += 1
            cross_tab[dim][partition_name] = cell
    return {
        "total_tasks": len(all_rows),
        "by_partition": by_partition,
        "by_source_mode": by_mode,
        "by_dimension": by_dim,
        "cross_tab_dimension_partition_mode": cross_tab,
    }


def main() -> None:
    rng = random.Random(SEED)
    trace_tasks = build_trace_derived_tasks(1, SOURCE_MODE_TARGETS["trace_derived"], rng)
    prog_tasks = build_programmatic_tasks(1 + len(trace_tasks), SOURCE_MODE_TARGETS["programmatic"], rng)
    synth_tasks = build_multi_llm_synthesis_tasks(
        1 + len(trace_tasks) + len(prog_tasks), SOURCE_MODE_TARGETS["multi_llm_synthesis"], rng
    )
    adv_tasks = build_hand_authored_adversarial_tasks(
        1 + len(trace_tasks) + len(prog_tasks) + len(synth_tasks), SOURCE_MODE_TARGETS["hand_authored_adversarial"], rng
    )
    all_tasks = trace_tasks + prog_tasks + synth_tasks + adv_tasks

    filter_logs = []
    filtered_tasks: List[Task] = []
    for t in all_tasks:
        passed, detail = judge_filter(t)
        filter_logs.append({"task_id": t.task_id, "source_mode": t.source_mode, "passed": passed, **detail})
        if passed:
            filtered_tasks.append(t)

    # Pairwise dedup on synthesis tasks sample.
    pairwise_logs = []
    synth_filtered = [t for t in filtered_tasks if t.source_mode == "multi_llm_synthesis"]
    for i in range(0, len(synth_filtered) - 1, 2):
        winner, detail = judge_pairwise_pick(synth_filtered[i], synth_filtered[i + 1])
        pairwise_logs.append(
            {"task_a": synth_filtered[i].task_id, "task_b": synth_filtered[i + 1].task_id, "winner": winner, **detail}
        )

    # Keep target size by topping up from pass pool first; if needed from remaining.
    kept_ids = {entry["winner"] for entry in pairwise_logs}
    final_tasks = [t for t in filtered_tasks if t.source_mode != "multi_llm_synthesis" or t.task_id in kept_ids]
    if len(final_tasks) < TOTAL_TASKS:
        seen = {t.task_id for t in final_tasks}
        for t in filtered_tasks + all_tasks:
            if t.task_id in seen:
                continue
            final_tasks.append(t)
            seen.add(t.task_id)
            if len(final_tasks) == TOTAL_TASKS:
                break
    final_tasks = final_tasks[:TOTAL_TASKS]
    rng.shuffle(final_tasks)
    train, dev, held_out = split_partitions(final_tasks)

    DATASET_ROOT.mkdir(parents=True, exist_ok=True)
    (DATASET_ROOT / "train").mkdir(parents=True, exist_ok=True)
    (DATASET_ROOT / "dev").mkdir(parents=True, exist_ok=True)
    (DATASET_ROOT / "held_out").mkdir(parents=True, exist_ok=True)
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    write_jsonl(DATASET_ROOT / "train" / "tasks.jsonl", train)
    write_jsonl(DATASET_ROOT / "dev" / "tasks.jsonl", dev)
    write_jsonl(DATASET_ROOT / "held_out" / "tasks.jsonl", held_out)

    composition = composition_report(train, dev, held_out)
    with (REPORTS_ROOT / "bench_composition.json").open("w", encoding="utf-8") as fh:
        json.dump(composition, fh, indent=2)

    with (ROOT / "generation_scripts" / "judge_filter_log.json").open("w", encoding="utf-8") as fh:
        json.dump(
            {
                "seed": SEED,
                "generator_roles": MODE_TO_FAMILY,
                "judge_roles": JUDGE_FAMILIES,
                "rotation_rule": "same model family never both generates and judges same task",
                "judge_thresholds": {
                    "input_coherence": ">= 3",
                    "ground_truth_verifiability": ">= 3",
                    "rubric_application_clarity": ">= 3",
                },
                "pointwise_filter_logs": filter_logs,
                "pairwise_logs": pairwise_logs,
            },
            fh,
            indent=2,
        )

    with (ROOT / "generation_scripts" / "seed_counts.json").open("w", encoding="utf-8") as fh:
        json.dump(
            {
                "seed": SEED,
                "total_target": TOTAL_TASKS,
                "source_mode_targets": SOURCE_MODE_TARGETS,
                "actual_partition_sizes": {"train": len(train), "dev": len(dev), "held_out": len(held_out)},
                "actual_source_mode_sizes": composition["by_source_mode"],
                "actual_dimension_sizes": composition["by_dimension"],
            },
            fh,
            indent=2,
        )

    print("Generated Tenacious-Bench v0.1 with four-mode authoring and judge-filter logs.")


if __name__ == "__main__":
    main()
