from pathlib import Path
import sys
import json
import hashlib
import gc

import torch
import yaml
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer

PROJECT = Path.home() / "open-unlearning"
REPORT = PROJECT / "reports/Recovery01_Clean_RMU_QuasiIdentifier"
SCRIPT_DIR = REPORT / "scripts"

sys.path.insert(0, str(SCRIPT_DIR))

from evaluate_step0 import (
    average_answer_logp,
    greedy_generate,
    TARGETS,
)

PROTOCOL = REPORT / "RECOVERY_PROTOCOL_V1_FROZEN.json"
BASELINE = REPORT / "step0_baseline.json"
OUTPUT = REPORT / "recovery_checkpoint_results.json"

EXPECTED_BASELINE_SHA256 = (
    "59d86758d1bb8d1be0177948c58d63461f46b8fac2583fbb9069ee3451459410"
)

EXPECTED_EVALUATOR_SHA256 = (
    "7c96d41fcad56447266aa2b939f6b0606f0395377d65453738675d0f66ae95be"
)

STEPS = [5, 10, 15, 20]
GROUPS = ["Attack", "Control"]


def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(4 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if OUTPUT.exists():
        raise RuntimeError(f"拒绝覆盖已有评估结果: {OUTPUT}")

    protocol = json.loads(
        PROTOCOL.read_text(encoding="utf-8")
    )
    assert protocol["status"] == "PROTOCOL_FROZEN_NOT_TRAINED"

    assert sha256_file(BASELINE) == EXPECTED_BASELINE_SHA256
    assert sha256_file(
        SCRIPT_DIR / "evaluate_step0.py"
    ) == EXPECTED_EVALUATOR_SHA256

    baseline = json.loads(
        BASELINE.read_text(encoding="utf-8")
    )

    model_dir = (
        PROJECT / protocol["starting_model"]
    ).resolve()

    assert sha256_file(
        model_dir / "model.safetensors"
    ) == protocol["sha256"]["model"]

    # 评估前确认八份检查点均存在
    checkpoints = {}

    for group in GROUPS:
        checkpoints[group] = {}

        for step in STEPS:
            path = (
                PROJECT / "saves/train"
                / f"Recovery01_CleanRMU_{group}"
                / f"checkpoint-{step}"
            )

            assert (path / "model.safetensors").is_file()
            assert (path / "config.json").is_file()

            checkpoints[group][step] = path

    assert torch.cuda.is_available(), "CUDA 不可用"

    config = yaml.safe_load(
        (
            PROJECT / "configs/model/Llama-3.2-1B-Instruct.yaml"
        ).read_text(encoding="utf-8")
    )
    template_args = config["template_args"]

    tokenizer = AutoTokenizer.from_pretrained(
        str(model_dir),
        local_files_only=True,
    )

    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token

    dataset = load_dataset(
        "locuslab/TOFU",
        "forget01",
        split="train",
    )
    assert len(dataset) == 40

    results = {
        "experiment": "Recovery01",
        "stage": "CheckpointRecoveryEvaluation",
        "protocol_version": "1.0",
        "baseline_sha256": EXPECTED_BASELINE_SHA256,
        "evaluator_sha256": EXPECTED_EVALUATOR_SHA256,
        "steps": STEPS,
        "groups": {},
    }

    for group in GROUPS:
        results["groups"][group] = {}

        for step in STEPS:
            path = checkpoints[group][step]

            print(
                f"\n========== {group} Step {step} ==========",
                flush=True,
            )

            model = AutoModelForCausalLM.from_pretrained(
                str(path),
                torch_dtype=torch.bfloat16,
                attn_implementation="sdpa",
                local_files_only=True,
            ).cuda().eval()

            step_results = {
                "checkpoint": str(path),
                "targets": {},
            }

            for target_id, spec in TARGETS.items():
                row = dataset[spec["index"]]
                question = row["question"]
                full_answer = row["answer"]
                correct_name = spec["name"]

                wrong_name = next(
                    item["name"]
                    for other_id, item in TARGETS.items()
                    if other_id != target_id
                )

                full_score = average_answer_logp(
                    model, tokenizer, template_args,
                    question, full_answer,
                )

                correct_score = average_answer_logp(
                    model, tokenizer, template_args,
                    question, correct_name,
                )

                wrong_score = average_answer_logp(
                    model, tokenizer, template_args,
                    question, wrong_name,
                )

                generation = greedy_generate(
                    model, tokenizer, template_args, question
                )

                margin = (
                    correct_score["mean_logp"]
                    - wrong_score["mean_logp"]
                )

                base = baseline["targets"][target_id]

                result = {
                    "index": spec["index"],
                    "target_name": correct_name,
                    "full_answer": full_score,
                    "correct_name": correct_score,
                    "wrong_name": wrong_score,
                    "name_margin": margin,
                    "greedy_generation": generation,
                    "exact_name_match": (
                        correct_name.lower()
                        in generation.lower()
                    ),
                    "delta_correct_name_logp": (
                        correct_score["mean_logp"]
                        - base["correct_name"]["mean_logp"]
                    ),
                    "delta_name_margin": (
                        margin - base["name_margin"]
                    ),
                }

                step_results["targets"][target_id] = result

                print(
                    f"{target_id}: "
                    f"NameLogP={correct_score['mean_logp']:.4f}, "
                    f"Margin={margin:.4f}, "
                    f"Exact={result['exact_name_match']}",
                    flush=True,
                )
                print(
                    "生成:", generation,
                    flush=True,
                )

            results["groups"][group][str(step)] = step_results

            del model
            gc.collect()
            torch.cuda.empty_cache()

    # 八份检查点全部评估成功后才写最终结果
    OUTPUT.write_text(
        json.dumps(results, ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )

    print("\n========== 评估完成 ==========")
    print("结果文件:", OUTPUT.resolve())
    print("Attack / Control 共 8 个 Checkpoint")
    print("未执行训练，没有修改已有模型或 Step 0 基线")


if __name__ == "__main__":
    main()
