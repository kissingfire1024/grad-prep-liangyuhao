import gc
import json
import math
import random
from pathlib import Path

import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForCausalLM

ROOT = Path.home() / "open-unlearning"
DATA = ROOT / "data/medical/amnesia_cv5"
OUT = ROOT / "reports/medical_unlearning/01_med000"

MODELS = {
    "Base": "Qwen/Qwen2.5-0.5B-Instruct",
    "MED000A": str(
        ROOT / "saves/train/MED000A_NotesSmoke_Qwen05"
    ),
    "MED000B": str(
        ROOT / "saves/train/MED000B_QASmoke_Qwen05"
    ),
}

rng = random.Random(42)
N = 8
MAX_LEN = 512

def load(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

def sample(rows):
    return rng.sample(rows, min(N, len(rows)))

train = load(DATA / "smoke/qa_smoke.jsonl")
forget_full = load(
    Path.home() / "amnesia-data"
    / "cardiovascular_forget_5_with_category.jsonl"
)

forget_ids = {str(x["id"]) for x in forget_full}

seen_forget = [
    x for x in train if str(x["id"]) in forget_ids
]
seen_retain = [
    x for x in train if str(x["id"]) not in forget_ids
]

groups = {
    "seen_forget": sample(seen_forget),
    "seen_retain": sample(seen_retain),
    "holdout_forget": sample(load(DATA / "eval_forget.jsonl")),
    "holdout_same": sample(load(DATA / "eval_same_disease.jsonl")),
    "holdout_other": sample(load(DATA / "eval_other_disease.jsonl")),
}

tokenizer = AutoTokenizer.from_pretrained(
    MODELS["Base"],
    local_files_only=True
)

def score_qa(model, question, answer):
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": question
        }
    ]

    prefix = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True
    )

    target = tokenizer(
        answer,
        add_special_tokens=False
    )["input_ids"]

    target = target + [tokenizer.eos_token_id]
    ids = prefix + target

    if len(ids) > MAX_LEN or len(target) == 0:
        return None

    inputs = torch.tensor(
        [ids],
        dtype=torch.long,
        device="cuda"
    )

    with torch.inference_mode():
        logits = model(input_ids=inputs).logits

        start = len(prefix) - 1
        end = start + len(target)

        pred = logits[0, start:end].float()
        labels = torch.tensor(
            target,
            dtype=torch.long,
            device="cuda"
        )

        loss = F.cross_entropy(
            pred,
            labels,
            reduction="sum"
        )

    return float(loss.item()), len(target)

results = {}

for name, path in MODELS.items():
    print(f"\n===== {name} =====", flush=True)

    model = AutoModelForCausalLM.from_pretrained(
        path,
        torch_dtype=torch.bfloat16,
        attn_implementation="sdpa",
        local_files_only=True
    ).to("cuda")

    model.eval()
    results[name] = {}

    for group_name, rows in groups.items():
        total_loss = 0.0
        total_tokens = 0
        valid = 0

        for row in rows:
            result = score_qa(
                model,
                row["question"],
                row["answer"]
            )

            if result is None:
                continue

            loss, tokens = result

            if not math.isfinite(loss):
                raise RuntimeError("Non-finite loss")

            total_loss += loss
            total_tokens += tokens
            valid += 1

        nll = (
            total_loss / total_tokens
            if total_tokens else None
        )

        results[name][group_name] = {
            "samples": valid,
            "tokens": total_tokens,
            "token_nll": nll
        }

        print(
            f"{group_name:20s} "
            f"samples={valid:2d} "
            f"NLL={nll}"
        , flush=True)

    del model
    gc.collect()
    torch.cuda.empty_cache()

output = OUT / "med000c_results.json"

with output.open("w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\nRESULTS SAVED:", output)
print("MED-000C FINISHED")
