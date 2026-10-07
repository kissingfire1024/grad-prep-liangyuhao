# OpenUnlearning Experiment Log

## Experiment 001

### 目标

在本地 RTX 4070 SUPER 12GB 环境中复现 OpenUnlearning，
完成 TOFU + Llama-3.2-1B-Instruct + GradAscent 的完整训练与评估流程。

---

## 环境

- OS: Windows + WSL2 Ubuntu
- GPU: RTX 4070 SUPER 12GB
- Python: 3.11.16
- CUDA Toolkit: 12.1
- PyTorch: 2.4.1+cu121
- OpenUnlearning commit: 4ad738a

Conda environment:

openunlearning

---

## Step 1：OpenUnlearning 环境验证

完成：

- OpenUnlearning repository clone
- Python dependencies 安装
- CUDA Toolkit 12.1 安装
- DeepSpeed import 验证
- PyTorch CUDA 验证
- RTX 4070 SUPER GPU 验证

结果：

OpenUnlearning 可以正常 import，
PyTorch 可以正常调用 GPU。

---

## Step 2：Single-GPU 配置

创建：

configs/accelerate/single_gpu.yaml

配置：

- num_processes = 1
- distributed_type = NO
- mixed_precision = bf16

Accelerate 单 GPU 测试成功。

---

## Step 3：模型准备

使用：

open-unlearning/tofu_Llama-3.2-1B-Instruct_full

由于 Meta Llama tokenizer 存在 gated access，
模型和 tokenizer 均改用 OpenUnlearning 提供的公开 checkpoint。

同时禁用 FlashAttention2，改用：

attn_implementation = sdpa

---

## Step 4：GradAscent Training

Dataset:

TOFU

Split:

- forget01
- retain99

训练设置：

- batch size = 1
- gradient accumulation = 4
- gradient checkpointing = true
- evaluation during training = disabled

训练完成：

- 100 / 100 steps
- 10 epochs
- runtime ≈ 956 seconds
- train loss ≈ -325.257

GradAscent loss 为负值属于目标函数设计结果，
不能按照普通 Cross-Entropy loss 的下降方式解释。

---

## Step 5：Retain99 Reference Evaluation

Reference model:

open-unlearning/tofu_Llama-3.2-1B-Instruct_retain99

主要结果：

- Forget Q/A Prob = 0.1656097
- Forget Q/A ROUGE = 0.4121098
- Forget Truth Ratio = 0.6515837
- Model Utility = 0.5988637
- Extraction Strength = 0.0692821

---

## Step 6：GradAscent Evaluation

主要结果：

- Forget Q/A Prob = 0
- Forget Q/A ROUGE = 0
- Forget Truth Ratio = 1.7369e-32
- Forget Quality = 1.8603e-23
- Model Utility = 0
- PrivLeak = -27.5862
- Extraction Strength = 0.0290594

---

## 实验结论

GradAscent 对 forget01 产生了非常强的遗忘效果。

但是：

Model Utility = 0

说明模型整体能力发生严重退化。

因此 Experiment 001 证明：

“Forget 指标下降”并不等价于“高质量选择性遗忘”。

一个有效的 Machine Unlearning 方法需要同时满足：

1. Forget target information
2. Preserve retain knowledge
3. Preserve general model utility

GradAscent 将作为后续实验的基础 baseline。

---

## 下一实验

Experiment 002:

GradDiff

保持以下条件尽量不变：

- Same model
- Same TOFU split
- Same GPU
- Same evaluation pipeline

然后与 GradAscent 进行直接比较。
