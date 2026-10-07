# OpenUnlearning Issues & Solutions

本文档记录 OpenUnlearning + TOFU 在 RTX 4070 SUPER 12GB
环境中的主要问题及解决方案。

---

## Issue 1：WSL 无法直接访问 Hugging Face

### 现象

WSL 中访问 Hugging Face 出现网络连接问题。

Windows 使用本地代理：

127.0.0.1:7897

WSL NAT 模式无法直接使用 Windows localhost。

### 解决

通过 WSL gateway 访问 Windows 代理，并设置：

HTTP_PROXY

HTTPS_PROXY

验证 Hugging Face 可以正常访问后继续下载模型。

---

## Issue 2：Hugging Face Xet 下载模型非常慢

### 现象

下载：

open-unlearning/tofu_Llama-3.2-1B-Instruct_full

时 model.safetensors 长时间停留在约 97%。

### 解决

设置：

export HF_HUB_DISABLE_XET=1

然后重新使用 huggingface_hub 下载模型。

最终 model.safetensors 下载成功。

---

## Issue 3：Meta Llama Tokenizer 401

### 现象

模型权重使用 OpenUnlearning 的公开 checkpoint，
但 tokenizer 默认仍然指向：

meta-llama/Llama-3.2-1B-Instruct

导致 gated repository 401 Unauthorized。

### 解决

同时覆盖 model 和 tokenizer：

model:
open-unlearning/tofu_Llama-3.2-1B-Instruct_full

tokenizer:
open-unlearning/tofu_Llama-3.2-1B-Instruct_full

因此当前 TOFU 实验不需要 Meta Llama gated access。

---

## Issue 4：FlashAttention2 未安装

### 现象

默认模型配置使用：

flash_attention_2

本地环境没有安装 flash_attn。

### 解决

没有额外编译 FlashAttention。

直接改为：

attn_implementation=sdpa

这样可以减少环境复杂度，并能够在 RTX 4070 SUPER 上正常运行。

---

## Issue 5：DeepSpeed 无法正常 import

### 现象

OpenUnlearning 的 trainer 会导入 DeepSpeed。

最初系统只有 NVIDIA Windows/WSL 驱动，
没有完整 CUDA Toolkit 和 nvcc。

### 解决

安装 NVIDIA 官方 WSL CUDA Toolkit 12.1。

CUDA_HOME：

/usr/local/cuda-12.1

设置：

export CUDA_HOME=/usr/local/cuda-12.1
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:${LD_LIBRARY_PATH:-}

验证：

nvcc --version

以及：

import train

均成功。

注意：

没有在 WSL 中额外安装 NVIDIA Linux GPU Driver。

---

## Issue 6：GradAscent 训练过程中 Evaluation OOM

### 现象

GradAscent 已经能够训练。

但是完成一个 epoch 后自动启动 TOFU evaluation，
RTX 4070 SUPER 12GB 出现 CUDA Out Of Memory。

仅设置：

do_eval=false

仍然会触发 epoch evaluation。

### 原因

trainer 配置仍包含：

eval_strategy=epoch

### 解决

训练时增加：

trainer.args.do_eval=false
trainer.args.eval_on_start=false
trainer.args.eval_strategy=no

训练与完整 evaluation 分离执行。

---

## Issue 7：TOFU Evaluation Batch Size OOM

### 现象

TOFU evaluator 默认：

batch_size=32

RTX 4070 SUPER 12GB 无法承受该 evaluation batch size。

### 解决

设置：

eval.tofu.batch_size=1

之后完整 evaluation 可以正常运行。

---

## Issue 8：BF16 转 NumPy 报错

### 错误

TypeError: Got unsupported ScalarType BFloat16

### 文件

src/evals/metrics/utils.py

### 原代码

avg_losses = avg_losses.cpu().numpy().tolist()

normalized_probs = normalized_probs.cpu().numpy().tolist()

### 修改

avg_losses = avg_losses.float().cpu().numpy().tolist()

normalized_probs = normalized_probs.float().cpu().numpy().tolist()

### 原因

NumPy 不能直接处理这里的 PyTorch BFloat16 Tensor。

先转换为 float32 后再转换为 NumPy。

---

## Issue 9：TOFU Dataset 在线访问失败

### 现象

GradAscent evaluation 过程中，
在线访问 locuslab/TOFU 一度失败。

### 结果

Hugging Face datasets 自动使用本地缓存。

缓存中的 TOFU 数据完整，因此 evaluation 正常完成。

这不是实验失败。

---

# 最终可用配置

当前已经验证可以工作的组合：

- RTX 4070 SUPER 12GB
- WSL2 Ubuntu
- CUDA Toolkit 12.1
- Python 3.11
- PyTorch 2.4.1+cu121
- OpenUnlearning
- Single GPU
- BF16
- SDPA
- Evaluation batch size = 1

该环境已经成功完成：

TOFU
+
Llama-3.2-1B-Instruct
+
GradAscent
+
完整 TOFU Evaluation
