from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel
import torch, bitsandbytes as bnb

BASE = "TinyLlama/TinyLlama-1.1B-intermediate-step-1431k-3T"
ADAPTER_DIR = "scripts/ner_lora"

bnb_cfg = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16)

tokenizer = AutoTokenizer.from_pretrained(BASE, use_fast=True)
base_model = AutoModelForCausalLM.from_pretrained(BASE,
                                                  quantization_config=bnb_cfg,
                                                  device_map="auto")

# Plug in the LoRA weights
model = PeftModel.from_pretrained(base_model, ADAPTER_DIR).merge_and_unload()
model.eval()

prompt = '[NER] Extract entities:\n"Pepsodent toothpaste price below 500"'
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

with torch.inference_mode():
    output = model.generate(**inputs, max_new_tokens=64)
print(tokenizer.decode(output[0], skip_special_tokens=True))
