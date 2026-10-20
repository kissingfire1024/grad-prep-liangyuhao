import json
import random
from pathlib import Path
from transformers import AutoTokenizer

ROOT = Path.home() / "open-unlearning"
DATA = ROOT / "data/medical/amnesia_cv5"
OUT = ROOT / "reports/medical_unlearning/01_med000"

tokenizer = AutoTokenizer.from_pretrained(
    "Qwen/Qwen2.5-0.5B-Instruct",
    local_files_only=True
)

def load(filename):
    with open(filename, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

def stats(lengths):
    values = sorted(lengths)
    n = len(values)

    def pct(p):
        return values[min(int((n - 1) * p), n - 1)]

    result = {
        "count": n,
        "mean": round(sum(values) / n, 2),
        "p50": pct(0.50),
        "p90": pct(0.90),
        "p95": pct(0.95),
        "p99": pct(0.99),
        "max": values[-1],
    }

    for limit in (512, 1024, 2048):
        count = sum(x > limit for x in values)
        result[f"over_{limit}"] = count
        result[f"over_{limit}_pct"] = round(
            count / n * 100, 2
        )
        result[f"token_coverage_{limit}_pct"] = round(
            sum(min(x, limit) for x in values)
            / sum(values) * 100, 2
        )

    return result

print("===== PATIENT NOTES =====", flush=True)

notes = load(DATA / "train_pretrain_notes.jsonl")

note_lengths = [
    len(tokenizer.encode(
        row["text"],
        add_special_tokens=False
    ))
    for row in notes
]

note_stats = stats(note_lengths)

for key, value in note_stats.items():
    print(f"{key}: {value}")

print("\n===== QA TOKEN LENGTH =====", flush=True)

qa = load(DATA / "train_sft_qa.jsonl")

rng = random.Random(42)
qa_sample = rng.sample(qa, min(2000, len(qa)))

qa_lengths = []

for row in qa_sample:
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": row["question"]
        }
    ]

    prompt_ids = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True
    )

    answer_ids = tokenizer.encode(
        row["answer"],
        add_special_tokens=False
    )

    qa_lengths.append(
        len(prompt_ids) + len(answer_ids) + 1
    )

qa_stats = stats(qa_lengths)

for key, value in qa_stats.items():
    print(f"{key}: {value}")

result = {
    "model": "Qwen2.5-0.5B-Instruct",
    "notes": note_stats,
    "qa_sample": qa_stats,
    "qa_sample_size": len(qa_sample),
    "notes_length_method": "tokenizer without special tokens",
    "qa_length_method": "approximate chat-template plus answer"
}

output = OUT / "med000d_length_audit.json"

with open(output, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print("\nAUDIT COMPLETED")
print("Saved:", output)
