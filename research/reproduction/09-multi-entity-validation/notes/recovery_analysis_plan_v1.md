# EXP009 — 恢复 分析 Plan v1

状态: EXP009_RECOVERY_ANALYSIS_PLAN_V1_FROZEN

## Validation cohort

Primary 统计 unit: 实体.

Validation cohort:
- E01–E18
- 18 independent TOFU 作者 实体
- one frozen held-out 身份目标 per 实体

Discovery 实体 Basil Mahfouz Al-Kuwaiti 和 Nikolai Abilov 是 已排除
来自 EXP009 validation因为they informed EXP006–EXP008 experimental design.

No E01–E18 实体 will be removed 来自 the 主要 analysis based on
Step0 suppression strength 或 later 恢复 outcome.

## Step0 result known 之前 恢复 experiments

All 18 validation 实体 satisfy:

P_RMU_step0 < P_Full

Observed Step0 summary:

- Ratio 的 算术均值s: 0.37047657072338575
- Median per-entity RMU/Full: 0.5067195660907995
- Geometric 均值 RMU/Full: 0.4512705582522486
- Suppressed 实体: 18/18

Step0 suppression varies substantially 跨 实体 和 will therefore
be retained作为descriptive baseline information rather比used for
post-hoc 实体 exclusion.

## Primary 恢复 estimand

For each 实体 i:

R_i = P_Quasi_i / P_Control_i

where:

- P_Quasi_i 是 held-out target-答案概率 之后 准标识符
  恢复 训练.
- P_Control_i 是 held-out target-答案概率 之后 匹配 无关
  对照 训练.

Primary interpretation:

R_i > 1 indicates greater target-答案概率 之后 准标识符
训练比之后 匹配 无关对照 训练.

This 是 termed quasi-identifier-associated excess 恢复.

It 是 NOT by itself 证据 的 精确 latent-memory persistence.

## Secondary 恢复 quantities

Quasi 恢复 相对于 RMU Step0:

G_Q_i = P_Quasi_i / P_RMU_i

对照 恢复 相对于 RMU Step0:

G_C_i = P_Control_i / P_RMU_i

These quantities distinguish overall post-training 恢复 来自
quasi-associated excess 恢复.

## Primary 统计 summaries

Across the 18 entity-level R_i values report:

1. Median R_i
2. Mean log(R_i)
3. Geometric 均值 R_i = exp(均值(log(R_i)))
4. Proportion 的 实体 使用 R_i > 1
5. Bootstrap 95% 置信区间 at the ENTITY level
6. Paired entity-level 比较 的 log probabilities:
   log(P_Quasi_i) versus log(P_Control_i)

The 实体, not the individual 证据 QA 记录, 是 the 统计 unit.

证据 记录 不得 be treated作为independent samples.

## 概率 metric

Primary outcome:

held-out target-答案概率

using the 相同 OpenUnlearning 概率 handler used在EXP006–EXP008.

ROUGE 和 已生成 text 是 辅助 qualitative outcomes 仅.

## Full-model reference

P_Full 是 retained作为a descriptive pre-unlearning reference.

恢复 above RMU Step0 does not necessarily imply restoration到the
original Full-model state.

## 解释 constraints

该实验 可能 support 证据 of:

- target-likelihood 恢复;
- quasi-identifier-associated excess 恢复;
- 恢复 through correlated non-name attributes.

该实验 alone 必须 NOT be described作为proof of:

- 精确 latent-memory persistence;
- semantic identity 恢复;
- 完成 reconstruction 的 the forgotten 记录;
- universal RMU 失败;
- 临床 patient-level 恢复;
- 统计 independence 的 证据 记录.

Clinical generalization requires a later patient-level 医学 experiment.

## Outcome-independent inclusion rule

All E01–E18 实体 remain在the 主要 analysis.

No 实体 will be 已排除 because:
- 恢复 是 弱;
- 恢复 是 negative;
- RMU suppression 为 relatively 弱;
- 已生成 text 是 degenerate;
- 结果 conflicts 使用 the 假设.

Any later sensitivity analysis 必须 be clearly labeled 次要 和 可能
not replace the full 18-entity 主要 analysis.

