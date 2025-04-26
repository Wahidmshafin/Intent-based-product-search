import argparse, os, json, random, torch
from pathlib import Path
from datasets import load_dataset
from unsloth import FastLanguageModel, is_bfloat16_supported
from unsloth.chat_templates import get_chat_template, train_on_responses_only
from transformers import DataCollatorForSeq2Seq, TrainingArguments
from trl import SFTTrainer

# ────────────────  CLI arguments ────────────────────────────────────────────
parser = argparse.ArgumentParser()
parser.add_argument("--dataset",   required=True, help="Path to JSONL with fields text + target")
parser.add_argument("--out_dir",   required=True, help="Directory to save LoRA adapter")
parser.add_argument("--max_steps", type=int, default=300, help="Training steps (300 ≈ 1-2 epochs on 7k rows)")
args = parser.parse_args()

Path(args.out_dir).mkdir(parents=True, exist_ok=True)

# ────────────────  Constants (match notebook) ───────────────────────────────
BASE_MODEL      = "unsloth/Llama-3.2-1B-Instruct"
MAX_SEQ_LENGTH  = 128
BATCH_PER_DEV   = 2         # fits 4 GB
GRAD_ACC_STEPS  = 8         # eff. batch 16
LR              = 3e-4
SEED            = 3407

# ────────────────  1. Load model (4-bit) ────────────────────────────────────
print("Loading base model…")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name      = BASE_MODEL,
    max_seq_length  = MAX_SEQ_LENGTH,
    load_in_4bit    = True,
    dtype           = None,            # auto fp16
)

# attach LoRA
model = FastLanguageModel.get_peft_model(
    model,
    r                = 8,
    lora_alpha       = 8,
    lora_dropout     = 0.05,
    target_modules   = ["q_proj","k_proj","v_proj","o_proj",
                        "gate_proj","up_proj","down_proj"],
    bias             = "none",
    use_gradient_checkpointing = "unsloth",   # memory saver on 4 GB
)
print("Trainable params:", sum(p.numel() for p in model.parameters() if p.requires_grad))

# ────────────────  2. Load dataset ──────────────────────────────────────────
print("Loading dataset:", args.dataset)
raw_ds = load_dataset("json", data_files=args.dataset, split="train")

def to_convo(row):
    return {"conversations": [
        {"role": "user",      "content": row["text"]},
        {"role": "assistant", "content": row["target"]},
    ]}
raw_ds = raw_ds.map(to_convo)

# Apply Llama chat template
tokenizer = get_chat_template(tokenizer, chat_template="llama-3.1")

def fmt(batch):
    return {"text": [
        tokenizer.apply_chat_template(c, tokenize=False, add_generation_prompt=False)
        for c in batch["conversations"]
    ]}
ds = raw_ds.map(fmt, batched=True, remove_columns=raw_ds.column_names)

train_ds, eval_ds = ds.train_test_split(test_size=0.1, seed=SEED).values()

# ────────────────  3. Trainer setup ─────────────────────────────────────────
data_collator = DataCollatorForSeq2Seq(tokenizer)

training_args = TrainingArguments(
    per_device_train_batch_size = BATCH_PER_DEV,
    gradient_accumulation_steps = GRAD_ACC_STEPS,
    max_steps                   = args.max_steps,
    warmup_steps                = 10,
    learning_rate               = LR,
    fp16                        = True,
    bf16                        = is_bfloat16_supported(),
    optim                       = "adamw_8bit",
    lr_scheduler_type           = "cosine",
    weight_decay                = 0.01,
    logging_steps               = 50,
    save_total_limit            = 2,
    output_dir                  = args.out_dir,
    report_to                   = "none",
    seed                        = SEED,
)

trainer = SFTTrainer(
    model               = model,
    tokenizer           = tokenizer,
    train_dataset       = train_ds,
    eval_dataset        = eval_ds,
    dataset_text_field  = "text",
    max_seq_length      = MAX_SEQ_LENGTH,
    data_collator       = data_collator,
    packing             = True,          # pack multiple short samples together
    args                = training_args,
)

# Train on assistant messages only
trainer = train_on_responses_only(
    trainer,
    instruction_part="<|start_header_id|>user<|end_header_id|>\n\n",
    response_part   ="<|start_header_id|>assistant<|end_header_id|>\n\n",
)

# ────────────────  4. Train & save ──────────────────────────────────────────
print("Starting training…")
trainer.train()
trainer.model.save_pretrained(args.out_dir, safe_serialization=True)
tokenizer.save_pretrained(args.out_dir)
print("LoRA adapter saved at", args.out_dir)