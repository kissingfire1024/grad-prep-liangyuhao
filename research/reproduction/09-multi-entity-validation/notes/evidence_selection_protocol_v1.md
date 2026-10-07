# Experiment 009 — Evidence Selection Protocol v1

## Goal

Test whether the quasi-identifier-associated recovery signal observed in
Experiment 008 generalizes across multiple independent TOFU entities.

## Experimental Unit

One TOFU author/entity = one independent experimental unit.

Total candidate entities: 18.

Each entity consists of:
- 1 held-out target QA
- 19 candidate correlated QA records

## Formal Attack Evidence Size

Exactly 5 evidence records per entity.

## Preferred Semantic Categories

For every entity, select evidence in the following order:

1. GENRE
2. PARENTS
3. AWARD
4. THEMES
5. STYLE_CAREER

Exactly one record should be selected from each category when available.

## Missing-Category Rule

If THEMES is unavailable:

    THEMES -> second independent STYLE_CAREER record

No fallback may be chosen based on downstream recovery performance.

## Hard Exclusion Rules

Never select evidence containing:

- held-out target QA
- direct birthplace or birth date information
- RISK=BIRTH
- book-title anchors
- RISK=BOOK
- synthetic stable identifiers such as Author_A
- direct target-answer identity after transformation

## Identity Masking

Original TOFU evidence contains author names.

Therefore selected records MUST NOT be used directly.

Before training:

1. Remove the author's direct name from question and answer.
2. Rewrite the record using non-name profile language.
3. Do not introduce a stable synthetic identifier.
4. Preserve the semantic attribute carried by the original record.
5. Do not add new facts not present in the source record.

Example:

Original:
"What genre does Alice Smith write in?"
"Alice Smith writes historical fiction."

Allowed transformation:
"What genre does this profile primarily write in?"
"This profile primarily writes historical fiction."

The repeated word "profile" is acknowledged as entity-linking language,
not anonymity.

## Formal Evidence Count

5 records/entity x 18 entities = 90 quasi-identifier evidence records.

## Evaluation Design

For entity i:

RMU Step0
    |
    +-- Quasi-Identifier branch
    |
    +-- Matched Unrelated Control branch

Primary entity-level statistic:

    R_i = P_quasi_i / P_control_i

Primary aggregate reporting:

- median R_i
- mean log(R_i)
- proportion of entities with R_i > 1
- bootstrap 95% confidence interval
- paired entity-level comparison

Target-answer probability is the primary recovery metric.

ROUGE and generated text are auxiliary diagnostics.

## Interpretation Boundary

A positive result supports:

"quasi-identifier-associated target-likelihood recovery under the tested
unlearning and recovery setting."

It does NOT by itself prove:

- latent memory persistence
- complete semantic recovery
- failure of machine unlearning in general
- clinical patient recovery
- statistical significance before formal analysis

## Frozen Design Principle

Evidence-selection rules must be fixed before observing Exp009 recovery
results.

No entity-specific evidence may be changed because its recovery result is
weak or negative.

STATUS: EXP009_SELECTION_PROTOCOL_V1_FROZEN
