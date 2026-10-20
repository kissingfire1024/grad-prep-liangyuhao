# EXP009 — Matched Unrelated 对照 协议 v1

状态: EXP009_MATCHED_CONTROL_PROTOCOL_V1_FROZEN

## 目的

Construct a 匹配 无关对照 branch用于the 18-entity EXP009
准标识符 恢复 experiment.

The 对照 必须 be frozen 之前 observing any EXP009 恢复 outcome.

## Source pool

对照 证据 will be drawn exclusively 来自 the 官方 TOFU
retain90 split.

retain90 包含:
- 3600 QA 记录
- 180 apparent author-profile blocks
- 20 QA 记录 per block

No forget10 validation 实体 will provide 对照 证据.

## Experimental structure

For every forgotten validation 实体 E01–E18:

Quasi branch:
- exactly 5 frozen 准标识符 QA 记录

对照 branch:
- exactly 5 QA 记录
- 来自 one 无关 retain90 作者 block

Therefore:
- 18 quasi profiles
- 18 对照 profiles
- 5 记录/档案
- 90 记录/branch

A retain90 作者 block 可能 be assigned到at most one validation 实体.

## Identity masking

对照 证据 必须 be identity-masked 之前 训练.

Direct references到the retain90 作者's identity 必须 be removed or
rewritten using neutral 档案 language.

The 对照 branch 不得 systematically 保留 显式 作者 names
while the quasi branch 是 identity-masked.

Masking 不得 introduce:
- synthetic stable aliases;
- new facts;
- 遗忘目标 identities.

## Hard exclusions

候选 对照 记录 必须 排除 证据 whose principal content is:

1. 作者 full-name identification;
2. date/place 的 birth 或 other direct birth/geography identification;
3. 书名s 或 title-based proxy identifiers;
4. synthetic identifiers;
5. any E01–E18 目标 identity;
6. any direct bridge到an E01–E18 held-out 目标.

记录 containing unavoidable direct author-name leakage 之后 masking
必须 also be 已排除.

## Preferred semantic 证据

Where available, safe 对照 证据 应当 represent 档案 attributes
analogous到the quasi branch, including:

- 体裁;
- parents/background;
- awards;
- themes;
- writing style/career.

If an 精确 category 是 unavailable, another safe style/career attribute
可能 be used.

## Matching objective

Matching 是 outcome-independent.

恢复 评估 results 必须 never be used到select 对照 记录.

For each validation 实体, 候选 5-record 对照 sets will be
compared against that 实体's frozen 5-record quasi set using tokenizer
exposure.

Primary matching variables:
- number 的 记录;
- total 问题 + 答案 token count.

Each branch 必须 contain exactly five 记录 per 实体.

The algorithm 应当 minimize token-exposure difference而satisfying
全部 safety 和 independence constraints.

Global token exposure 应当 be reported as:

T_control / T_quasi

where frozen quasi exposure is:

T_quasi = 3604 tokens

Per-entity token exposure differences 必须 also be reported.

## Independence rule

Each validation 实体 receives 证据 来自 a 不同的 retain90 作者
档案.

No retain90 档案 可能 be 重复使用 跨 multiple validation 实体.

The 统计 unit remains the forgotten validation 实体 E01–E18,
not the 对照 作者 和 not the individual QA 记录.

## 训练 matching

Later Quasi 和 对照 恢复 branches 必须 use identical:

- RMU Step0 starting checkpoint;
- optimizer 配置;
- 学习率;
- batch size;
- 梯度累积;
- number 的 optimization steps;
- random 随机种子;
- 评估 procedure.

Only the 恢复 证据 differs.

## Primary 比较

For 实体 i:

R_i = P_Quasi_i / P_Control_i

对照 训练 measures generic retraining / parameter-drift 恢复.

Quasi-over-Control measures excess target-likelihood 恢复 associated
使用 correlated 准标识符 证据.

## 解释 constraint

A value R_i > 1 是 not, by itself, proof 的 精确 latent-memory
persistence.

It 是 证据 仅 的 更高 held-out target-answer likelihood following
the 准标识符 branch比the 匹配 unrelated-control branch.

## Versioning

本协议 是 frozen 之前 对照 选择 和 之前 EXP009
Quasi/对照 恢复 训练.

Do not modify this file 之后 freezing.

Any methodological change requires a new protocol version.
