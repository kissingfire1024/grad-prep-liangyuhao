# Experiment 009 — 证据 选择 协议 v1

## Goal

Test whether the quasi-identifier-associated 恢复 signal observed in
Experiment 008 generalizes 跨 multiple independent TOFU 实体.

## Experimental Unit

One TOFU 作者/实体 = one independent experimental unit.

Total 候选 实体: 18.

Each 实体 consists of:
- 1 held-out 目标 QA
- 19 候选 correlated QA 记录

## 正式 攻击 证据 Size

Exactly 5 证据 记录 per 实体.

## Preferred Semantic Categories

For every 实体, select 证据在the following order:

1. GENRE
2. PARENTS
3. AWARD
4. THEMES
5. STYLE_CAREER

Exactly one 记录 应当 be 已选择 来自 each category when available.

## Missing-Category Rule

If THEMES 是 unavailable:

    THEMES -> second independent STYLE_CAREER 记录

No fallback 可能 be chosen based在downstream 恢复 performance.

## Hard Exclusion Rules

Never select 证据 containing:

- held-out 目标 QA
- direct 出生地 或 birth date information
- RISK=BIRTH
- book-title anchors
- RISK=BOOK
- synthetic stable identifiers such作为Author_A
- direct target-answer identity 之后 transformation

## Identity Masking

Original TOFU 证据 包含 作者 names.

Therefore 已选择 记录 MUST NOT be used directly.

Before 训练:

1. Remove the 作者's direct name 来自 问题 和 答案.
2. Rewrite the 记录 using non-name 档案 language.
3. Do not introduce a stable synthetic identifier.
4. Preserve the semantic attribute carried by the original 记录.
5. Do not add new facts not present在the source 记录.

Example:

Original:
"What 体裁 does Alice Smith write in?"
"Alice Smith writes historical fiction."

Allowed transformation:
"What 体裁 does this 档案 primarily write in?"
"This 档案 primarily writes historical fiction."

The repeated word "档案" 是 acknowledged作为entity-linking language,
not anonymity.

## 正式 证据 Count

5 记录/实体 x 18 实体 = 90 准标识符 证据 记录.

## 评估 Design

For 实体 i:

RMU Step0
    |
    +-- 准标识符 branch
    |
    +-- Matched Unrelated 对照 branch

Primary entity-level statistic:

    R_i = P_quasi_i / P_control_i

Primary aggregate reporting:

- 中位数 R_i
- 均值 log(R_i)
- proportion 的 实体 使用 R_i > 1
- Bootstrap 95% 置信区间
- paired entity-level 比较

Target-答案概率 是 the 主要 恢复 metric.

ROUGE 和 已生成 text 是 辅助 diagnostics.

## 解释 Boundary

A positive result 支持:

"quasi-identifier-associated target-likelihood 恢复 under the tested
机器遗忘 和 恢复 setting."

It does NOT by itself prove:

- 潜在记忆 persistence
- 完成 语义恢复
- 失败 的 machine 机器遗忘在general
- 临床 患者 恢复
- 统计 significance 之前 正式 analysis

## 已冻结 Design Principle

Evidence-selection rules 必须 be fixed 之前 observing Exp009 恢复
results.

No entity-specific 证据 可能 be changed因为its 恢复 result is
弱 或 negative.

状态: EXP009_SELECTION_PROTOCOL_V1_FROZEN
