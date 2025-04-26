#!/usr/bin/env python
# fine_tune_ecom_distilbert.py
# Fine‑tunes DistilBERT for token‑level NER on a custom “brand / product /
# size / color / material” label set.

import numpy as np
from datasets import load_dataset
from evaluate import load as load_metric     # NEW import
from transformers import (
    AutoTokenizer,
    AutoModelForTokenClassification,
    DataCollatorForTokenClassification,
    TrainingArguments,
    Trainer,
)

# ---------------------------------------------------------------------
# 1.  Configuration
# ---------------------------------------------------------------------
DATA_FILE = "ecom_ner_dummy.jsonl"
MODEL_NAME = "distilbert/distilbert-base-uncased"
LABEL_LIST = [
    "O",
    "B-BRAND", "I-BRAND",
    "B-PRODUCT", "I-PRODUCT",
    "B-SIZE", "I-SIZE",
    "B-COLOR", "I-COLOR",
    "B-MATERIAL", "I-MATERIAL",
]
LABEL_TO_ID = {lab: i for i, lab in enumerate(LABEL_LIST)}
NUM_LABELS = len(LABEL_LIST)

# ---------------------------------------------------------------------
# 2.  Load & split
# ---------------------------------------------------------------------
dataset = load_dataset("json", data_files=DATA_FILE, split="train")
dataset = dataset.train_test_split(test_size=0.1, seed=2025)
train_ds, val_ds = dataset["train"], dataset["test"]

# ---------------------------------------------------------------------
# 3.  Tokeniser & label alignment
# ---------------------------------------------------------------------
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def tokenize_and_align_labels(examples, label_all_tokens=True):
    tokenized = tokenizer(
        examples["tokens"],
        is_split_into_words=True,
        truncation=True,
    )

    all_labels = []
    for i, word_ids in enumerate(tokenized.word_ids(batch_index=None)):
        labels = []
        example_labels = examples["ner_tags"][i]
        prev_word_id = None
        for word_id in tokenized.word_ids(batch_index=i):
            if word_id is None:
                labels.append(-100)
            elif word_id != prev_word_id:
                labels.append(example_labels[word_id])
            else:
                labels.append(example_labels[word_id] if label_all_tokens else -100)
            prev_word_id = word_id
        all_labels.append(labels)

    tokenized["labels"] = all_labels
    return tokenized

train_ds = train_ds.map(tokenize_and_align_labels, batched=True, remove_columns=train_ds.column_names)
val_ds   = val_ds.map(tokenize_and_align_labels,   batched=True, remove_columns=val_ds.column_names)

# ---------------------------------------------------------------------
# 4.  Model, collator, metric
# ---------------------------------------------------------------------
model = AutoModelForTokenClassification.from_pretrained(
    MODEL_NAME,
    num_labels=NUM_LABELS,
    id2label={i: l for i, l in enumerate(LABEL_LIST)},
    label2id=LABEL_TO_ID,
)

data_collator = DataCollatorForTokenClassification(tokenizer)
metric = evaluate.load("seqeval")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=2)

    true_labels, true_preds = [], []
    for lab_seq, pred_seq in zip(labels, preds):
        lab_list, pred_list = [], []
        for l, p in zip(lab_seq, pred_seq):
            if l == -100:
                continue
            lab_list.append(LABEL_LIST[l])
            pred_list.append(LABEL_LIST[p])
        true_labels.append(lab_list)
        true_preds.append(pred_list)

    results = metric.compute(predictions=true_preds, references=true_labels)
    return {
        "precision": results["overall_precision"],
        "recall":    results["overall_recall"],
        "f1":        results["overall_f1"],
        "accuracy":  results["overall_accuracy"],
    }

# ---------------------------------------------------------------------
# 5.  TrainingArguments & Trainer
# ---------------------------------------------------------------------
args = TrainingArguments(
    output_dir="ecom_distilbert_ner_ckpt",
    evaluation_strategy="epoch",
    learning_rate=3e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=5,
    weight_decay=0.01,
    logging_steps=50,
    save_total_limit=2,
    load_best_model_at_end=True,
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_ds,
    eval_dataset=val_ds,
    data_collator=data_collator,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

# ---------------------------------------------------------------------
# 6.  Train, evaluate, save
# ---------------------------------------------------------------------
trainer.train()
metrics = trainer.evaluate()
print("Validation metrics:", metrics)

trainer.save_model("ecom_distilbert_ner_final")
tokenizer.save_pretrained("ecom_distilbert_ner_final")
