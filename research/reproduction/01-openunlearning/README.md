# OpenUnlearning Reproduction

## 1. 实验目的

复现 OpenUnlearning 在 TOFU 数据集上的 Machine Unlearning 实验。

本阶段首先复现 GradAscent baseline，用于验证：

- OpenUnlearning 环境
- TOFU 数据集
- Llama-3.2-1B-Instruct
- Machine Unlearning 训练流程
- TOFU 评估 流程

后续将在相同实验环境下继续复现 GradDiff、NPO、RMU、OUR 和 Relearning 攻击。

## 2. 实验环境

- OS: Windows + WSL2 Ubuntu
- GPU: NVIDIA GeForce RTX 4070 SUPER
- VRAM: 12 GB
- CUDA Toolkit: 12.1
- Python: 3.11.16
- Conda: openunlearning
- PyTorch: 2.4.1+cu121
- Transformers: 4.51.3
- Datasets: 3.0.1
- Accelerate: 0.34.2
- DeepSpeed: 0.15.4

## 3. OpenUnlearning

Repository:
https://github.com/locuslab/open-unlearning

Local directory:

/home/research/open-unlearning

Git commit:

4ad738a

## 4. 实验设置

模型:

Llama-3.2-1B-Instruct

数据集:

TOFU

Split:

- Forget: forget01
- Retain: retain99
- Holdout: holdout01

Unlearning 方法:

GradAscent

GPU 配置:

- Single GPU
- batch_size = 1
- gradient_accumulation_steps = 4
- gradient_checkpointing = true
- attention = SDPA

## 5. 实验脚本

训练：

scripts/01_gradascent_train.sh

Retain99 参考 评估：

scripts/02_retain99_eval.sh

GradAscent 评估：

scripts/03_gradascent_eval.sh

## 6. 实验结果

### Retain99

- Forget Q/A Prob: 0.1656097
- Forget 问答 ROUGE: 0.4121098
- Forget 真实性比率: 0.6515837
- 模型 Utility: 0.5988637
- 提取强度: 0.0692821

### GradAscent Forget01

- Forget Q/A Prob: 0.0
- Forget 问答 ROUGE: 0.0
- Forget 真实性比率: 1.7369e-32
- 遗忘质量: 1.8603e-23
- 模型 Utility: 0.0
- PrivLeak: -27.5862
- 提取强度: 0.0290594

## 7. 初步结论

GradAscent 能够非常强烈地抑制 遗忘 数据。

Forget 问答概率 和 Forget 问答 ROUGE 均下降至 0。

但是 模型 Utility 同样下降至 0。

因此，该结果不能简单解释为成功的选择性遗忘，而更接近：

强遗忘 + 严重 Utility Degradation。

后续需要与 GradDiff、NPO、RMU、OUR 等方法进行比较。

## 8. 兼容性修改

RTX 4070 SUPER 12GB 环境下进行了以下修改：

1. FlashAttention2 改为 SDPA。
2. TOFU 评估 batch size 从 32 改为 1。
3. 关闭训练过程中的自动 评估。
4. 修复 BF16 Tensor 转 NumPy 的兼容性问题。

详细记录见：

notes/issues.md

## 9. 文件结构

code/
- 本次实验涉及的 OpenUnlearning 源代码和配置

scripts/
- 实际使用的训练和评估脚本

results/retain99/
- Retain99 reference 评估

results/gradascent_forget01/
- GradAscent 评估

notes/
- 实验过程和问题记录

## 10. 下一阶段

GradAscent
→ GradDiff
→ NPO
→ RMU
→ OUR
→ Latent Residual 分析
→ Relearning 攻击
→ Clinical Patient-level Unlearning
→ Cross-record 恢复
