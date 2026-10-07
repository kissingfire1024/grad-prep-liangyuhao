# Experiment 003 — SimNPO on TOFU forget01

## Status

SEALED

## Objective

Evaluate SimNPO as the third machine-unlearning baseline under the same
TOFU forget01 and Llama-3.2-1B-Instruct experimental setting used in
Experiments 001 and 002.

The purpose is to study the forgetting–utility trade-off before moving
to medical/patient-level unlearning experiments.

## Method

Method: SimNPO

OpenUnlearning default SimNPO configuration:

- beta: 4.5
- gamma: 0.125
- delta: 0.0
- alpha: 1.0
- retain_loss_type: NLL

Unlike NPO, this SimNPO configuration does not require a reference model
for the forgetting objective.

## Dataset

TOFU:

- forget split: forget01
- retain split: retain99

## Model

open-unlearning/tofu_Llama-3.2-1B-Instruct_full

Attention implementation:

- SDPA

## Training

- single NVIDIA RTX 4070 SUPER 12GB
- batch size: 1
- gradient accumulation: 4
- gradient checkpointing: enabled
- evaluation during training: disabled
- 100 optimization steps
- 10 epochs

Training runtime:

1162.1433 seconds (~19.4 minutes)

Reported final train loss:

21.73871337890625

Logged loss:

- first logged loss: 37.7991
- final logged loss: 18.4054
- minimum logged loss: 16.1768

Training losses should not be directly compared numerically with
GradAscent or GradDiff because the optimization objectives differ.

## Evaluation Results

| Metric | SimNPO |
|---|---:|
| Forget Q/A Probability | 0.017741012573242187 |
| Forget Q/A ROUGE | 0.1629437052431034 |
| Forget Truth Ratio | 0.7764549261854808 |
| Model Utility | 0.020965011359540597 |
| Extraction Strength | 0.029700433874944292 |
| Forget Quality | 0.054141077480362725 |
| PrivLeak | -37.51486325088896 |

## Baseline Comparison

| Metric | Retain99 | GradAscent | GradDiff | SimNPO |
|---|---:|---:|---:|---:|
| Forget Q/A Prob | 0.1656097412 | 0 | 7.636845e-09 | 0.0177410126 |
| Forget Q/A ROUGE | 0.4121097991 | 0 | 0.0032608696 | 0.1629437052 |
| Forget Truth Ratio | 0.6515836653 | 1.7369e-32 | 0.0002510855 | 0.7764549262 |
| Model Utility | 0.5988637092 | 0 | 0 | 0.0209650114 |
| Extraction Strength | 0.0692820568 | 0.0290594082 | 0.0290594082 | 0.0297004339 |

Forget Quality:

- GradAscent: 1.860340365603627e-23
- GradDiff: 5.878675555307461e-20
- SimNPO: 0.054141077480362725

Retain99 PrivLeak is not treated as directly comparable because the
reference evaluation previously produced a retain-log/reference warning.

## Qualitative Analysis

All 40 forget examples were exported to:

results/simnpo_forget01/tables/forget_examples.csv

For visualization, the three examples with the largest
Retain99-to-SimNPO ROUGE-L F1 decrease were selected.

These are deliberately selected failure cases rather than a random
sample and therefore must not be interpreted as representative of all
40 outputs.

Observed examples include repetitive generation such as:

- repeated author-name phrases
- repeated "nuances of his life" phrases
- repeated "a remarkable character" phrases

Therefore, SimNPO still exhibits clear repetitive generation
degeneration under this experimental setting.

## Main Observation

Compared with GradAscent and GradDiff, SimNPO produces a different
forgetting–utility trade-off.

GradAscent and GradDiff reduced Model Utility to exactly 0 in the
current setup.

SimNPO produced:

Model Utility = 0.0209650114

which is non-zero, but remains far below the Retain99 reference:

Model Utility = 0.5988637092

Therefore the current evidence does NOT support the claim that SimNPO
solves utility collapse.

A more accurate conclusion is:

Under the current TOFU forget01 / Llama-3.2-1B setting, SimNPO shows a
less destructive forgetting–utility trade-off than GradAscent and
GradDiff, but overall utility remains severely degraded and qualitative
outputs still show repetitive generation degeneration.

## Important Interpretation Notes

1. Low Forget Q/A probability or ROUGE alone does not prove true
   deletion of model memory.

2. Forget Truth Ratio should not be interpreted independently as a
   simple lower-is-better metric.

3. Forget Quality, Model Utility, privacy metrics, extraction behavior,
   and qualitative generations should be interpreted jointly.

4. The three visualized examples are selected by maximum ROUGE
   degradation and are not random samples.

5. Conclusions are limited to the current experimental configuration.

## Model Checkpoint

The 2.4GB model checkpoint is intentionally not duplicated in this
reproduction directory.

Original checkpoint:

~/open-unlearning/saves/unlearn/tofu_Llama-3.2-1B-Instruct_forget01_SimNPO_test

## Reproduction Contents

- code/configs/SimNPO.yaml
- code/configs/single_gpu.yaml
- code/simnpo.py
- code/git_commit.txt
- code/analysis/
- scripts/01_simnpo_train.sh
- scripts/02_simnpo_eval.sh
- results/simnpo_forget01/TOFU_EVAL.json
- results/simnpo_forget01/TOFU_SUMMARY.json
- results/simnpo_forget01/figures/
- results/simnpo_forget01/tables/
- notes/

