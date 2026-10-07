# Experiment 010 — Generic Post-Unlearning Instability

## 动机

Experiment 009 found substantial 机器遗忘后 target-probability 恢复
under both Quasi 和 无关 对照 SFT.

已冻结 Exp009 aggregate results:

- Quasi / RMU = 9.41236406387773x
- 对照 / RMU = 9.047124522386598x
- Quasi / 对照 = 1.0403707874902537x

The previously observed Exp008 准标识符 excess-recovery signal was
not stably reproduced 跨 the 18-entity Exp009 validation cohort.

Therefore, the next 问题 是 not whether quasi-identifiers can again be
made到produce a large 恢复 比率.

The next 问题 is:

> Why does 无关 机器遗忘后 fine-tuning substantially 增加
> forgotten-目标概率 之后 RMU?

## Primary Mechanistic Alternatives

### H1 — Generic model / capability drift

Post-unlearning SFT broadly changes model probabilities 或 restores general
answering capability.

Prediction:

遗忘目标 和 comparable non-遗忘目标 应当 both show
substantial 概率 changes.

### H2 — Forgotten-knowledge-specific 抑制反转

RMU suppresses access到previously learned forgotten information, and
ordinary subsequent updates partially reverse that suppression.

Prediction:

遗忘目标 应当 exhibit 更强 relative 恢复比comparable
non-遗忘目标.

### H3 — Mixed 机制

Both generic drift 和 forgotten-specific 恢复 contribute.

## Exp010-A

No new 训练.

Reuse existing checkpoints 只读:

1. RMU forget10 Step0
2. Exp009 Quasi 20-step
3. Exp009 对照 20-step

Evaluate:

A. the existing 18 forgotten heldout 身份目标;
B. a newly constructed 匹配 set 的 未遗忘 身份目标.

主要分析:

Compare post-update 概率 shifts 之间 forgotten 和 未遗忘
targets.

目的 是 机制 discrimination, not optimization 的 恢复.

## 解释 Boundary

概率 恢复 alone 是 并非证明 的 精确 latent-memory persistence.

A forgotten-specific excess shift would support a suppression-reversal
interpretation,但would still require representation-level 或 additional
mechanistic 证据.

A similar shift在forgotten 和 non-遗忘目标 would favor a generic
post-update drift explanation.

## 状态

EXP010_RESEARCH_QUESTION_V1_FROZEN
