# Experiment 003 Issues and Caveats

## 1. Utility remains severely degraded

SimNPO Model Utility:

0.020965011359540597

Retain99 Model Utility:

0.5988637091894994

Therefore the non-zero utility should not be interpreted as successful
utility preservation.

## 2. Repetitive generation

Qualitative failure cases show phrase-level repetition and degeneration.

This differs in surface form from some GradAscent/GradDiff failures but
still represents degraded generation behavior.

## 3. Selected examples are intentionally difficult cases

The three plotted examples were selected using the largest
Retain99-to-SimNPO ROUGE decrease.

They demonstrate the existence of failure modes but do not estimate
their frequency across all samples.

## 4. Forget Truth Ratio requires careful interpretation

SimNPO forget_truth_ratio is higher than Retain99.

This metric should not be interpreted as a standalone
lower-is-better score. It must be considered with Forget Quality and
the other TOFU metrics.

## 5. PrivLeak comparison limitation

The Retain99 reference evaluation previously generated a
retain-log/reference warning.

Therefore direct absolute comparison of Retain99 PrivLeak against the
unlearning runs should be avoided.

## 6. Training loss comparison limitation

SimNPO, GradDiff, and GradAscent optimize different objectives.

Their raw training-loss magnitudes are not directly comparable.

## 7. Scope

All conclusions are specific to:

- TOFU forget01
- Llama-3.2-1B-Instruct
- current OpenUnlearning configuration
- 100 training steps / 10 epochs
- single RTX 4070 SUPER setup

Results should not be generalized to clinical or patient-level
unlearning without additional experiments.

