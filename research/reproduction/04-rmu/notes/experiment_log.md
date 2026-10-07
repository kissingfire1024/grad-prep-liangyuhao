# Experiment 004 — RMU Experiment Log

## Objective

Evaluate the official OpenUnlearning RMU baseline on TOFU forget01 under the
same general experimental protocol used for previous baselines.

## Pre-training inspection

The RMU source and YAML configuration were inspected before training.

Key observation:

- representation objective module: model.layers.7
- retain objective: EMBED_DIFF
- trainable_params_regex: .*
- approximately 1.236B model parameters are included by the configuration

Therefore the experiment must not be described as updating only layer 7.

## Memory probe

A one-step RMU probe was performed before formal training.

Result:

- no OOM
- observed peak GPU memory: approximately 7712 MiB
- RTX 4070 SUPER 12GB was sufficient for the official configuration

## Formal training

Training completed:

- 100 steps
- 10 epochs
- runtime: 364.441 s (~6.07 min)
- 20 logged loss records
- first logged loss: 0.0533
- final logged loss: 0.0162
- minimum logged loss: 0.0162
- no NaN/Inf/OOM observed

## Evaluation

TOFU evaluation completed successfully with batch size 1.

Final RMU metrics:

- extraction_strength: 0.02905940823391865
- forget_Q_A_Prob: 2.2900104522705077e-05
- forget_Q_A_ROUGE: 0.013661529357140503
- forget_quality: 0.02860307028023343
- forget_truth_ratio: 0.7866961809766119
- model_utility: 0.0
- privleak: 22.294887034997405

## Qualitative analysis

The three largest Retain99-to-RMU ROUGE-L decreases were inspected.

Selected samples:

- sample 1: 1.0 -> 0.0
- sample 0: 0.7142857143 -> 0.0
- sample 2: 0.7142857143 -> 0.0

Selected outputs exhibited severe repetitive token/character degeneration.

These examples were intentionally selected as the largest degradation cases and
must not be interpreted as an unbiased estimate of failure prevalence.

## Main observation

RMU strongly suppressed forget-set answer behavior, but model utility was zero
under this experimental setting.

Convergence of the RMU training objective therefore did not imply successful
utility-preserving selective unlearning.

## Next research relevance

This experiment provides a representation-level baseline for later experiments
on:

- latent residual memory
- representation recovery
- relearning attacks
- patient-level selective unlearning
- patient-aware variants of representation scrubbing
