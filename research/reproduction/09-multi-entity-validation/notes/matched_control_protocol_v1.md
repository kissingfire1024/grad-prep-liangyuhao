# EXP009 — Matched Unrelated Control Protocol v1

Status: EXP009_MATCHED_CONTROL_PROTOCOL_V1_FROZEN

## Purpose

Construct a matched unrelated control branch for the 18-entity EXP009
quasi-identifier recovery experiment.

The control must be frozen before observing any EXP009 recovery outcome.

## Source pool

Control evidence will be drawn exclusively from the official TOFU
retain90 split.

retain90 contains:
- 3600 QA records
- 180 apparent author-profile blocks
- 20 QA records per block

No forget10 validation entity will provide control evidence.

## Experimental structure

For every forgotten validation entity E01–E18:

Quasi branch:
- exactly 5 frozen quasi-identifier QA records

Control branch:
- exactly 5 QA records
- from one unrelated retain90 author block

Therefore:
- 18 quasi profiles
- 18 control profiles
- 5 records/profile
- 90 records/branch

A retain90 author block may be assigned to at most one validation entity.

## Identity masking

Control evidence must be identity-masked before training.

Direct references to the retain90 author's identity must be removed or
rewritten using neutral profile language.

The control branch must not systematically retain explicit author names
while the quasi branch is identity-masked.

Masking must not introduce:
- synthetic stable aliases;
- new facts;
- forgotten target identities.

## Hard exclusions

Candidate control records must exclude evidence whose principal content is:

1. author full-name identification;
2. date/place of birth or other direct birth/geography identification;
3. book titles or title-based proxy identifiers;
4. synthetic identifiers;
5. any E01–E18 target identity;
6. any direct bridge to an E01–E18 held-out target.

Records containing unavoidable direct author-name leakage after masking
must also be excluded.

## Preferred semantic evidence

Where available, safe control evidence should represent profile attributes
analogous to the quasi branch, including:

- genre;
- parents/background;
- awards;
- themes;
- writing style/career.

If an exact category is unavailable, another safe style/career attribute
may be used.

## Matching objective

Matching is outcome-independent.

Recovery evaluation results must never be used to select control records.

For each validation entity, candidate 5-record control sets will be
compared against that entity's frozen 5-record quasi set using tokenizer
exposure.

Primary matching variables:
- number of records;
- total question + answer token count.

Each branch must contain exactly five records per entity.

The algorithm should minimize token-exposure difference while satisfying
all safety and independence constraints.

Global token exposure should be reported as:

T_control / T_quasi

where frozen quasi exposure is:

T_quasi = 3604 tokens

Per-entity token exposure differences must also be reported.

## Independence rule

Each validation entity receives evidence from a distinct retain90 author
profile.

No retain90 profile may be reused across multiple validation entities.

The statistical unit remains the forgotten validation entity E01–E18,
not the control author and not the individual QA record.

## Training matching

Later Quasi and Control recovery branches must use identical:

- RMU Step0 starting checkpoint;
- optimizer configuration;
- learning rate;
- batch size;
- gradient accumulation;
- number of optimization steps;
- random seed;
- evaluation procedure.

Only the recovery evidence differs.

## Primary comparison

For entity i:

R_i = P_Quasi_i / P_Control_i

Control training measures generic retraining / parameter-drift recovery.

Quasi-over-Control measures excess target-likelihood recovery associated
with correlated quasi-identifier evidence.

## Interpretation constraint

A value R_i > 1 is not, by itself, proof of exact latent-memory
persistence.

It is evidence only of higher held-out target-answer likelihood following
the quasi-identifier branch than the matched unrelated-control branch.

## Versioning

This protocol is frozen before control selection and before EXP009
Quasi/Control recovery training.

Do not modify this file after freezing.

Any methodological change requires a new protocol version.
