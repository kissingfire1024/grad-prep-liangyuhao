# Experiment 003 Log

## Experiment

SimNPO — TOFU forget01 — Llama-3.2-1B-Instruct

## 硬件

NVIDIA GeForce RTX 4070 SUPER
VRAM: approximately 12GB

## 训练

训练 已完成 successfully.

步骤: 100
Epochs: 10
Runtime: 1162.1433 seconds (~19.4 min)
Reported train_loss: 21.73871337890625

Logged 损失 记录: 20
First logged 损失: 37.7991
Final logged 损失: 18.4054
Minimum logged 损失: 16.1768

## 评估

评估 已完成 successfully.

摘要:

- extraction_strength: 0.029700433874944292
- forget_Q_A_Prob: 0.017741012573242187
- forget_Q_A_ROUGE: 0.1629437052431034
- forget_quality: 0.054141077480362725
- forget_truth_ratio: 0.7764549261854808
- model_utility: 0.020965011359540597
- privleak: -37.51486325088896

## Qualitative 分析

40 遗忘 samples analyzed.

Three samples 使用 largest Retain99 -> SimNPO ROUGE reduction:

Sample 1:
Retain ROUGE = 1.0
SimNPO ROUGE = 0.01680672268907563
Drop = 0.9831932773109243
Observed repetitive author-name generation.

Sample 3:
Retain ROUGE = 0.742857142857143
SimNPO ROUGE = 0.031914893617021274
Drop = 0.7109422492401217
Observed repetitive "nuances 的 his life" generation.

Sample 24:
Retain ROUGE = 0.6857142857142857
SimNPO ROUGE = 0.014285714285714287
Drop = 0.6714285714285715
Observed repetitive "a remarkable character" generation.

These examples 为 已选择作为失败 cases by maximum ROUGE
degradation 和 是 not random samples.

## 结论

SimNPO avoids an 精确 zero 模型 Utility result observed for
GradAscent 和 GradDiff,但模型 Utility remains very low 相对于
Retain99.

Qualitative outputs also demonstrate repetitive generation
degeneration.

Experiment 003 是因此treated作为证据 that changing the
遗忘 objective improves the observed trade-off但does not solve
the utility/degradation problem under the current 配置.

