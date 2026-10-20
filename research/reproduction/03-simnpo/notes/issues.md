# Experiment 003 问题记录 和 注意事项

## 1. Utility remains severely degraded

SimNPO 模型 Utility:

0.020965011359540597

Retain99 模型 Utility:

0.5988637091894994

Therefore the non-zero utility 不应解释为 成功
utility preservation.

## 2. Repetitive generation

Qualitative 失败 cases show phrase-level repetition 和 degeneration.

This differs在surface form 来自 some GradAscent/GradDiff failures but
still represents degraded generation behavior.

## 3. Selected examples 是 intentionally difficult cases

The three plotted examples 为 已选择 using the largest
Retain99-to-SimNPO ROUGE 下降.

They demonstrate the existence 的 失败 modes但do not estimate
their frequency 跨 全部 samples.

## 4. Forget 真实性比率 requires careful interpretation

SimNPO forget_truth_ratio 是 更高比Retain99.

This metric 不应解释为 a standalone
lower-is-better score. It 必须 be considered 使用 遗忘质量 and
the other TOFU metrics.

## 5. PrivLeak 比较 limitation

The Retain99 reference 评估 previously 已生成 a
retain-log/reference 警告.

Therefore direct absolute 比较 的 Retain99 PrivLeak against the
机器遗忘 runs 应当 be avoided.

## 6. 训练 损失 比较 limitation

SimNPO, GradDiff, 和 GradAscent optimize 不同 objectives.

Their raw training-loss magnitudes 是 不能直接比较.

## 7. Scope

All conclusions 是 specific to:

- TOFU forget01
- Llama-3.2-1B-Instruct
- current OpenUnlearning 配置
- 100 训练 steps / 10 epochs
- single RTX 4070 SUPER setup

结果 应当 not be generalized到临床 或 patient-level
机器遗忘 不使用 additional experiments.

