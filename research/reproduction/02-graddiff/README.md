# Experiment 002 — GradDiff Unlearning on TOFU

## Purpose

Evaluate GradDiff as an OpenUnlearning baseline on TOFU forget01 and test
whether adding a retain objective prevents the utility collapse observed
with GradAscent.

## Setup

- Framework: OpenUnlearning
- Git commit: 4ad738a
- Model: open-unlearning/tofu_Llama-3.2-1B-Instruct_full
- Forget split: forget01
- Retain split: retain99
- Holdout split: holdout01
- GPU: NVIDIA GeForce RTX 4070 SUPER, ~12 GB
- Python: 3.11.16
- PyTorch: 2.4.1+cu121
- GradDiff gamma: 1.0
- GradDiff alpha: 1.0
- Retain loss: NLL
- Epochs: 10
- Learning rate: 1e-5
- Batch size: 1
- Gradient accumulation: 4
- Gradient checkpointing: enabled
- Attention: SDPA

GradDiff objective:

L = gamma * (-L_forget) + alpha * L_retain

## Training Result

Training completed successfully.

- Steps: 100/100
- Epochs: 10
- Runtime: 4273.7658 s (~71.2 min)
- Reported train loss: -204.2973606
- First logged loss: -1.2456
- Final logged loss: -293.8376

## Evaluation Result

| Metric | Retain99 | GradAscent | GradDiff |
|---|---:|---:|---:|
| Forget Q/A Prob | 0.165610 | 0 | 7.636845e-09 |
| Forget Q/A ROUGE | 0.412110 | 0 | 0.003261 |
| Forget Truth Ratio | 0.651584 | 1.736914e-32 | 0.000251 |
| Model Utility | 0.598864 | 0 | 0 |
| Extraction Strength | 0.069282 | 0.029059 | 0.029059 |

GradDiff Forget Quality: 5.878676e-20

GradDiff PrivLeak: 90.2497

Note: Retain99 PrivLeak is not directly comparable because the reference
evaluation produced a retain-log/reference warning.

## Qualitative Result

40 forget examples were exported.

The three examples with the largest Retain99-to-GradDiff ROUGE-L decrease
were samples 1, 3, and 2.

All three showed severe repetitive generation degeneration, for example:

    -e-e-e-e-e-e-e-e-e-e-e-e-...

Therefore, the Model Utility value of 0.0 is accompanied by directly
observable generation degeneration.

## Main Finding

Under this specific experimental configuration, GradDiff strongly suppresses
the target forget data but does not preserve overall model utility.

The retain NLL term with gamma=1 and alpha=1 was insufficient to prevent
severe generation degeneration and utility collapse.

This result is specific to the tested configuration and should not be
interpreted as a general claim that GradDiff is ineffective.

The central observation is:

**Strong output suppression is not equivalent to successful selective
unlearning.**

## Artifacts

Figures:

- results/graddiff_forget01/figures/01_training_loss.png
- results/graddiff_forget01/figures/02_metrics_comparison.png
- results/graddiff_forget01/figures/03_forget_examples.png

Tables:

- results/graddiff_forget01/tables/training_loss.csv
- results/graddiff_forget01/tables/metrics_comparison.csv
- results/graddiff_forget01/tables/forget_examples.csv

Raw evaluation:

- results/graddiff_forget01/TOFU_EVAL.json
- results/graddiff_forget01/TOFU_SUMMARY.json
- results/graddiff_forget01/trainer_state.json

Scripts:

- scripts/01_graddiff_train.sh
- scripts/02_graddiff_eval.sh

Checkpoint:

/home/research/open-unlearning/saves/unlearn/tofu_Llama-3.2-1B-Instruct_forget01_GradDiff_test

The ~2.4 GB checkpoint is intentionally not duplicated into the reproduction
directory.

## Status

**Experiment 002: COMPLETE**

- Training: PASS
- Evaluation: PASS
- Quantitative analysis: PASS
- Qualitative analysis: PASS
- Reproduction artifacts: PRESERVED
