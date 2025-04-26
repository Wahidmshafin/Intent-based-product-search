from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

CKPT = "scripts/ecom_distilbert_ner_final"      # or an absolute path

# 1️⃣  Load tokenizer + model
tokenizer = AutoTokenizer.from_pretrained(CKPT)
model     = AutoModelForTokenClassification.from_pretrained(CKPT)

# 2️⃣  Quick inference pipeline (aggregates sub‑tokens into full entities)
ner = pipeline(
    task="token-classification",
    model=model,
    tokenizer=tokenizer,
    aggregation_strategy="simple",      # merges B‑/I‑ tags into one span
)

text = "Pepsodent toothpaste price less than 500"

raw = ner(text, aggregation_strategy=None)   # token‑level
merged = []
for tok in raw:
    if merged and tok['word'].startswith('##') and tok['entity_group'] == merged[-1]['entity_group']:
        merged[-1]['word'] += tok['word'][2:]
        merged[-1]['end']   = tok['end']
        merged[-1]['score'] = max(merged[-1]['score'], tok['score'])
    else:
        merged.append(tok)
print(merged)
