import sys
import json
import gc
import re
from collections import Counter
from pathlib import Path

import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForCausalLM
from omegaconf import OmegaConf

ROOT = Path.home() / "open-unlearning"
OUT = ROOT / "reports/medical_unlearning/02_med000f"
SAMPLES = OUT / "samples"

sys.path.insert(0, str(ROOT / "src"))
from data.qa import QADataset

MODELS = {
    "Base": "Qwen/Qwen2.5-0.5B-Instruct",
    "MED000D": str(
        ROOT / "saves/train/MED000D_NotesFull_E1_Qwen05"
    ),
    "MED000E": str(
        ROOT / "saves/train/MED000E_QAFull_E1_Qwen05"
    )
}

GROUPS = [
    "seen_forget", "seen_same", "seen_other",
    "holdout_forget", "holdout_same", "holdout_other"
]

GEN_COUNT = 8

cfg = OmegaConf.load(
    ROOT / "configs/model/Qwen2.5-0.5B-Instruct-MED.yaml"
)
template = OmegaConf.to_container(
    cfg.template_args, resolve=True
)

tokenizer = AutoTokenizer.from_pretrained(
    MODELS["Base"], local_files_only=True
)

def make_dataset(group, generate=False):
    return QADataset(
        hf_args={
            "path": "json",
            "data_files": str(SAMPLES / f"{group}.jsonl"),
            "split": "train"
        },
        template_args=template,
        tokenizer=tokenizer,
        question_key="question",
        answer_key="answer",
        max_length=512,
        predict_with_generate=generate
    )

def token_f1(pred, ref):
    a = re.findall(r"\w+", pred.lower())
    b = re.findall(r"\w+", ref.lower())
    if not a or not b:
        return 0.0
    overlap = sum((Counter(a) & Counter(b)).values())
    precision = overlap / len(a)
    recall = overlap / len(b)
    return (
        2 * precision * recall / (precision + recall)
        if precision + recall else 0.0
    )

datasets = {
    group: make_dataset(group)
    for group in GROUPS
}
generation_sets = {
    group: make_dataset(group, True)
    for group in GROUPS
}
references = {}
for group in GROUPS:
    with (SAMPLES / f"{group}.jsonl").open(
        encoding="utf-8"
    ) as f:
        references[group] = [
            json.loads(x) for x in f if x.strip()
        ]

results = {}

for model_name, path in MODELS.items():
    print("\n==========", model_name, "==========", flush=True)

    model = AutoModelForCausalLM.from_pretrained(
        path,
        torch_dtype=torch.bfloat16,
        attn_implementation="sdpa",
        local_files_only=True
    ).to("cuda")
    model.eval()

    results[model_name] = {}

    for group in GROUPS:
        dataset = datasets[group]
        total_loss = 0.0
        total_tokens = 0

        for i in range(len(dataset)):
            item = dataset[i]
            ids = item["input_ids"].unsqueeze(0).to("cuda")
            labels = item["labels"].unsqueeze(0).to("cuda")
            mask = labels[:, 1:] != -100

            if not mask.any().item():
                raise ValueError(
                    f"No valid answer tokens: {group}/{i}"
                )

            with torch.inference_mode():
                logits = model(input_ids=ids).logits
                pred_logits = logits[:, :-1, :][mask].float()
                targets = labels[:, 1:][mask]

                loss = F.cross_entropy(
                    pred_logits, targets,
                    reduction="sum"
                )

            total_loss += loss.item()
            total_tokens += targets.numel()

        nll = total_loss / total_tokens

        generated = []
        f1_values = []

        for i in range(GEN_COUNT):
            item = generation_sets[group][i]
            ids = item["input_ids"].unsqueeze(0).to("cuda")
            attention = torch.ones_like(ids)

            with torch.inference_mode():
                output = model.generate(
                    input_ids=ids,
                    attention_mask=attention,
                    max_new_tokens=128,
                    do_sample=False,
                    pad_token_id=(
                        tokenizer.pad_token_id
                        if tokenizer.pad_token_id is not None
                        else tokenizer.eos_token_id
                    )
                )

            text = tokenizer.decode(
                output[0][ids.shape[1]:],
                skip_special_tokens=True
            ).strip()

            record = references[group][i]
            f1 = token_f1(text, record["answer"])
            f1_values.append(f1)

            generated.append({
                "id": record["id"],
                "question": record["question"],
                "reference": record["answer"],
                "prediction": text,
                "token_f1": f1
            })

        results[model_name][group] = {
            "nll": nll,
            "nll_samples": len(dataset),
            "answer_tokens": total_tokens,
            "generation_samples": GEN_COUNT,
            "generation_token_f1": (
                sum(f1_values) / len(f1_values)
            ),
            "examples": generated
        }

        print(
            f"{group:20s} "
            f"NLL={nll:.4f} "
            f"Gen-F1={sum(f1_values)/len(f1_values):.4f}",
            flush=True
        )

    del model
    gc.collect()
    torch.cuda.empty_cache()

path = OUT / "med000f_pilot_results.json"
with path.open("w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\nMED-000F PILOT COMPLETED")
print("Results:", path)
