"""
Path B ORPO training script (LoRA-only).

Cost-optimized defaults:
- Backbone: Qwen/Qwen2.5-0.5B-Instruct
- LoRA adapters only (no full fine-tune)
- Small max steps for 30-90 minute envelope on T4/4090
"""

import argparse
import json
import random
from pathlib import Path

import numpy as np
import torch
from datasets import load_dataset
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from trl import ORPOTrainer


ROOT = Path(__file__).resolve().parents[1]


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--train_file", default=str(ROOT / "training_data" / "path_b_pairs.jsonl"))
    parser.add_argument("--output_dir", default=str(ROOT / "training" / "artifacts"))
    parser.add_argument("--backbone", default="Qwen/Qwen2.5-0.5B-Instruct")
    parser.add_argument("--backbone_revision", default="main")
    parser.add_argument("--seed", type=int, default=11)
    parser.add_argument("--learning_rate", type=float, default=2e-5)
    parser.add_argument("--per_device_train_batch_size", type=int, default=4)
    parser.add_argument("--gradient_accumulation_steps", type=int, default=2)
    parser.add_argument("--num_train_epochs", type=float, default=1.0)
    parser.add_argument("--max_steps", type=int, default=300)
    parser.add_argument("--warmup_ratio", type=float, default=0.03)
    parser.add_argument("--lr_scheduler_type", default="cosine")
    parser.add_argument("--lora_r", type=int, default=16)
    parser.add_argument("--lora_alpha", type=int, default=32)
    parser.add_argument("--lora_dropout", type=float, default=0.05)
    parser.add_argument("--max_length", type=int, default=1024)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    set_seed(args.seed)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    log_path = ROOT / "training" / "training_run.log"

    tokenizer = AutoTokenizer.from_pretrained(args.backbone, revision=args.backbone_revision, use_fast=True)
    tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        args.backbone,
        revision=args.backbone_revision,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    )
    lora_cfg = LoraConfig(
        r=args.lora_r,
        lora_alpha=args.lora_alpha,
        lora_dropout=args.lora_dropout,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora_cfg)

    ds = load_dataset("json", data_files={"train": args.train_file})
    training_args = TrainingArguments(
        output_dir=str(output_dir),
        learning_rate=args.learning_rate,
        per_device_train_batch_size=args.per_device_train_batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        num_train_epochs=args.num_train_epochs,
        max_steps=args.max_steps,
        warmup_ratio=args.warmup_ratio,
        lr_scheduler_type=args.lr_scheduler_type,
        logging_steps=10,
        save_steps=100,
        evaluation_strategy="no",
        seed=args.seed,
        report_to=[],
        fp16=torch.cuda.is_available(),
    )

    trainer = ORPOTrainer(
        model=model,
        args=training_args,
        processing_class=tokenizer,
        train_dataset=ds["train"],
        max_length=args.max_length,
        max_prompt_length=min(512, args.max_length // 2),
    )
    train_result = trainer.train()
    trainer.save_model(str(output_dir / "lora_adapter"))
    tokenizer.save_pretrained(str(output_dir / "lora_adapter"))

    run_meta = {
        "path": "B",
        "algorithm": "ORPO",
        "seed": args.seed,
        "backbone": args.backbone,
        "backbone_revision": args.backbone_revision,
        "lora_only": True,
        "hyperparameters": {
            "learning_rate": args.learning_rate,
            "per_device_train_batch_size": args.per_device_train_batch_size,
            "gradient_accumulation_steps": args.gradient_accumulation_steps,
            "num_train_epochs": args.num_train_epochs,
            "max_steps": args.max_steps,
            "warmup_ratio": args.warmup_ratio,
            "lr_scheduler_type": args.lr_scheduler_type,
            "lora_r": args.lora_r,
            "lora_alpha": args.lora_alpha,
            "lora_dropout": args.lora_dropout,
            "max_length": args.max_length,
        },
        "train_runtime_seconds": train_result.metrics.get("train_runtime"),
        "train_loss": train_result.metrics.get("train_loss"),
    }
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(run_meta) + "\n")
    print("Training complete. Adapter saved.")


if __name__ == "__main__":
    main()
