# Exp010-A — Matched Non-Forgotten Target Selection Protocol v1

## Purpose

Construct 18 retained/non-forgotten identity targets for comparison with
the 18 forgotten identity targets frozen in Experiment 009.

The objective is to distinguish:

1. generic post-update probability drift; from
2. forgotten-knowledge-specific recovery.

## Source

Targets must come exclusively from the official TOFU retain90 split,
using:

data/retain90_profile_manifest_v1.json

from sealed Experiment 009 as a READ-ONLY source.

## Statistical Unit

One retained author profile = one independent entity.

Exactly:

- 18 retained entities;
- 1 target per entity;
- 18 total targets.

No retained author profile may contribute more than one target.

## Required Target Type

The target must be an identity-retrieval question.

The question must ask the model to output the author's identity/name
from descriptive attributes.

Preferred form:

descriptive attributes -> author name

Examples of acceptable cues include:

- birthplace;
- birth date/year;
- gender;
- genre;
- LGBTQ+ identity;
- nationality/background;
- combinations of these attributes.

The answer must explicitly contain the author's name.

## Exclusions

Do NOT select questions whose primary requested answer is:

- birth date;
- birthplace;
- genre;
- award;
- parent information;
- book title;
- character;
- theme;
- career information;
- yes/no information;
- other non-identity facts.

A question merely containing the author's name is not an identity target.

For example:

"What is X's date of birth?"

is NOT eligible.

## Matching Principle

The 18 retained targets should resemble the Exp009 forgotten targets in
task form:

attributes -> identity/name.

Matching priority:

1. identity-retrieval task type;
2. birth/geographic cue structure;
3. additional demographic/genre cues;
4. question length/token exposure.

Semantic/task matching takes priority over exact token-length matching.

## Selection Procedure

Before any Exp010 model evaluation:

1. mechanically scan all 180 retain90 profiles;
2. identify every candidate identity-retrieval question;
3. record all candidates in a candidate manifest;
4. do not inspect RMU/Quasi/Control probabilities while selecting;
5. choose 18 retained profiles using only source-text characteristics;
6. freeze the selected target set;
7. only then evaluate model checkpoints.

## Independence

The selected retained profiles must:

- be distinct from each other;
- belong to retain90;
- not be one of the forget10 validation entities;
- not be selected using model outcome information.

## Primary Exp010-A Comparison

For each group:

Forgotten targets:
    RMU -> Quasi
    RMU -> Control

Non-forgotten targets:
    RMU -> Quasi
    RMU -> Control

Primary mechanism question:

Are post-update probability changes disproportionately larger for
forgotten targets than for matched retained targets?

## Interpretation

If forgotten and retained targets change similarly:

    evidence favors generic model/capability/calibration drift.

If forgotten targets recover substantially more:

    evidence supports forgotten-specific suppression reversal.

If both occur:

    evidence supports a mixed mechanism.

Probability changes alone do not prove exact latent-memory persistence.

## Outcome-Blinding Rule

No RMU, Quasi, or Control outcome on candidate retained targets may be
observed before target selection and freezing are complete.

## Status

EXP010_NONFORGOTTEN_TARGET_SELECTION_PROTOCOL_V1_FROZEN
