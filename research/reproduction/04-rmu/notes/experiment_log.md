# Experiment 004 — RMU 实验日志

## 目标

Evaluate the 官方 OpenUnlearning RMU baseline在TOFU forget01 under the
相同 general experimental protocol used用于previous baselines.

## Pre-training inspection

The RMU source 和 YAML 配置 为 inspected 之前 训练.

Key observation:

- representation objective module: model.layers.7
- 保留 objective: EMBED_DIFF
- trainable_params_regex: .*
- approximately 1.236B model parameters 是 已纳入 by the 配置

Therefore 该实验 不得 be described作为updating 仅 layer 7.

## Memory probe

A one-step RMU probe 为 performed 之前 正式 训练.

结果:

- no OOM
- observed peak GPU 记忆: approximately 7712 MiB
- RTX 4070 SUPER 12GB 为 sufficient用于the 官方 配置

## 正式 训练

训练 已完成:

- 100 steps
- 10 epochs
- 运行时间: 364.441 s (~6.07 min)
- 20 logged 损失 记录
- first logged 损失: 0.0533
- final logged 损失: 0.0162
- minimum logged 损失: 0.0162
- no NaN/Inf/OOM observed

## 评估

TOFU 评估 已完成 successfully 使用 batch size 1.

Final RMU metrics:

- extraction_strength: 0.02905940823391865
- forget_Q_A_Prob: 2.2900104522705077e-05
- forget_Q_A_ROUGE: 0.013661529357140503
- forget_quality: 0.02860307028023343
- forget_truth_ratio: 0.7866961809766119
- model_utility: 0.0
- privleak: 22.294887034997405

## Qualitative analysis

The three largest Retain99-to-RMU ROUGE-L decreases 为 inspected.

Selected samples:

- sample 1: 1.0 -> 0.0
- sample 0: 0.7142857143 -> 0.0
- sample 2: 0.7142857143 -> 0.0

Selected outputs exhibited severe repetitive token/character degeneration.

These examples 为 intentionally 已选择作为the largest degradation cases and
不得 be interpreted作为an unbiased estimate 的 失败 prevalence.

## Main observation

RMU strongly suppressed forget-set 答案 behavior,但模型效用 为 zero
在当前实验设置下.

Convergence 的 the RMU 训练 objective因此did not imply 成功
utility-preserving selective 机器遗忘.

## Next research relevance

本实验 provides a representation-level baseline用于later experiments
on:

- latent residual 记忆
- representation 恢复
- 再学习 attacks
- patient-level selective 机器遗忘
- patient-aware variants 的 representation scrubbing
