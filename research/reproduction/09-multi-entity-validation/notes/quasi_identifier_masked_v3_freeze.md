# EXP009 准标识符 Masked 数据集 V3 冻结

## 状态

EXP009_QUASI_IDENTIFIER_MASKED_V3_FROZEN

## 已冻结 artifact

Path:

`/home/research/research/reproduction/09-multi-entity-validation/data/quasi_identifier_masked_v3.json`

SHA256:

`c60a2720057b0574e99b3bec5f18dedaf468fac24212b949cde26d74d1c0e8a6`

记录: 90

Entities: 18

证据 记录 per 实体: 5

## Validation cohort

E01–E18 来自 TOFU forget10.

The two discovery 实体 used在EXP006–EXP008
(Basil Mahfouz Al-Kuwaiti 和 Nikolai Abilov)
are 已排除 来自 the EXP009 validation cohort.

## Construction constraints

The dataset 为 constructed 之前 EXP009 恢复 outcomes.

The following constraints 为 applied:

- heldout 目标 QA 已排除 来自 攻击 证据;
- direct target-author full names removed;
- verified target-author short-name references removed;
- direct birth/出生地 bridge 证据 已排除;
- book-title anchor 证据 已排除;
- no synthetic stable 实体 identifier introduced;
- semantic 准标识符 attributes preserved;
- 显式 E17 地理 identity label removed;
- non-target identities 为 preserved when required用于semantic fidelity.

## Important collision decision

For E14, the 目标 作者 是 Kalkidan Abera.

The 证据 记录 also 包含 the 不同的 person:

`Fikadu Abera`

This name 为 intentionally preserved因为it refers to
the 目标 作者's father rather比the 目标 作者.

## Final 审计

Structure:

- 90 记录
- 90 unique 实体/source-index pairs
- 18 实体
- exactly 5 证据 记录 per 实体

Final identity/artifact 审计:

- full-name leaks: 0
- known short-name leaks: 0
- E17 geo-label leaks: 0
- known masking text artifacts: 0
- E14 collision protection: 通过

Final machine-audit status:

`EXP009_MASKED_V3_FINAL_MACHINE_AUDIT_PASS`

## Version history

V1:
Initial global name-part masking.
Rejected 之前 训练因为global surname/name-part
replacement produced linguistic artifacts 和 已修改 a
non-target person's surname.

V2:
Context-aware identity masking.
Passed automated identity checks,但manual pre-training
review found two E17 grammatical artifacts.

V3:
Only E17 源索引 321 和 324 为 grammatically
normalized 相对于 V2.

No 恢复 results 为 used到make these corrections.

## 冻结 rule

This file 是 now 不可修改用于EXP009.

Do not modify:

`quasi_identifier_masked_v3.json`

If a substantive issue 是 discovered later, create a new
version 和 preserve V3 unchanged.

冻结 timestamp:

2026-10-03T20:12:48.876786

