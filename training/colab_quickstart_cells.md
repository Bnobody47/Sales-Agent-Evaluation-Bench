# Colab Quickstart Cells (Run Now)

Use these cells in your Colab notebook to run Path B training with low-cost defaults.

## Cell 1 - Install

```python
!pip -q install --upgrade pip
!pip -q install transformers==4.46.3 trl==0.11.4 peft==0.12.0 accelerate==0.34.2 datasets==3.2.0 bitsandbytes==0.43.3
```

## Cell 2 - Upload your pair file

```python
from google.colab import files
uploaded = files.upload()  # upload training_data/path_b_pairs.jsonl
```

## Cell 3 - Write minimal ORPO training script

```python
%%writefile train_orpo_colab.py
import random, numpy as np, torch
from datasets import load_dataset
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from trl import ORPOTrainer

SEED = 11
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)

model_id = "Qwen/Qwen2.5-0.5B-Instruct"
revision = "main"
train_file = "path_b_pairs.jsonl"

tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision, use_fast=True)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    revision=revision,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
)

lora_cfg = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    bias="none",
    task_type="CAUSAL_LM",
)
model = get_peft_model(model, lora_cfg)

ds = load_dataset("json", data_files={"train": train_file})
args = TrainingArguments(
    output_dir="orpo_out",
    learning_rate=2e-5,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=2,
    max_steps=200,            # low-cost first run
    warmup_ratio=0.03,
    lr_scheduler_type="cosine",
    logging_steps=10,
    save_steps=100,
    eval_strategy="no",
    seed=SEED,
    report_to=[],
    fp16=torch.cuda.is_available(),
)

trainer = ORPOTrainer(
    model=model,
    args=args,
    processing_class=tokenizer,
    train_dataset=ds["train"],
    max_length=1024,
    max_prompt_length=512,
)

result = trainer.train()
trainer.save_model("orpo_out/lora_adapter")
tokenizer.save_pretrained("orpo_out/lora_adapter")
print("train_loss:", result.metrics.get("train_loss"))
print("runtime_s:", result.metrics.get("train_runtime"))
```

## Cell 4 - Run training

```python
!python train_orpo_colab.py
```

## Cell 5 - Download adapter (optional)

```python
!zip -r lora_adapter.zip orpo_out/lora_adapter
from google.colab import files
files.download("lora_adapter.zip")
```
