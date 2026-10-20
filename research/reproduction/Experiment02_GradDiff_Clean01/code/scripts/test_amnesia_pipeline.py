import sys
from pathlib import Path

import torch
from omegaconf import OmegaConf
from transformers import AutoTokenizer

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from data import get_data

ROOT = Path(__file__).resolve().parents[1]

model_cfg = OmegaConf.load(
    ROOT / "configs/model/Qwen2.5-1.5B-Instruct.yaml"
)

tokenizer_name = model_cfg.tokenizer_args.pretrained_model_name_or_path

print("Tokenizer:", tokenizer_name)

tokenizer = AutoTokenizer.from_pretrained(
    tokenizer_name,
    local_files_only=True,
)

print("Tokenizer 加载成功")

forget_cfg = OmegaConf.load(
    ROOT / "configs/data/datasets/AMNESIA_CVD_forget.yaml"
)

retain_cfg = OmegaConf.load(
    ROOT / "configs/data/datasets/AMNESIA_CVD_retain.yaml"
)

data_cfg = OmegaConf.create({
    "anchor": "forget",
    "forget": forget_cfg,
    "retain": retain_cfg,
})

datasets = get_data(
    data_cfg,
    mode="unlearn",
    tokenizer=tokenizer,
    template_args=model_cfg.template_args,
)

train_dataset = datasets["train"]

print("\n===== 数据集长度 =====")
print("Forget:", len(train_dataset.forget))
print("Retain:", len(train_dataset.retain))
print("训练配对数:", len(train_dataset))

sample = train_dataset[0]

print("\n===== 样本检查 =====")

for split in ["forget", "retain"]:
    item = sample[split]

    input_ids = item["input_ids"]
    labels = item["labels"]
    attention_mask = item["attention_mask"]

    valid_labels = (labels != -100).sum().item()

    print(f"\n{split}")
    print("input_ids shape:", tuple(input_ids.shape))
    print("labels shape:", tuple(labels.shape))
    print("attention_mask shape:", tuple(attention_mask.shape))
    print("有效答案 Token 数:", valid_labels)

    assert input_ids.shape == labels.shape
    assert input_ids.shape == attention_mask.shape
    assert valid_labels > 0, f"{split} 没有有效训练标签"

print("\n===== 前 100 条 Forget 样本检查 =====")

invalid = 0
truncated = 0

for i in range(min(100, len(train_dataset.forget))):
    item = train_dataset.forget[i]

    valid = (item["labels"] != -100).sum().item()

    if valid == 0:
        invalid += 1

    if len(item["input_ids"]) >= 512:
        truncated += 1

print("无有效答案标签样本数:", invalid)
print("达到 512 Token 的样本数:", truncated)

print("\nAMNESIA 数据管线测试完成")
