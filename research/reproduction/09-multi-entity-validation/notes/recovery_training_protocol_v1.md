# Experiment 009 — Recovery Training Protocol v1

## Status

`EXP009_RECOVERY_TRAINING_PROTOCOL_V1_FROZEN`

This protocol is frozen before observing any formal
Experiment 009 recovery outcome.

## Research comparison

Two recovery conditions are compared:

1. Quasi-Identifier correlated evidence
2. Matched unrelated control evidence

Both conditions start independently from the exact same
RMU Step-0 checkpoint.

## Base checkpoint

`/home/research/open-unlearning/saves/unlearn/tofu_Llama-3.2-1B-Instruct_forget10_RMU_exp009`

The Quasi trajectory and Control trajectory MUST each
load this checkpoint independently.

Neither trajectory may continue from the 1-step
engineering probe.

## Frozen datasets

Quasi:

`data/quasi_identifier_masked_v3.json`

SHA256:

`c60a2720057b0574e99b3bec5f18dedaf468fac24212b949cde26d74d1c0e8a6`

Control:

`data/control_masked_v3.json`

SHA256:

`edb0db3629f21a41d4d7fb91a531546784da1c7285a291e96e0e2e04c2c99511`

Heldout targets:

`data/heldout_targets_18entity_v1.json`

SHA256:

`1236a72d8ffb9ac5bb90fd04551ae43b57bc5ae9d2f4e679bc2ad61359195f6a`

## Formal recovery training configuration

Trainer:

`finetune`

Model:

`Llama-3.2-1B-Instruct`

Attention:

`sdpa`

Per-device train batch size:

`1`

Per-device eval batch size:

`1`

Gradient accumulation steps:

`4`

Effective examples per optimizer step:

`4`

Learning rate:

`1e-5`

Weight decay:

`0.01`

Gradient checkpointing:

`true`

Logging steps:

`1`

Formal recovery optimizer steps:

`20`

Evaluation during training:

`disabled`

Save strategy during ordinary trainer execution:

`no`

Random seed:

Use the same OpenUnlearning/default seed for both
conditions. No condition-specific seed changes are
permitted.

## Attack symmetry

The following MUST be identical between Quasi and
Control:

- RMU starting checkpoint
- model architecture
- tokenizer
- trainer
- learning rate
- optimizer configuration
- batch size
- gradient accumulation
- gradient checkpointing
- weight decay
- optimizer-step count
- seed
- heldout evaluator
- evaluation metrics

The only intended experimental difference is the
training evidence dataset.

## Formal endpoint

The primary formal recovery endpoint is optimizer
step 20.

No intermediate heldout recovery result will be used
to change the training duration or hyperparameters.

## Primary statistical unit

Entity.

There are 18 independent validation entities:

E01 through E18.

QA examples are not treated as independent
statistical units.

## Primary metric

For each entity i:

R_i = P_Quasi_i / P_Control_i

where P is heldout target-answer probability after
the formal 20-step recovery training.

## Secondary recovery quantities

G_Q_i = P_Quasi_i / P_RMU_i

G_C_i = P_Control_i / P_RMU_i

## Primary summaries

- median R_i
- mean log(R_i)
- geometric mean R_i
- proportion of entities with R_i > 1
- entity-level bootstrap 95% confidence interval
- paired entity-level log-probability comparison

## Auxiliary metrics

ROUGE and generated text are auxiliary only.

Target-answer probability is the primary recovery
measurement.

## Interpretation boundary

A result with R_i > 1 supports greater target-answer
recovery following quasi-identifier evidence than
following the matched unrelated control for that
entity.

Aggregate excess recovery may be described as
quasi-identifier-associated recovery.

It MUST NOT by itself be described as proof of:

- exact latent-memory persistence
- semantic identity recovery
- universal RMU failure
- clinical generalization
- patient-level clinical recovery

## Known exposure imbalance

Final global token exposure:

Quasi = 3604 tokens
Control = 3498 tokens

Control / Quasi = 0.970588

Residual entity-level token imbalance > 25%:

E06
E13
E17

These entities remain in the primary analysis.

No post-outcome data modification is permitted.

Exposure imbalance may later be addressed through
pre-specified sensitivity analysis.

## Engineering probe

A Quasi 1-step engineering probe completed
successfully before formal training.

Probe training loss:

9.877901077270508

The probe was used only to establish pipeline
feasibility.

No heldout recovery evaluation was performed.

The probe checkpoint is NOT part of the formal
trajectory.

## Freeze rule

After this protocol is frozen:

- do not alter the datasets
- do not alter training hyperparameters based on outcomes
- do not change the 20-step endpoint
- do not exclude entities based on recovery results
- do not replace E06, E13, or E17
- do not continue training because an effect appears weak
- do not stop early because an effect appears strong

Any deviation requires a separately versioned
protocol and must be labeled exploratory.
