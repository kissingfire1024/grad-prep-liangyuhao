# Experiment 004 — 问题记录 和 注意事项

## 1. Hydra max_steps override

The initial one-step 记忆 probe used:

    trainer.args.max_steps=1

Hydra rejected this因为the key 为 not present在the active 配置.

Correct form:

    +trainer.args.max_steps=1

The 失败 attempt did not perform model 训练.

## 2. RMU requires a 参考模型

The current OpenUnlearning RMU 实现 creates/prepares a 参考模型
for the representation-preservation objective.

This increases 记忆 requirements 与……相比 methods that do not require a
参考模型.

## 3. Layer-7 objective does not 均值 layer-7-only 训练

RMU computes the relevant representation losses at:

    model.layers.7

However:

    trainable_params_regex:
      - .*

matches 全部 parameters.

Therefore descriptions claiming that 仅 layer 7 为 trained would be
incorrect用于本实验.

## 4. 模型 效用崩溃

Final 评估 reported:

    model_utility = 0.0

Therefore low forget-set ROUGE/概率 cannot be interpreted independently
as 成功 选择性遗忘.

## 5. Qualitative degeneration

Selected maximum-ROUGE-drop examples showed severe repetitive generation.

Because the examples 为 已选择 according到maximum degradation, they prove
that degeneration exists但do not establish its frequency over the 完成
遗忘集.

## 6. Forget 真实性比率

Forget 真实性比率 应当 not be interpreted independently作为a simple
higher-is-better 或 lower-is-better score.

It 必须 be interpreted together 使用 遗忘质量, utility, 和 other
遗忘 metrics.

## 7. PrivLeak

PrivLeak 是 retained用于reproducibility,但direct absolute 比较 应当
be treated cautiously因为the Retain99 reference 评估 previously
produced a retain-log/reference 警告.

## 8. Scope limitation

本实验 uses TOFU fictitious-author data.

It does not establish conclusions about 临床 LLMs, patient-level 遗忘,
医学 隐私, 或 cardiovascular 记录.

## 9. No latent-deletion conclusion

该实验 measures output/评估 behavior 和 RMU objective
optimization.

It does not demonstrate that latent representations containing the forgotten
information have been permanently erased.

## 10. No relearning-resistance conclusion

No 再学习 或 恢复 攻击 为 performed在Experiment 004.

Resistance到再学习 remains a separate experimental 问题.
