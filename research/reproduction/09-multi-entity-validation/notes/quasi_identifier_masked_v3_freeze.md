# EXP009 Quasi-Identifier Masked Dataset V3 Freeze

## Status

EXP009_QUASI_IDENTIFIER_MASKED_V3_FROZEN

## Frozen artifact

Path:

`/home/research/research/reproduction/09-multi-entity-validation/data/quasi_identifier_masked_v3.json`

SHA256:

`c60a2720057b0574e99b3bec5f18dedaf468fac24212b949cde26d74d1c0e8a6`

Records: 90

Entities: 18

Evidence records per entity: 5

## Validation cohort

E01–E18 from TOFU forget10.

The two discovery entities used in EXP006–EXP008
(Basil Mahfouz Al-Kuwaiti and Nikolai Abilov)
are excluded from the EXP009 validation cohort.

## Construction constraints

The dataset was constructed before EXP009 recovery outcomes.

The following constraints were applied:

- heldout target QA excluded from attack evidence;
- direct target-author full names removed;
- verified target-author short-name references removed;
- direct birth/birthplace bridge evidence excluded;
- book-title anchor evidence excluded;
- no synthetic stable entity identifier introduced;
- semantic quasi-identifier attributes preserved;
- explicit E17 geographic identity label removed;
- non-target identities were preserved when required for semantic fidelity.

## Important collision decision

For E14, the target author is Kalkidan Abera.

The evidence record also contains the distinct person:

`Fikadu Abera`

This name was intentionally preserved because it refers to
the target author's father rather than the target author.

## Final audit

Structure:

- 90 records
- 90 unique entity/source-index pairs
- 18 entities
- exactly 5 evidence records per entity

Final identity/artifact audit:

- full-name leaks: 0
- known short-name leaks: 0
- E17 geo-label leaks: 0
- known masking text artifacts: 0
- E14 collision protection: PASS

Final machine-audit status:

`EXP009_MASKED_V3_FINAL_MACHINE_AUDIT_PASS`

## Version history

V1:
Initial global name-part masking.
Rejected before training because global surname/name-part
replacement produced linguistic artifacts and modified a
non-target person's surname.

V2:
Context-aware identity masking.
Passed automated identity checks, but manual pre-training
review found two E17 grammatical artifacts.

V3:
Only E17 source indices 321 and 324 were grammatically
normalized relative to V2.

No recovery results were used to make these corrections.

## Freeze rule

This file is now immutable for EXP009.

Do not modify:

`quasi_identifier_masked_v3.json`

If a substantive issue is discovered later, create a new
version and preserve V3 unchanged.

Freeze timestamp:

2026-10-03T20:12:48.876786

