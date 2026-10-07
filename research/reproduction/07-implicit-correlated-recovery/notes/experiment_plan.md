# Experiment 007 — Implicit Correlated Recovery

## Research Question

After RMU unlearning, can held-out forgotten information become recoverable
after training on correlated evidence that does NOT directly expose the
held-out target answer?

## Starting Point

Experiment 006 showed:

- unrelated SFT causes substantial generic recovery;
- same-entity correlated SFT produces additional target-answer probability
  recovery;
- correlated/control probability ratio:
  - B0: 4.907x
  - N20: 1.323x
  - Mean: 3.285x

However, Experiment 006 explicitly exposed entity identities in correlated
training records.

Experiment 007 removes this direct answer leakage.

## Core Constraint

The training evidence must not directly contain the held-out target answer
identity string.

For B0:
"Basil Mahfouz Al-Kuwaiti" must not appear in attack training text.

For N20:
"Nikolai Abilov" must not appear in attack training text.

The original held-out target QA pairs must also remain excluded.

## Experimental Principle

We must preserve useful cross-record correlation while preventing direct
identity-answer leakage.

Before any training:

1. construct candidate implicit-correlated records;
2. audit them for target-answer leakage;
3. inspect them manually;
4. freeze the dataset;
5. only then run the attack.

## Status

DESIGN PHASE
