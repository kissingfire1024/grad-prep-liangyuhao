# EXP009 Control Masked v3 Freeze

## Status

`EXP009_CONTROL_MASKED_V3_FROZEN`

This file freezes the final matched unrelated control
dataset for Experiment 009.

No recovery outcome was observed before this freeze.

## Dataset

Final file:

`data/control_masked_v3.json`

Entities: 18

Records per entity: 5

Total records: 90

Unique source indices: 90

SHA256:

`edb0db3629f21a41d4d7fb91a531546784da1c7285a291e96e0e2e04c2c99511`

## Quasi dataset

`data/quasi_identifier_masked_v3.json`

SHA256:

`c60a2720057b0574e99b3bec5f18dedaf468fac24212b949cde26d74d1c0e8a6`

## Final audit

All 90 records PASS after manual adjudication.

Automatic residual flags:

- E04 / 682: `NAME_PART:Bergstrøm`
  - MANUAL_KEEP
  - Parent surname, not target-author self-reference.

- E06 / 1083: `HARD_BIRTH`
  - MANUAL_KEEP
  - Family/background wording only; no birth date,
    birthplace, or geography bridge.

- E09 / 1682: `HARD_BIRTH`
  - MANUAL_KEEP
  - Parent/family wording only; no birth date,
    birthplace, or geography bridge.

Unresolved violations: 0

Audit SHA256:

`1cafa7a7b6748b921bcf5fb0b29f5daa5a215a50b438ccceffa7643389a2e1ba`

## Final masked token exposure

Quasi total tokens: 3604

Control total tokens: 3498

Control / Quasi:

`0.970588235`

Global relative difference:

`0.029411765`

Entities with relative difference > 0.25:

`E06, E13, E17`

These residual entity-level exposure imbalances are
retained intentionally.

No further token-based data modification is permitted.

They must be reported and handled through sensitivity
analysis rather than additional dataset tuning.

Token audit SHA256:

`80473b353e26f184aaecd6d8436da55d2cfb04e05f361ac66cc49fac0657bf91`

## Methodological priority

1. Hard-exclusion safety
2. Evidence-category preservation
3. Token-exposure matching

Token matching was not allowed to override semantic
category preservation.

## Provenance

Control v3 was constructed from the previously audited
Control v2.

81 previously audited records were preserved unchanged.

9 records were replaced using category-preserving,
pre-outcome replacements.

The 9 new records were independently identity-masked
and audited before merging.

No recovery outcome was used to select, modify, or
optimize Control v3.

## Freeze rule

DO NOT MODIFY `control_masked_v3.json`.

Any future change requires a new version and a new
documented protocol.

Recovery experiments must use this frozen file exactly.
