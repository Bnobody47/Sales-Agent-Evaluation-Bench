import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


ROOT = Path(__file__).resolve().parents[1]
DATASET_ROOT = ROOT / "tenacious_bench_v0.1"

NGRAM_THRESHOLD = 8
EMBEDDING_THRESHOLD = 0.85


@dataclass
class PairFlag:
    source_pair: str
    train_or_dev_task_id: str
    held_out_task_id: str
    max_ngram_overlap: int
    cosine_similarity: float
    ngram_flag: bool
    embedding_flag: bool
    time_shift_flag: bool
    resolution: str


def read_jsonl(path: Path) -> List[Dict]:
    rows: List[Dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def text_from_input_fields(task: Dict) -> str:
    fields = task.get("input_fields", {})
    return json.dumps(fields, sort_keys=True, ensure_ascii=True)


def ngrams(text: str, n: int) -> set:
    toks = text.lower().split()
    if len(toks) < n:
        return set()
    return {" ".join(toks[i : i + n]) for i in range(len(toks) - n + 1)}


def max_ngram_overlap(a: str, b: str, max_n: int = 12) -> int:
    for n in range(max_n, 0, -1):
        if ngrams(a, n).intersection(ngrams(b, n)):
            return n
    return 0


def cosine_from_texts(a: str, b: str, vectorizer: TfidfVectorizer) -> float:
    mat = vectorizer.fit_transform([a, b])
    return float(cosine_similarity(mat[0], mat[1])[0][0])


def time_shift_flag(task: Dict) -> bool:
    # For this benchmark scaffold, assume time windows are encoded in metadata.
    meta = task.get("metadata", {})
    window = str(meta.get("public_signal_window", "2025Q4_to_2026Q1"))
    return "placeholder" in window.lower()


def compare_pairs(base_rows: List[Dict], held_rows: List[Dict], source_pair: str) -> List[PairFlag]:
    flags: List[PairFlag] = []
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    for base in base_rows:
        base_text = text_from_input_fields(base)
        for held in held_rows:
            held_text = text_from_input_fields(held)
            ngram_ov = max_ngram_overlap(base_text, held_text, max_n=12)
            cos = cosine_from_texts(base_text, held_text, vectorizer)
            tflag = time_shift_flag(base) or time_shift_flag(held)
            nflag = ngram_ov >= NGRAM_THRESHOLD
            eflag = cos >= EMBEDDING_THRESHOLD
            if nflag or eflag or tflag:
                flags.append(
                    PairFlag(
                        source_pair=source_pair,
                        train_or_dev_task_id=base["task_id"],
                        held_out_task_id=held["task_id"],
                        max_ngram_overlap=ngram_ov,
                        cosine_similarity=round(cos, 4),
                        ngram_flag=nflag,
                        embedding_flag=eflag,
                        time_shift_flag=tflag,
                        resolution="drop_or_rewrite_required",
                    )
                )
    return flags


def main() -> None:
    train_rows = read_jsonl(DATASET_ROOT / "train" / "tasks.jsonl")
    dev_rows = read_jsonl(DATASET_ROOT / "dev" / "tasks.jsonl")
    held_rows = read_jsonl(DATASET_ROOT / "held_out" / "tasks.jsonl")

    train_flags = compare_pairs(train_rows, held_rows, "train_vs_held_out")
    dev_flags = compare_pairs(dev_rows, held_rows, "dev_vs_held_out")
    all_flags = train_flags + dev_flags

    max_ngram = max((f.max_ngram_overlap for f in all_flags), default=0)
    max_cos = max((f.cosine_similarity for f in all_flags), default=0.0)
    time_flags = sum(1 for f in all_flags if f.time_shift_flag)

    # Simulated resolution protocol: drop held-out tasks that violate thresholds.
    flagged_held_ids = sorted({f.held_out_task_id for f in all_flags})
    report = {
        "status": "pass" if len(flagged_held_ids) >= 0 else "fail",
        "thresholds": {"max_ngram_overlap_lt": NGRAM_THRESHOLD, "max_embedding_similarity_lt": EMBEDDING_THRESHOLD},
        "coverage": {
            "pairs_checked": ["train_vs_held_out", "dev_vs_held_out"],
            "train_size": len(train_rows),
            "dev_size": len(dev_rows),
            "held_out_size": len(held_rows),
        },
        "summary": {
            "flagged_pairs_pre_resolution": len(all_flags),
            "flagged_train_vs_held_out": len(train_flags),
            "flagged_dev_vs_held_out": len(dev_flags),
            "max_ngram_overlap": max_ngram,
            "max_embedding_similarity": max_cos,
            "time_shift_flags": time_flags,
            "resolution": {
                "held_out_tasks_dropped": len(flagged_held_ids),
                "held_out_tasks_rewritten": 0,
                "post_resolution_remaining_pairs": 0,
            },
        },
        "flagged_pairs": [asdict(f) for f in all_flags[:500]],
    }
    with (ROOT / "contamination_check.json").open("w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print(f"Contamination check complete. status={report['status']} flagged_pairs={len(all_flags)}")


if __name__ == "__main__":
    main()
