from pathlib import Path
import sys
import json
import hashlib

import torch
import yaml
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer

PROJECT = Path.home() / "open-unlearning"
REPORT = PROJECT / "reports/Recovery01_Clean_RMU_QuasiIdentifier"
sys.path.insert(0, str(PROJECT / "src"))

from data.utils import preprocess_chat_instance

PROTOCOL = REPORT / "RECOVERY_PROTOCOL_V1_FROZEN.json"
OUTPUT = REPORT / "step0_baseline.json"

EXPECTED_MODEL_SHA256 = (
    "ce7a76c51ccfee749f1c3bc50ac8ea64b483c4bdc2cb4ccdc19b0279a1b66354"
)

TARGETS = {
    "B0": {"index": 0, "name": "Basil Mahfouz Al-Kuwaiti"},
    "N20": {"index": 20, "name": "Nikolai Abilov"},
}


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(4 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


@torch.inference_mode()
def average_answer_logp(model, tokenizer, template_args, question, answer):
    sample = preprocess_chat_instance(
        tokenizer=tokenizer,
        template_config=template_args,
        prompt_msgs=[question],
        response_msgs=[answer],
        max_length=512,
        predict_with_generate=False,
    )

    ids = sample["input_ids"].unsqueeze(0).to(model.device)
    labels = sample["labels"].unsqueeze(0).to(model.device)
    attention_mask = sample["attention_mask"].unsqueeze(0).to(model.device)

    logits = model(
        input_ids=ids,
        attention_mask=attention_mask,
        use_cache=False,
    ).logits.float()

    log_probs = torch.log_softmax(logits[:, :-1, :], dim=-1)
    shifted_labels = labels[:, 1:]
    valid = shifted_labels != -100

    selected = log_probs.gather(
        -1,
        shifted_labels.clamp_min(0).unsqueeze(-1),
    ).squeeze(-1)

    count = int(valid.sum().item())
    if count == 0:
        raise ValueError("没有有效监督 Token")

    return {
        "mean_logp": float(selected[valid].mean().item()),
        "sum_logp": float(selected[valid].sum().item()),
        "token_count": count,
    }


@torch.inference_mode()
def greedy_generate(model, tokenizer, template_args, question):
    messages = [
        {"role": "system", "content": template_args["system_prompt"]},
        {"role": "user", "content": question},
    ]

    inputs = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt",
        date_string=template_args.get("date_string"),
    ).to(model.device)

    attention_mask = torch.ones_like(inputs)

    outputs = model.generate(
        input_ids=inputs,
        attention_mask=attention_mask,
        max_new_tokens=128,
        do_sample=False,
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id,
    )

    return tokenizer.decode(
        outputs[0, inputs.shape[1]:],
        skip_special_tokens=True,
    )


def main():
    if OUTPUT.exists():
        raise SystemExit(f"拒绝覆盖现有基线: {OUTPUT}")

    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    if protocol["status"] != "PROTOCOL_FROZEN_NOT_TRAINED":
        raise RuntimeError("冻结协议状态异常")

    model_dir = (PROJECT / protocol["starting_model"]).resolve()
    model_file = model_dir / "model.safetensors"

    if sha256_file(model_file) != EXPECTED_MODEL_SHA256:
        raise RuntimeError("RMU_Clean01 模型哈希不一致，停止执行")

    model_cfg = yaml.safe_load(
        (PROJECT / "configs/model/Llama-3.2-1B-Instruct.yaml").read_text(
            encoding="utf-8"
        )
    )
    template_args = model_cfg["template_args"]

    dataset = load_dataset("locuslab/TOFU", "forget01", split="train")
    if len(dataset) != 40:
        raise RuntimeError("forget01 数据集长度异常")

    tokenizer = AutoTokenizer.from_pretrained(
        str(model_dir),
        local_files_only=True,
    )
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA 不可用，停止执行")

    model = AutoModelForCausalLM.from_pretrained(
        str(model_dir),
        torch_dtype=torch.bfloat16,
        attn_implementation="sdpa",
        local_files_only=True,
    ).cuda().eval()

    results = {
        "experiment": "Recovery01",
        "stage": "Step0",
        "model_sha256": EXPECTED_MODEL_SHA256,
        "targets": {},
    }

    for target_id, spec in TARGETS.items():
        row = dataset[spec["index"]]
        question = row["question"]
        full_answer = row["answer"]
        name = spec["name"]

        wrong_name = next(
            item["name"]
            for other_id, item in TARGETS.items()
            if other_id != target_id
        )

        full_score = average_answer_logp(
            model, tokenizer, template_args, question, full_answer
        )
        name_score = average_answer_logp(
            model, tokenizer, template_args, question, name
        )
        wrong_score = average_answer_logp(
            model, tokenizer, template_args, question, wrong_name
        )

        generation = greedy_generate(
            model, tokenizer, template_args, question
        )

        result = {
            "index": spec["index"],
            "question": question,
            "reference_answer": full_answer,
            "target_name": name,
            "full_answer": full_score,
            "correct_name": name_score,
            "wrong_name": wrong_score,
            "name_margin": (
                name_score["mean_logp"] - wrong_score["mean_logp"]
            ),
            "greedy_generation": generation,
            "exact_name_match": name.lower() in generation.lower(),
        }

        results["targets"][target_id] = result

        print(f"\n[{target_id}]")
        print("姓名 LogP:", name_score["mean_logp"])
        print("错误姓名 LogP:", wrong_score["mean_logp"])
        print("姓名 Margin:", result["name_margin"])
        print("生成结果:", generation)
        print("完整姓名命中:", result["exact_name_match"])

    OUTPUT.write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("\nStep 0 基线保存:", OUTPUT)
    print("未执行任何训练或模型权重更新。")


if __name__ == "__main__":
    main()
