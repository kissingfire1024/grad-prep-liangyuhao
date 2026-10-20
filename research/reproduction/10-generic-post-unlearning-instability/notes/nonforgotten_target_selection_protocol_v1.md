# Exp010-A — Matched Non-Forgotten Target 选择 协议 v1

## 目的

Construct 18 retained/未遗忘 身份目标用于比较 使用
the 18 forgotten 身份目标 frozen在Experiment 009.

目标 是到distinguish:

1. generic post-update 概率 drift; 来自
2. forgotten-knowledge-specific 恢复.

## Source

Targets 必须 come exclusively 来自 the 官方 TOFU retain90 split,
using:

data/retain90_profile_manifest_v1.json

来自 sealed Experiment 009作为a READ-ONLY source.

## Statistical Unit

One retained 作者 档案 = one independent 实体.

Exactly:

- 18 retained 实体;
- 1 目标 per 实体;
- 18 total targets.

No retained 作者 档案 可能 contribute more比one 目标.

## Required Target Type

The 目标 必须 be an identity-retrieval 问题.

The 问题 必须 ask 模型到output the 作者's identity/name
来自 descriptive attributes.

Preferred form:

descriptive attributes -> 作者 name

Examples 的 acceptable cues 纳入:

- 出生地;
- birth date/year;
- gender;
- 体裁;
- LGBTQ+ identity;
- nationality/background;
- combinations 的 these attributes.

The 答案 必须 explicitly contain the 作者's name.

## Exclusions

Do NOT select questions whose 主要 requested 答案 is:

- birth date;
- 出生地;
- 体裁;
- award;
- parent information;
- 书名;
- character;
- theme;
- career information;
- yes/no information;
- other non-identity facts.

A 问题 merely containing the 作者's name 是 not an 身份目标.

For example:

"What 是 X's 出生日期?"

is NOT 符合条件.

## Matching Principle

The 18 保留目标 应当 resemble the Exp009 遗忘目标 in
task form:

attributes -> identity/name.

Matching priority:

1. identity-retrieval task type;
2. birth/地理 cue structure;
3. additional demographic/体裁 cues;
4. 问题 length/token exposure.

Semantic/task matching takes priority over 精确 token-length matching.

## 选择 流程

Before any Exp010 model 评估:

1. mechanically scan 全部 180 retain90 profiles;
2. identify every 候选 identity-retrieval 问题;
3. 记录 全部 candidates在a 候选 清单;
4. do not inspect RMU/Quasi/对照 probabilities而selecting;
5. choose 18 retained profiles using 仅 source-text characteristics;
6. 冻结 the 已选择 目标 set;
7. 仅 then evaluate model checkpoints.

## Independence

The 已选择 retained profiles 必须:

- be 不同的 来自 each other;
- belong到retain90;
- not be one 的 the forget10 validation 实体;
- not be 已选择 using model outcome information.

## Primary Exp010-A 比较

For each group:

遗忘目标:
    RMU -> Quasi
    RMU -> 对照

Non-遗忘目标:
    RMU -> Quasi
    RMU -> 对照

Primary 机制 问题:

Are post-update 概率 changes disproportionately larger for
遗忘目标 than用于匹配 保留目标?

## 解释

If forgotten 和 保留目标 change similarly:

    证据 favors generic model/capability/calibration drift.

If 遗忘目标 recover substantially more:

    证据 支持 forgotten-specific 抑制反转.

If both occur:

    证据 支持 a mixed 机制.

概率 changes alone do not prove 精确 latent-memory persistence.

## Outcome-Blinding Rule

No RMU, Quasi, 或 对照 outcome在候选 保留目标 可能 be
observed 之前 目标 选择 和 freezing 是 完成.

## 状态

EXP010_NONFORGOTTEN_TARGET_SELECTION_PROTOCOL_V1_FROZEN
