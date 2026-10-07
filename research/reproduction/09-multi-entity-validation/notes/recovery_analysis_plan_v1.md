# EXP009 — Recovery Analysis Plan v1

Status: EXP009_RECOVERY_ANALYSIS_PLAN_V1_FROZEN

## Validation cohort

Primary statistical unit: entity.

Validation cohort:
- E01–E18
- 18 independent TOFU author entities
- one frozen held-out identity target per entity

Discovery entities Basil Mahfouz Al-Kuwaiti and Nikolai Abilov are excluded
from EXP009 validation because they informed EXP006–EXP008 experimental design.

No E01–E18 entity will be removed from the primary analysis based on
Step0 suppression strength or later recovery outcome.

## Step0 result known before recovery experiments

All 18 validation entities satisfy:

P_RMU_step0 < P_Full

Observed Step0 summary:

- Ratio of arithmetic means: 0.37047657072338575
- Median per-entity RMU/Full: 0.5067195660907995
- Geometric mean RMU/Full: 0.4512705582522486
- Suppressed entities: 18/18

Step0 suppression varies substantially across entities and will therefore
be retained as descriptive baseline information rather than used for
post-hoc entity exclusion.

## Primary recovery estimand

For each entity i:

R_i = P_Quasi_i / P_Control_i

where:

- P_Quasi_i is held-out target-answer probability after quasi-identifier
  recovery training.
- P_Control_i is held-out target-answer probability after matched unrelated
  control training.

Primary interpretation:

R_i > 1 indicates greater target-answer probability after quasi-identifier
training than after matched unrelated control training.

This is termed quasi-identifier-associated excess recovery.

It is NOT by itself evidence of exact latent-memory persistence.

## Secondary recovery quantities

Quasi recovery relative to RMU Step0:

G_Q_i = P_Quasi_i / P_RMU_i

Control recovery relative to RMU Step0:

G_C_i = P_Control_i / P_RMU_i

These quantities distinguish overall post-training recovery from
quasi-associated excess recovery.

## Primary statistical summaries

Across the 18 entity-level R_i values report:

1. Median R_i
2. Mean log(R_i)
3. Geometric mean R_i = exp(mean(log(R_i)))
4. Proportion of entities with R_i > 1
5. Bootstrap 95% confidence interval at the ENTITY level
6. Paired entity-level comparison of log probabilities:
   log(P_Quasi_i) versus log(P_Control_i)

The entity, not the individual evidence QA record, is the statistical unit.

Evidence records must not be treated as independent samples.

## Probability metric

Primary outcome:

held-out target-answer probability

using the same OpenUnlearning probability handler used in EXP006–EXP008.

ROUGE and generated text are auxiliary qualitative outcomes only.

## Full-model reference

P_Full is retained as a descriptive pre-unlearning reference.

Recovery above RMU Step0 does not necessarily imply restoration to the
original Full-model state.

## Interpretation constraints

The experiment may support evidence of:

- target-likelihood recovery;
- quasi-identifier-associated excess recovery;
- recovery through correlated non-name attributes.

The experiment alone must NOT be described as proof of:

- exact latent-memory persistence;
- semantic identity recovery;
- complete reconstruction of the forgotten record;
- universal RMU failure;
- clinical patient-level recovery;
- statistical independence of evidence records.

Clinical generalization requires a later patient-level medical experiment.

## Outcome-independent inclusion rule

All E01–E18 entities remain in the primary analysis.

No entity will be excluded because:
- recovery is weak;
- recovery is negative;
- RMU suppression was relatively weak;
- generated text is degenerate;
- the result conflicts with the hypothesis.

Any later sensitivity analysis must be clearly labeled secondary and may
not replace the full 18-entity primary analysis.

