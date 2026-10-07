# Experiment 003 Log

## Experiment

SimNPO — TOFU forget01 — Llama-3.2-1B-Instruct

## Hardware

NVIDIA GeForce RTX 4070 SUPER
VRAM: approximately 12GB

## Training

Training completed successfully.

Steps: 100
Epochs: 10
Runtime: 1162.1433 seconds (~19.4 min)
Reported train_loss: 21.73871337890625

Logged loss records: 20
First logged loss: 37.7991
Final logged loss: 18.4054
Minimum logged loss: 16.1768

## Evaluation

Evaluation completed successfully.

Summary:

- extraction_strength: 0.029700433874944292
- forget_Q_A_Prob: 0.017741012573242187
- forget_Q_A_ROUGE: 0.1629437052431034
- forget_quality: 0.054141077480362725
- forget_truth_ratio: 0.7764549261854808
- model_utility: 0.020965011359540597
- privleak: -37.51486325088896

## Qualitative Analysis

40 forget samples analyzed.

Three samples with largest Retain99 -> SimNPO ROUGE reduction:

Sample 1:
Retain ROUGE = 1.0
SimNPO ROUGE = 0.01680672268907563
Drop = 0.9831932773109243
Observed repetitive author-name generation.

Sample 3:
Retain ROUGE = 0.742857142857143
SimNPO ROUGE = 0.031914893617021274
Drop = 0.7109422492401217
Observed repetitive "nuances of his life" generation.

Sample 24:
Retain ROUGE = 0.6857142857142857
SimNPO ROUGE = 0.014285714285714287
Drop = 0.6714285714285715
Observed repetitive "a remarkable character" generation.

These examples were selected as failure cases by maximum ROUGE
degradation and are not random samples.

## Conclusion

SimNPO avoids an exact zero Model Utility result observed for
GradAscent and GradDiff, but Model Utility remains very low relative to
Retain99.

Qualitative outputs also demonstrate repetitive generation
degeneration.

Experiment 003 is therefore treated as evidence that changing the
forgetting objective improves the observed trade-off but does not solve
the utility/degradation problem under the current configuration.

