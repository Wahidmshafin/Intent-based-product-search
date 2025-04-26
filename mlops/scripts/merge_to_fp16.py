#!/usr/bin/env python3
"""
Merge LoRA adapter into full FP16 model.
Usage:
  python merge_to_fp16.py --adapter artifacts/ner_lora_1b \
                          --out_dir artifacts/ner_merged_fp16
"""
import argparse, torch, shutil
from unsloth import FastLanguageModel
from peft import PeftModel

parser = argparse.ArgumentParser()
parser.add_argument("--adapter", required=True)
parser.add_argument("--out_dir", required=True)
args = parser.parse_args()

BASE = "unsloth/Llama-3.2-1B-Instruct"
base, tok = FastLanguageModel.from_pretrained(
    BASE, dtype=torch.float16, load_in_4bit=False, max_seq_length=128
)

merged = PeftModel.from_pretrained(base, args.adapter).merge_and_unload()
merged.save_pretrained(args.out_dir, safe_serialization=True)
tok.save_pretrained(args.out_dir)
print("Merged FP16 model saved to", args.out_dir)
