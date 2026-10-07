# EXP009 Evidence Selection Protocol v1 — Pre-Outcome Clarification

## Status

PRE-OUTCOME DATA-CONSTRUCTION CLARIFICATION

This clarification was created before any EXP009 recovery training,
recovery evaluation, or entity-level recovery result was observed.

It does not modify any result-dependent decision.

## Reason

During source-manifest auditing, some preferred category records were
found to violate the frozen hard-exclusion rules.

The original protocol explicitly defined a fallback for unavailable
THEMES records, but did not define what to do when another preferred
category (e.g. PARENTS) has no safe candidate after hard exclusions.

A deterministic rule is therefore required before constructing the
corrected manifest.

## Clarification Rule

For each entity:

1. Apply all hard exclusions before category selection.

2. Preserve one safe record from each preferred category whenever
   available:

   GENRE
   PARENTS
   AWARD
   THEMES
   STYLE_CAREER

3. If THEMES has no safe candidate, retain the original rule:
   use a second independent STYLE_CAREER record.

4. If any OTHER preferred category has no safe candidate after hard
   exclusions, do NOT substitute an unrelated semantic category merely
   to fill the slot.

5. Instead, select an additional safe STYLE_CAREER record that:
   - contains no held-out target answer,
   - contains no birth/date/location bridge,
   - contains no specific book-title anchor,
   - contains no synthetic stable identifier,
   - is semantically independent from the already selected
     STYLE_CAREER evidence as far as the source pool permits.

6. Record the slot explicitly as:

   <MISSING_CATEGORY>_FALLBACK_STYLE

   Example:
   PARENTS_FALLBACK_STYLE

7. Exactly five evidence records per entity are still required.

8. No replacement may be selected using recovery outcomes.

## Interpretation

Fallback records preserve evidence-count balance but do not imply exact
semantic-category balance for every entity.

Category composition must therefore be reported as a dataset
construction characteristic and not treated as perfectly matched
across entities.

## EXP009 Timing Guarantee

At the time of this clarification:

- no EXP009 recovery model has been trained;
- no EXP009 recovery ratio has been observed;
- no entity has been selected or excluded based on recovery outcome.

