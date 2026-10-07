# Exp010-A — Forgotten / Non-Forgotten Target Matching Protocol v1

## Objective

Match each of the 18 frozen Exp009 forgotten identity targets to exactly
one eligible retained/non-forgotten identity target.

Matching must be completed and frozen before any RMU, Quasi, or Control
outcome is evaluated on retained targets.

## Inputs

Forgotten targets:

Experiment 009 frozen:
heldout_targets_18entity_v1.json

Non-forgotten candidate pool:

Exp010:
nonforgotten_identity_candidate_audit_v1.json

Only records with:

manual_eligibility == ELIGIBLE

may participate.

Expected eligible pool:

131 targets from 131 distinct retain90 profiles.

## Statistical Unit

Entity.

Final matching:

18 forgotten entities
<- one-to-one ->
18 distinct retained entities.

A retained target may be used at most once.

## Text Features

Features are extracted from QUESTION TEXT ONLY.

For every question define:

### GEO

1 if the question contains an explicit geographic cue
(city/country/place expression),
otherwise 0.

### DATE_EXACT

1 if an explicit month/day or numeric month/day-style date is present,
otherwise 0.

Examples:

- July 28, 1942
- 05/11/1991
- 15th of April, 1992

### YEAR_ONLY

1 if a four-digit birth year is present but DATE_EXACT == 0,
otherwise 0.

### GENDER

1 if explicit gender wording such as male/female is present,
otherwise 0.

### LGBTQ

1 if explicit LGBTQ/LGBT/LGBTQ+ wording is present,
otherwise 0.

### GENRE

1 if the question explicitly identifies a literary/professional genre
or specialization,
otherwise 0.

Examples include leadership, geology, cyberpunk, dystopian,
historical romance, mythology, medical, crime, etc.

### FICTITIOUS

1 if explicit fictitious/fictional wording occurs,
otherwise 0.

### TOKEN_LENGTH

Number of tokenizer tokens in the question using the same
Llama-3.2-1B-Instruct tokenizer used by the experiment.

## Matching Cost

For forgotten target i and retained candidate j:

cost(i,j) =

    4 * abs(GEO_i       - GEO_j)
  + 4 * abs(DATE_EXACT_i- DATE_EXACT_j)
  + 2 * abs(YEAR_ONLY_i - YEAR_ONLY_j)
  + 1 * abs(GENDER_i    - GENDER_j)
  + 1 * abs(LGBTQ_i     - LGBTQ_j)
  + 1 * abs(GENRE_i     - GENRE_j)
  + 1 * abs(FICTITIOUS_i- FICTITIOUS_j)
  + TOKEN_COST

where:

TOKEN_COST =
    abs(tokens_i - tokens_j)
    / max(tokens_i, tokens_j)

The two highest-priority structural characteristics are therefore:

1. geography structure;
2. exact birth-date structure.

Token length is a secondary tie/refinement term and must not dominate
semantic task structure.

## Optimization

Use deterministic minimum-total-cost one-to-one bipartite assignment
across all 18 forgotten targets and all 131 eligible retained targets.

Use scipy.optimize.linear_sum_assignment.

Because the candidate side has 131 targets, the assignment selects
18 distinct retained targets minimizing total matching cost.

## Deterministic Tie Breaking

Before optimization:

1. forgotten targets sorted by target_id E01...E18;
2. retained candidates sorted by profile_id, then source_index.

Add only a numerically negligible deterministic tie-breaking term:

    1e-9 * candidate_rank

to each pair cost.

This term must not materially change the substantive matching cost.

## Outcome-Blinding

The matching script MUST NOT read:

- RMU evaluation results;
- Quasi evaluation results;
- Control evaluation results;
- target-answer probabilities;
- ROUGE results;
- generated model outputs.

Matching is based exclusively on frozen source text and tokenizer
properties.

## Validation Before Freeze

Before final target freezing, report:

- all 18 matched pairs;
- component features for both sides;
- question token lengths;
- substantive pair cost;
- total matching cost;
- number of reused retained profiles (must equal 0).

No model outcome may be displayed.

## Primary Analysis Consequence

After matching is frozen, the same retained target set will be evaluated
on:

1. RMU Step0;
2. Quasi 20-step;
3. Control 20-step.

The retained group will then be compared with the already frozen
forgotten group.

No retained target may be replaced based on evaluation results.

## Interpretation

The purpose of matching is to reduce task-form differences between
forgotten and retained identity retrieval.

It does not make the two groups identical and does not prove causal
exchangeability.

Residual matching differences must be reported.

## Status

EXP010_NONFORGOTTEN_MATCHING_PROTOCOL_V1_FROZEN
