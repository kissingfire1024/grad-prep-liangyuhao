# EXP009 证据 选择 协议 v1 — Pre-Outcome Clarification

## 状态

PRE-OUTCOME DATA-CONSTRUCTION CLARIFICATION

This clarification 为 已创建 之前 any EXP009 恢复 训练,
恢复 评估, 或 entity-level 恢复 result 为 observed.

It does not modify any result-dependent decision.

## Reason

During source-manifest auditing, some preferred category 记录 were
found到violate the frozen hard-exclusion rules.

The original protocol explicitly defined a fallback用于unavailable
THEMES 记录,但did not define what到do when another preferred
category (e.g. PARENTS) has no safe 候选 之后 hard exclusions.

A 确定性 rule 是因此required 之前 constructing the
corrected 清单.

## Clarification Rule

For each 实体:

1. Apply 全部 hard exclusions 之前 category 选择.

2. Preserve one safe 记录 来自 each preferred category whenever
   available:

   GENRE
   PARENTS
   AWARD
   THEMES
   STYLE_CAREER

3. If THEMES has no safe 候选, 保留 the original rule:
   use a second independent STYLE_CAREER 记录.

4. If any OTHER preferred category has no safe 候选 之后 hard
   exclusions, do NOT substitute an 无关 semantic category merely
  到fill the slot.

5. Instead, select an additional safe STYLE_CAREER 记录 that:
   - 包含 no held-out 目标答案,
   - 包含 no birth/date/location bridge,
   - 包含 no specific book-title anchor,
   - 包含 no synthetic stable identifier,
   - 是 semantically independent 来自 the already 已选择
     STYLE_CAREER 证据作为far作为the source pool permits.

6. Record the slot explicitly as:

   <MISSING_CATEGORY>_FALLBACK_STYLE

   Example:
   PARENTS_FALLBACK_STYLE

7. Exactly five 证据 记录 per 实体 是 still required.

8. No replacement 可能 be 已选择 using 恢复 outcomes.

## 解释

Fallback 记录 preserve evidence-count balance但do not imply 精确
semantic-category balance用于every 实体.

Category composition 必须因此be reported作为a dataset
construction characteristic 和 not treated作为perfectly 匹配
跨 实体.

## EXP009 Timing Guarantee

At the time 的 this clarification:

- no EXP009 恢复 model has been trained;
- no EXP009 恢复 比率 has been observed;
- no 实体 has been 已选择 或 已排除 based在恢复 outcome.

