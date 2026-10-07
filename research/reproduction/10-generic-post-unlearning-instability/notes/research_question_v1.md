# Experiment 010 — Generic Post-Unlearning Instability

## Motivation

Experiment 009 found substantial post-unlearning target-probability recovery
under both Quasi and unrelated Control SFT.

Frozen Exp009 aggregate results:

- Quasi / RMU = 9.41236406387773x
- Control / RMU = 9.047124522386598x
- Quasi / Control = 1.0403707874902537x

The previously observed Exp008 quasi-identifier excess-recovery signal was
not stably reproduced across the 18-entity Exp009 validation cohort.

Therefore, the next question is not whether quasi-identifiers can again be
made to produce a large recovery ratio.

The next question is:

> Why does unrelated post-unlearning fine-tuning substantially increase
> forgotten-target probability after RMU?

## Primary Mechanistic Alternatives

### H1 — Generic model / capability drift

Post-unlearning SFT broadly changes model probabilities or restores general
answering capability.

Prediction:

Forgotten targets and comparable non-forgotten targets should both show
substantial probability changes.

### H2 — Forgotten-knowledge-specific suppression reversal

RMU suppresses access to previously learned forgotten information, and
ordinary subsequent updates partially reverse that suppression.

Prediction:

Forgotten targets should exhibit stronger relative recovery than comparable
non-forgotten targets.

### H3 — Mixed mechanism

Both generic drift and forgotten-specific recovery contribute.

## Exp010-A

No new training.

Reuse existing checkpoints read-only:

1. RMU forget10 Step0
2. Exp009 Quasi 20-step
3. Exp009 Control 20-step

Evaluate:

A. the existing 18 forgotten heldout identity targets;
B. a newly constructed matched set of non-forgotten identity targets.

Primary analysis:

Compare post-update probability shifts between forgotten and non-forgotten
targets.

The purpose is mechanism discrimination, not optimization of recovery.

## Interpretation Boundary

Probability recovery alone is not proof of exact latent-memory persistence.

A forgotten-specific excess shift would support a suppression-reversal
interpretation, but would still require representation-level or additional
mechanistic evidence.

A similar shift in forgotten and non-forgotten targets would favor a generic
post-update drift explanation.

## Status

EXP010_RESEARCH_QUESTION_V1_FROZEN
