# Experiment 002 — GradDiff Unlearning在TOFU

## 目的

Evaluate GradDiff作为an OpenUnlearning baseline在TOFU forget01 和 test
whether adding a 保留 objective prevents the 效用崩溃 observed
使用 GradAscent.

## Setup

- Framework: OpenUnlearning
- Git commit: 4ad738a
- 模型: open-unlearning/tofu_Llama-3.2-1B-Instruct_full
- Forget split: forget01
- Retain split: retain99
- Holdout split: holdout01
- GPU: NVIDIA GeForce RTX 4070 SUPER, ~12 GB
- Python: 3.11.16
- PyTorch: 2.4.1+cu121
- GradDiff gamma: 1.0
- GradDiff alpha: 1.0
- Retain 损失: NLL
- Epochs: 10
- Learning rate: 1e-5
- Batch size: 1
- Gradient accumulation: 4
- Gradient checkpointing: enabled
- Attention: SDPA

GradDiff objective:

L = gamma * (-L_forget) + alpha * L_retain

## 训练 结果

训练 已完成 successfully.

- 步骤: 100/100
- Epochs: 10
- Runtime: 4273.7658 s (~71.2 min)
- Reported train 损失: -204.2973606
- First logged 损失: -1.2456
- Final logged 损失: -293.8376

## 评估 结果

| 指标 | Retain99 | GradAscent | GradDiff |
|---|---:|---:|---:|
| Forget Q/A Prob | 0.165610 | 0 | 7.636845e-09 |
| Forget 问答 ROUGE | 0.412110 | 0 | 0.003261 |
| Forget 真实性比率 | 0.651584 | 1.736914e-32 | 0.000251 |
| 模型 Utility | 0.598864 | 0 | 0 |
| 提取强度 | 0.069282 | 0.029059 | 0.029059 |

GradDiff 遗忘质量: 5.878676e-20

GradDiff PrivLeak: 90.2497

Note: Retain99 PrivLeak 是 不能直接比较因为the reference
评估 produced a retain-log/reference 警告.

## Qualitative 结果

40 遗忘 examples 为 exported.

The three examples 使用 the largest Retain99-to-GradDiff ROUGE-L 下降
were samples 1, 3, 和 2.

All three showed severe repetitive generation degeneration,用于example:

    -e-e-e-e-e-e-e-e-e-e-e-e-...

Therefore, the 模型 Utility value 的 0.0 是 accompanied by directly
observable generation degeneration.

## Main Finding

Under this specific experimental 配置, GradDiff strongly suppresses
the 目标 遗忘 data但does not preserve overall 模型效用.

The 保留 NLL term 使用 gamma=1 和 alpha=1 为 insufficient到prevent
severe generation degeneration 和 效用崩溃.

This result 是 specific到the tested 配置 和 应当 not be
interpreted作为a general claim that GradDiff 是 ineffective.

The central observation is:

**Strong output suppression 是 not equivalent到成功 selective
机器遗忘.**

## 实验产物

Figures:

- results/graddiff_forget01/figures/01_training_loss.png
- results/graddiff_forget01/figures/02_metrics_comparison.png
- results/graddiff_forget01/figures/03_forget_examples.png

Tables:

- results/graddiff_forget01/tables/training_loss.csv
- results/graddiff_forget01/tables/metrics_comparison.csv
- results/graddiff_forget01/tables/forget_examples.csv

Raw 评估:

- results/graddiff_forget01/TOFU_EVAL.json
- results/graddiff_forget01/TOFU_SUMMARY.json
- results/graddiff_forget01/trainer_state.json

Scripts:

- scripts/01_graddiff_train.sh
- scripts/02_graddiff_eval.sh

检查点:

/home/research/open-unlearning/saves/unlearn/tofu_Llama-3.2-1B-Instruct_forget01_GradDiff_test

The ~2.4 GB checkpoint 是 intentionally not duplicated into the reproduction
directory.

## 状态

**Experiment 002: COMPLETE**

- 训练: 通过
- 评估: 通过
- Quantitative analysis: 通过
- Qualitative analysis: 通过
- Reproduction artifacts: PRESERVED
