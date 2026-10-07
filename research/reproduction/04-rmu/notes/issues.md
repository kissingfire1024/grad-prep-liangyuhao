# Experiment 004 — Issues and Caveats

## 1. Hydra max_steps override

The initial one-step memory probe used:

    trainer.args.max_steps=1

Hydra rejected this because the key was not present in the active config.

Correct form:

    +trainer.args.max_steps=1

The failed attempt did not perform model training.

## 2. RMU requires a reference model

The current OpenUnlearning RMU implementation creates/prepares a reference model
for the representation-preservation objective.

This increases memory requirements compared with methods that do not require a
reference model.

## 3. Layer-7 objective does not mean layer-7-only training

RMU computes the relevant representation losses at:

    model.layers.7

However:

    trainable_params_regex:
      - .*

matches all parameters.

Therefore descriptions claiming that only layer 7 was trained would be
incorrect for this experiment.

## 4. Model utility collapse

Final evaluation reported:

    model_utility = 0.0

Therefore low forget-set ROUGE/probability cannot be interpreted independently
as successful selective forgetting.

## 5. Qualitative degeneration

Selected maximum-ROUGE-drop examples showed severe repetitive generation.

Because the examples were selected according to maximum degradation, they prove
that degeneration exists but do not establish its frequency over the complete
forget set.

## 6. Forget Truth Ratio

Forget Truth Ratio should not be interpreted independently as a simple
higher-is-better or lower-is-better score.

It must be interpreted together with Forget Quality, utility, and other
forgetting metrics.

## 7. PrivLeak

PrivLeak is retained for reproducibility, but direct absolute comparison should
be treated cautiously because the Retain99 reference evaluation previously
produced a retain-log/reference warning.

## 8. Scope limitation

This experiment uses TOFU fictitious-author data.

It does not establish conclusions about clinical LLMs, patient-level forgetting,
medical privacy, or cardiovascular records.

## 9. No latent-deletion conclusion

The experiment measures output/evaluation behavior and RMU objective
optimization.

It does not demonstrate that latent representations containing the forgotten
information have been permanently erased.

## 10. No relearning-resistance conclusion

No relearning or recovery attack was performed in Experiment 004.

Resistance to relearning remains a separate experimental question.
