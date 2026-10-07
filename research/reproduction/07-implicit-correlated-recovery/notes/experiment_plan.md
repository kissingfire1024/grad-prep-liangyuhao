# Experiment 007 — Implicit Correlated 恢复

## 研究问题

After RMU 机器遗忘, can held-out forgotten information become recoverable
之后 训练在相关证据 that does NOT directly expose the
held-out 目标答案?

## Starting Point

Experiment 006 showed:

- 无关 SFT causes substantial 通用恢复;
- 同实体 correlated SFT produces additional target-答案概率
  恢复;
- correlated/对照 概率 比率:
  - B0: 4.907x
  - N20: 1.323x
  - Mean: 3.285x

However, Experiment 006 explicitly exposed 实体 identities在correlated
训练 记录.

Experiment 007 removes this direct 答案 leakage.

## Core Constraint

The 训练 证据 不得 directly contain the held-out 目标答案
identity string.

For B0:
"Basil Mahfouz Al-Kuwaiti" 不得 appear在攻击 训练 text.

For N20:
"Nikolai Abilov" 不得 appear在攻击 训练 text.

The original held-out 目标 QA pairs 必须 also remain 已排除.

## Experimental Principle

We 必须 preserve useful cross-record 相关性而preventing direct
identity-answer leakage.

Before any 训练:

1. construct 候选 implicit-correlated 记录;
2. 审计 them用于target-answer leakage;
3. inspect them manually;
4. 冻结 the dataset;
5. 仅 then run the 攻击.

## 状态

DESIGN PHASE
