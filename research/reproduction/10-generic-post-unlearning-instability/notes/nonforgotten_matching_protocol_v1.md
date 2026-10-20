# Exp010-A — Forgotten / Non-Forgotten Target Matching 协议 v1

## 目标

Match each 的 the 18 frozen Exp009 forgotten 身份目标到exactly
one 符合条件 retained/未遗忘 身份目标.

Matching 必须 be 已完成 和 frozen 之前 any RMU, Quasi, 或 对照
outcome 是 evaluated在保留目标.

## 输入

遗忘目标:

Experiment 009 frozen:
heldout_targets_18entity_v1.json

未遗忘 候选 pool:

Exp010:
nonforgotten_identity_candidate_audit_v1.json

Only 记录 使用:

manual_eligibility == ELIGIBLE

可能 participate.

Expected 符合条件 pool:

131 targets 来自 131 不同的 retain90 profiles.

## Statistical Unit

实体.

Final matching:

18 forgotten 实体
<- one-to-one ->
18 不同的 retained 实体.

A 保留目标 可能 be used at most once.

## Text Features

Features 是 extracted 来自 QUESTION TEXT ONLY.

For every 问题 define:

### GEO

1 if the 问题 包含 an 显式 地理 cue
(city/country/place expression),
otherwise 0.

### DATE_EXACT

1 if an 显式 month/day 或 numeric month/day-style date 是 present,
otherwise 0.

Examples:

- July 28, 1942
- 05/11/1991
- 15th 的 April, 1992

### YEAR_ONLY

1 if a four-digit 出生年份 是 present但DATE_EXACT == 0,
otherwise 0.

### GENDER

1 if 显式 gender wording such作为male/female 是 present,
otherwise 0.

### LGBTQ

1 if 显式 LGBTQ/LGBT/LGBTQ+ wording 是 present,
otherwise 0.

### GENRE

1 if the 问题 explicitly identifies a literary/professional 体裁
or specialization,
otherwise 0.

Examples 纳入 leadership, geology, cyberpunk, dystopian,
historical romance, mythology, 医学, crime, etc.

### FICTITIOUS

1 if 显式 fictitious/fictional wording occurs,
otherwise 0.

### TOKEN_LENGTH

Number 的 tokenizer tokens在the 问题 using the 相同
Llama-3.2-1B-Instruct tokenizer used by 该实验.

## Matching Cost

For 遗忘目标 i 和 retained 候选 j:

cost(i,j) =

    4 * abs(GEO_i       - GEO_j)
  + 4 * abs(DATE_EXACT_i- DATE_EXACT_j)
  + 2 * abs(YEAR_ONLY_i - YEAR_ONLY_j)
  + 1 * abs(GENDER_i    - GENDER_j)
  + 1 * abs(LGBTQ_i     - LGBTQ_j)
  + 1 * abs(GENRE_i     - GENRE_j)
  + 1 * abs(FICTITIOUS_i- FICTITIOUS_j)
  + TOKEN_COST

where:

TOKEN_COST =
    abs(tokens_i - tokens_j)
    / max(tokens_i, tokens_j)

The two highest-priority structural characteristics 是 therefore:

1. geography structure;
2. 精确 birth-date structure.

Token length 是 a 次要 tie/refinement term 和 不得 dominate
semantic task structure.

## Optimization

Use 确定性 minimum-total-cost one-to-one bipartite assignment
跨 全部 18 遗忘目标 和 全部 131 符合条件 保留目标.

Use scipy.optimize.linear_sum_assignment.

Because the 候选 side has 131 targets, the assignment selects
18 不同的 保留目标 minimizing total 匹配代价.

## Deterministic Tie Breaking

Before optimization:

1. 遗忘目标 sorted by target_id E01...E18;
2. retained candidates sorted by profile_id, then source_index.

Add 仅 a numerically negligible 确定性 tie-breaking term:

    1e-9 * candidate_rank

to each pair cost.

This term 不得 materially change the substantive 匹配代价.

## Outcome-Blinding

The matching script MUST NOT read:

- RMU 评估 results;
- Quasi 评估 results;
- 对照 评估 results;
- target-answer probabilities;
- ROUGE results;
- 已生成 model outputs.

Matching 是 based exclusively在frozen source text 和 tokenizer
properties.

## Validation Before 冻结

Before final 目标 freezing, report:

- 全部 18 匹配 pairs;
- component features用于both sides;
- 问题 token 长度s;
- substantive pair cost;
- total 匹配代价;
- number 的 重复使用 retained profiles (必须 equal 0).

No model outcome 可能 be displayed.

## Primary 分析 Consequence

After matching 是 frozen, the 相同 保留目标 set will be evaluated
on:

1. RMU Step0;
2. Quasi 20-step;
3. 对照 20-step.

The retained group will then be 与……相比 the already frozen
forgotten group.

No 保留目标 可能 be replaced based在评估 results.

## 解释

目的 的 matching 是到reduce task-form differences 之间
forgotten 和 retained 身份检索.

It does not make the two groups identical 和 不能证明 因果
exchangeability.

Residual matching differences 必须 be reported.

## 状态

EXP010_NONFORGOTTEN_MATCHING_PROTOCOL_V1_FROZEN
