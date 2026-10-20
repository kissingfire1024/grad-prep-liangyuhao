# EXP009 对照 Masked v3 冻结

## 状态

`EXP009_CONTROL_MASKED_V3_FROZEN`

This file freezes the final 匹配 无关对照
dataset用于Experiment 009.

No 恢复 outcome 为 observed 之前 this 冻结.

## 数据集

Final file:

`data/control_masked_v3.json`

Entities: 18

记录 per 实体: 5

Total 记录: 90

Unique 源索引: 90

SHA256:

`edb0db3629f21a41d4d7fb91a531546784da1c7285a291e96e0e2e04c2c99511`

## Quasi dataset

`data/quasi_identifier_masked_v3.json`

SHA256:

`c60a2720057b0574e99b3bec5f18dedaf468fac24212b949cde26d74d1c0e8a6`

## Final 审计

All 90 记录 通过 之后 manual adjudication.

Automatic residual flags:

- E04 / 682: `NAME_PART:Bergstrøm`
  - MANUAL_KEEP
  - Parent surname, not target-author self-reference.

- E06 / 1083: `HARD_BIRTH`
  - MANUAL_KEEP
  - Family/background wording 仅; no birth date,
    出生地, 或 geography bridge.

- E09 / 1682: `HARD_BIRTH`
  - MANUAL_KEEP
  - Parent/family wording 仅; no birth date,
    出生地, 或 geography bridge.

Unresolved violations: 0

审计 SHA256:

`1cafa7a7b6748b921bcf5fb0b29f5daa5a215a50b438ccceffa7643389a2e1ba`

## Final masked token exposure

Quasi total tokens: 3604

对照 total tokens: 3498

对照 / Quasi:

`0.970588235`

Global relative difference:

`0.029411765`

Entities 使用 relative difference > 0.25:

`E06, E13, E17`

These residual entity-level exposure imbalances are
retained intentionally.

No further token-based data modification 是 permitted.

They 必须 be reported 和 handled through sensitivity
analysis rather比additional dataset tuning.

Token 审计 SHA256:

`80473b353e26f184aaecd6d8436da55d2cfb04e05f361ac66cc49fac0657bf91`

## Methodological priority

1. Hard-exclusion safety
2. Evidence-category preservation
3. Token-exposure matching

Token matching 为 not allowed到override semantic
category preservation.

## Provenance

对照 v3 为 constructed 来自 the previously audited
对照 v2.

81 previously audited 记录 为 preserved unchanged.

9 记录 为 replaced using category-preserving,
pre-outcome replacements.

The 9 new 记录 为 independently identity-masked
and audited 之前 merging.

No 恢复 outcome 为 used到select, modify, or
optimize 对照 v3.

## 冻结 rule

DO NOT MODIFY `control_masked_v3.json`.

Any future change requires a new version 和 a new
documented protocol.

恢复 experiments 必须 use this frozen file exactly.
