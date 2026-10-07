# EXP009 — 18-Entity Heldout Target Set Freeze

Status: EXP009_HELDOUT_TARGETS_18ENTITY_V1_FROZEN

File:
`/home/research/research/reproduction/09-multi-entity-validation/data/heldout_targets_18entity_v1.json`

SHA256:
`1236a72d8ffb9ac5bb90fd04551ae43b57bc5ae9d2f4e679bc2ad61359195f6a`

Source:
- Dataset: locuslab/TOFU
- Split: forget10
- Total source records: 400

Validation cohort:
- E01–E18
- 18 independent author entities
- one pre-specified block-first identity target per entity
- source indices: [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340]

Discovery entities excluded from validation:
- Basil Mahfouz Al-Kuwaiti
- Nikolai Abilov

Selection rule:
- first record of each of the first 18 twenty-record entity blocks
- rule fixed before model recovery outcomes are observed

Notes:
- E04 asks for both author identity and birthplace and is retained unchanged.
- E10 uses "name" rather than "full name" and is retained unchanged.
- No target was replaced based on anticipated model performance.
- This file must not be modified after freezing.
- Any future change requires a new versioned target file.
