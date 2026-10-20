# Experiment 009 — 恢复 训练 协议 v1

## 状态

`EXP009_RECOVERY_TRAINING_PROTOCOL_V1_FROZEN`

本协议 是 frozen 之前 observing any 正式
Experiment 009 恢复 outcome.

## Research 比较

Two 恢复 conditions 是 compared:

1. 准标识符 相关证据
2. Matched 无关对照 证据

Both conditions start independently 来自 the 精确 相同
RMU Step-0 checkpoint.

## Base checkpoint

`/home/research/open-unlearning/saves/unlearn/tofu_Llama-3.2-1B-Instruct_forget10_RMU_exp009`

The Quasi trajectory 和 对照 trajectory MUST each
load this checkpoint independently.

Neither trajectory 可能 continue 来自 the 1-step
engineering probe.

## 已冻结 datasets

Quasi:

`data/quasi_identifier_masked_v3.json`

SHA256:

`c60a2720057b0574e99b3bec5f18dedaf468fac24212b949cde26d74d1c0e8a6`

对照:

`data/control_masked_v3.json`

SHA256:

`edb0db3629f21a41d4d7fb91a531546784da1c7285a291e96e0e2e04c2c99511`

Heldout targets:

`data/heldout_targets_18entity_v1.json`

SHA256:

`1236a72d8ffb9ac5bb90fd04551ae43b57bc5ae9d2f4e679bc2ad61359195f6a`

## 正式 恢复 训练 配置

Trainer:

`finetune`

模型:

`Llama-3.2-1B-Instruct`

Attention:

`sdpa`

Per-device train batch size:

`1`

Per-device eval batch size:

`1`

Gradient accumulation steps:

`4`

Effective examples per 优化器步:

`4`

Learning rate:

`1e-5`

Weight decay:

`0.01`

Gradient checkpointing:

`true`

Logging steps:

`1`

正式 恢复 优化器步数:

`20`

评估 during 训练:

`disabled`

Save strategy during ordinary trainer execution:

`no`

Random 随机种子:

Use the 相同 OpenUnlearning/default 随机种子用于both
conditions. No condition-specific 随机种子 changes are
permitted.

## 攻击 symmetry

The following MUST be identical 之间 Quasi and
对照:

- RMU starting checkpoint
- model architecture
- tokenizer
- trainer
- 学习率
- optimizer 配置
- batch size
- 梯度累积
- 梯度检查点
- 权重衰减
- optimizer-step count
- 随机种子
- heldout evaluator
- 评估 metrics

The 仅 intended experimental difference 是 the
训练 证据 dataset.

## 正式 endpoint

The 主要 正式 恢复 endpoint 是 optimizer
step 20.

No intermediate heldout 恢复 result will be used
to change the 训练 duration 或 hyperparameters.

## Primary 统计 unit

实体.

There 是 18 independent validation 实体:

E01 through E18.

QA examples 是 not treated作为independent
统计 units.

## 主要指标

For each 实体 i:

R_i = P_Quasi_i / P_Control_i

where P 是 heldout target-答案概率 之后
the 正式 20-step 恢复 训练.

## Secondary 恢复 quantities

G_Q_i = P_Quasi_i / P_RMU_i

G_C_i = P_Control_i / P_RMU_i

## Primary summaries

- 中位数 R_i
- 均值 log(R_i)
- 几何均值 R_i
- proportion 的 实体 使用 R_i > 1
- entity-level Bootstrap 95% 置信区间
- paired entity-level log-probability 比较

## Auxiliary metrics

ROUGE 和 已生成 text 是 辅助 仅.

Target-答案概率 是 the 主要 恢复
measurement.

## 解释 boundary

A result 使用 R_i > 1 支持 greater target-answer
恢复 following 准标识符 证据 than
following the 匹配 无关对照用于that
实体.

Aggregate excess 恢复 可能 be described as
quasi-identifier-associated 恢复.

It MUST NOT by itself be described作为proof of:

- 精确 latent-memory persistence
- semantic identity 恢复
- universal RMU 失败
- 临床 generalization
- patient-level 临床 恢复

## Known exposure imbalance

Final global token exposure:

Quasi = 3604 tokens
对照 = 3498 tokens

对照 / Quasi = 0.970588

Residual entity-level token imbalance > 25%:

E06
E13
E17

These 实体 remain在the 主要 analysis.

No post-outcome data modification 是 permitted.

Exposure imbalance 可能 later be addressed through
pre-specified sensitivity analysis.

## Engineering probe

A Quasi 1-step engineering probe 已完成
successfully 之前 正式 训练.

Probe 训练 损失:

9.877901077270508

The probe 为 used 仅到establish pipeline
feasibility.

No heldout 恢复 评估 为 performed.

The probe checkpoint 是 NOT part 的 the 正式
trajectory.

## 冻结 rule

After 本协议 是 frozen:

- do not alter the datasets
- do not alter 训练 hyperparameters based在outcomes
- do not change the 20-step endpoint
- do not 排除 实体 based在恢复 results
- do not replace E06, E13, 或 E17
- do not continue 训练因为an effect appears 弱
- do not stop early因为an effect appears 强

Any deviation requires a separately versioned
protocol 和 必须 be labeled 探索性.
