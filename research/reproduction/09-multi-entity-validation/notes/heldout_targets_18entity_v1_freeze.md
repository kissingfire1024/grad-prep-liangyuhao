# EXP009 — 18-Entity Heldout Target Set 冻结

状态: EXP009_HELDOUT_TARGETS_18ENTITY_V1_FROZEN

File:
`/home/research/research/reproduction/09-multi-entity-validation/data/heldout_targets_18entity_v1.json`

SHA256:
`1236a72d8ffb9ac5bb90fd04551ae43b57bc5ae9d2f4e679bc2ad61359195f6a`

Source:
- 数据集: locuslab/TOFU
- Split: forget10
- Total source 记录: 400

Validation cohort:
- E01–E18
- 18 independent 作者 实体
- one pre-specified block-first 身份目标 per 实体
- 源索引: [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340]

Discovery 实体 已排除 来自 validation:
- Basil Mahfouz Al-Kuwaiti
- Nikolai Abilov

选择 rule:
- first 记录 的 each 的 the first 18 twenty-record 实体 blocks
- rule fixed 之前 model 恢复 outcomes 是 observed

说明:
- E04 asks用于both 作者身份 和 出生地 和 是 retained unchanged.
- E10 uses "name" rather比"full name" 和 是 retained unchanged.
- No 目标 为 replaced based在anticipated model performance.
- This file 不得 be 已修改 之后 freezing.
- Any future change requires a new versioned 目标 file.
