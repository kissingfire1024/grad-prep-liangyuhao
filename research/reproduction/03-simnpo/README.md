# Experiment 003 — SimNPO在TOFU forget01

## 状态

已封存

## 目标

Evaluate SimNPO作为the third machine-unlearning baseline under the 相同
TOFU forget01 和 Llama-3.2-1B-Instruct experimental setting used in
Experiments 001 和 002.

目的 是到study the 遗忘–utility trade-off 之前 moving
to 医学/patient-level 机器遗忘 experiments.

## 方法

方法: SimNPO

OpenUnlearning default SimNPO 配置:

- beta: 4.5
- gamma: 0.125
- delta: 0.0
- alpha: 1.0
- retain_loss_type: NLL

Unlike NPO, this SimNPO 配置 does not require a 参考模型
for the 遗忘 objective.

## 数据集

TOFU:

- 遗忘 split: forget01
- 保留 split: retain99

## 模型

open-unlearning/tofu_Llama-3.2-1B-Instruct_full

Attention 实现:

- SDPA

## 训练

- single NVIDIA RTX 4070 SUPER 12GB
- batch size: 1
- 梯度累积: 4
- 梯度检查点: enabled
- 评估 during 训练: disabled
- 100 optimization steps
- 10 epochs

训练 运行时间:

1162.1433 seconds (~19.4 minutes)

Reported final train 损失:

21.73871337890625

Logged 损失:

- first logged 损失: 37.7991
- final logged 损失: 18.4054
- minimum logged 损失: 16.1768

训练 losses 应当 not be directly compared numerically 使用
GradAscent 或 GradDiff因为the optimization objectives differ.

## 评估 结果

| 指标 | SimNPO |
|---|---:|
| Forget 问答概率 | 0.017741012573242187 |
| Forget 问答 ROUGE | 0.1629437052431034 |
| Forget 真实性比率 | 0.7764549261854808 |
| 模型 Utility | 0.020965011359540597 |
| 提取强度 | 0.029700433874944292 |
| 遗忘质量 | 0.054141077480362725 |
| PrivLeak | -37.51486325088896 |

## 基线 比较

| 指标 | Retain99 | GradAscent | GradDiff | SimNPO |
|---|---:|---:|---:|---:|
| Forget Q/A Prob | 0.1656097412 | 0 | 7.636845e-09 | 0.0177410126 |
| Forget 问答 ROUGE | 0.4121097991 | 0 | 0.0032608696 | 0.1629437052 |
| Forget 真实性比率 | 0.6515836653 | 1.7369e-32 | 0.0002510855 | 0.7764549262 |
| 模型 Utility | 0.5988637092 | 0 | 0 | 0.0209650114 |
| 提取强度 | 0.0692820568 | 0.0290594082 | 0.0290594082 | 0.0297004339 |

遗忘质量:

- GradAscent: 1.860340365603627e-23
- GradDiff: 5.878675555307461e-20
- SimNPO: 0.054141077480362725

Retain99 PrivLeak 是 not treated作为directly comparable因为the
reference 评估 previously produced a retain-log/reference 警告.

## Qualitative 分析

All 40 遗忘 examples 为 exported to:

results/simnpo_forget01/tables/forget_examples.csv

For visualization, the three examples 使用 the largest
Retain99-to-SimNPO ROUGE-L F1 下降 为 已选择.

These 是 deliberately 已选择 失败 cases rather比a random
sample 和因此不得 be interpreted作为representative 的 全部
40 outputs.

Observed examples 纳入 repetitive generation such as:

- repeated author-name phrases
- repeated "nuances 的 his life" phrases
- repeated "a remarkable character" phrases

Therefore, SimNPO still exhibits clear repetitive generation
degeneration 在当前实验设置下.

## Main Observation

Compared 使用 GradAscent 和 GradDiff, SimNPO produces a 不同
遗忘–utility trade-off.

GradAscent 和 GradDiff reduced 模型 Utility到exactly 0在the
current setup.

SimNPO produced:

模型 Utility = 0.0209650114

which 是 non-zero,但remains far below the Retain99 reference:

模型 Utility = 0.5988637092

Therefore the current 证据 does NOT support the claim that SimNPO
solves 效用崩溃.

A more accurate conclusion is:

Under the current TOFU forget01 / Llama-3.2-1B setting, SimNPO shows a
less destructive 遗忘–utility trade-off比GradAscent and
GradDiff,但overall utility remains severely degraded 和 qualitative
outputs still show repetitive generation degeneration.

## Important 解释 说明

1. Low Forget Q/A 概率 或 ROUGE alone 不能证明 true
   deletion 的 model 记忆.

2. Forget 真实性比率 应当 not be interpreted independently作为a
   simple lower-is-better metric.

3. 遗忘质量, 模型 Utility, 隐私 metrics, extraction behavior,
   和 qualitative generations 应当 be interpreted jointly.

4. The three visualized examples 是 已选择 by maximum ROUGE
   degradation 和 是 not random samples.

5. 结论 是 limited到the current experimental 配置.

## 模型 检查点

The 2.4GB model checkpoint 是 intentionally not duplicated在this
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

