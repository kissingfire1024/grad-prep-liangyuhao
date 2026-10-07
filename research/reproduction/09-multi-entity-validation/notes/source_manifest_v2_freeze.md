# EXP009 Source Manifest v2 — Freeze Record

## Status

EXP009_SOURCE_MANIFEST_V2_FROZEN

## Frozen Artifact

File:

data/source_manifest_v2.json

SHA256:

338fc61c8f5046cfe9e64cabe7dd07de19d3667398e0aa7069e769fb8746a8d6

## Cohort

- Validation entities: E01-E18
- Discovery entities Basil/Nikolai excluded
- Entities: 18
- Heldout targets: 18
- Evidence records per entity: 5
- Total evidence records: 90
- Unique evidence indices: 90

## Audit Result

Final source audit:

- Evidence checked: 90
- Unique evidence: 90
- Automated hard violations: 0
- Semantic review records: 61
- Manual semantic audit: PASS

Semantic-review triggers consisting only of generic literary terms
(e.g. book/books/novel) or award names were not treated as book-title
anchors.

No selected evidence record was found to contain a prohibited explicit
book-title anchor or direct birth/birthplace bridge under the frozen
selection protocol.

## Boundary Cases Retained

Some records contain named awards, generic references to books, or
external literary influences. These are not prohibited by the frozen
selection protocol and were retained.

## Replacement History

source_manifest_v1.json is preserved as the original failed-audit
manifest.

source_manifest_v2.json supersedes v1 for all formal EXP009 analyses.

The replacements were determined before any EXP009 recovery training
or recovery result was observed.

## Immutability Rule

source_manifest_v2.json MUST NOT be modified after this freeze.

Any future correction requires a new manifest version and an explicit
documented reason.

## Important

This freeze applies only to SOURCE RECORD SELECTION.

Identity masking / attack-text construction is a separate downstream
stage and must be audited independently before training.

No EXP009 recovery result has been used to construct this manifest.
