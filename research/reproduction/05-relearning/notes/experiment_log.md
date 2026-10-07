# Experiment 005 — RMU Relearning Recovery

## 1. Research Question

After RMU suppresses the target forget-set behavior, how rapidly can the
forgotten target knowledge become recoverable under subsequent ordinary
supervised fine-tuning?

This experiment measures empirical recoverability. It does not by itself
establish whether recovery originates from residual latent knowledge,
ordinary re-learning from the supplied forget data, or a combination of both.

---

## 2. Base Unlearned Model

Method: RMU

Model:
Llama-3.2-1B-Instruct

Dataset:
TOFU forget01

Initial checkpoint:

/home/research/open-unlearning/saves/unlearn/tofu_Llama-3.2-1B-Instruct_forget01_RMU_test

The Step-0 RMU model showed strong suppression of forget-set behavior but
Model Utility = 0 under the unified TOFU evaluation.

---

## 3. Relearning Attack

Attack type:
ordinary supervised fine-tuning on the TOFU forget01 QA data.

This is NOT an unlearning objective.

The attack directly reintroduces the original forget-set training data and
therefore represents a strong-access relearning attack.

Important limitation:

Successful recovery in this setting does not prove that RMU retained the
original information internally, because the model is explicitly exposed
again to the forgotten examples.

---

## 4. Training Protocol

A single continuous relearning trajectory was used.

Snapshots:

- Step 0: original RMU checkpoint
- Step 1
- Step 5
- Step 10
- Step 20
- Step 50

The Step 1/5/10/20/50 snapshots therefore belong to the same optimizer and
scheduler trajectory rather than independent retraining runs.

Main training settings:

- learning rate: 1e-5
- batch size: 1
- gradient accumulation: 4
- weight decay: 0.01
- gradient checkpointing: enabled
- maximum optimizer steps: 50
- attention implementation: SDPA
- optimizer: paged_adamw_32bit
- scheduler: linear decay, no explicit warmup
- seed: 0
- BF16: enabled

Approximate epoch mapping:

- Step 5: 0.5 epoch
- Step 10: 1 epoch
- Step 20: 2 epochs
- Step 50: 5 epochs

---

## 5. Recovery Metrics

Three official OpenUnlearning TOFU metrics were used:

1. Forget Q/A Probability
2. Forget Q/A ROUGE
3. Extraction Strength

Step 0 values come from the complete Experiment 004 TOFU evaluation.

Step 1/5/10/20/50 values come from the lightweight recovery-screen
evaluator using the same official metric implementations.

---

## 6. Results

| Relearning Steps | Forget Q/A Prob | Forget Q/A ROUGE | Extraction Strength |
|---:|---:|---:|---:|
| 0  | 0.0000229001 | 0.0136615 | 0.0290594 |
| 1  | 0.0002258897 | 0.0556710 | 0.0290594 |
| 5  | 0.0015385628 | 0.0225540 | 0.0290594 |
| 10 | 0.0062427521 | 0.0174940 | 0.0290594 |
| 20 | 0.0219810486 | 0.2502909 | 0.0290594 |
| 50 | 0.0410003662 | 0.2554944 | 0.0297004 |

---

## 7. Main Observations

### 7.1 Target-answer probability recovers rapidly

Forget Q/A Probability increased from approximately:

2.29e-5 at Step 0

to:

4.10e-2 at Step 50.

This corresponds to approximately a 1790x increase relative to the very small
Step-0 value.

Because the baseline is extremely small, absolute metric values should be
reported together with relative changes.

### 7.2 Free-generation recovery is delayed and non-monotonic

Forget Q/A ROUGE did not recover monotonically during the early trajectory.

It increased at Step 1, decreased again at Steps 5 and 10, and then showed a
large increase between Steps 10 and 20:

Step 10: 0.01749
Step 20: 0.25029
Step 50: 0.25549

This suggests that target-answer likelihood and free-generation behavior can
recover at different rates under this setting.

### 7.3 Extraction Strength is comparatively insensitive

Extraction Strength remained exactly:

0.0290594082

from Step 0 through Step 20.

At Step 50 it changed only slightly to:

0.0297004339.

Thus the three recovery metrics capture different aspects of post-unlearning
behavior and should not be treated as interchangeable.

---

## 8. Interpretation

Under the current TOFU forget01 setting, knowledge behavior suppressed by RMU
is empirically recoverable under subsequent supervised relearning.

The recovery appears staged:

1. target-answer probability begins recovering early;
2. free-generation ROUGE shows delayed but substantial recovery;
3. extraction strength remains comparatively insensitive over the same
   trajectory.

This provides evidence that low post-unlearning forget metrics do not by
themselves imply resistance to subsequent recovery.

---

## 9. What This Experiment Does NOT Prove

This experiment does NOT establish that:

- RMU failed to erase a specific latent representation;
- the original memory necessarily remained intact after unlearning;
- Step-50 recovery is entirely retrieval of residual memory rather than
  ordinary re-learning;
- the same behavior necessarily occurs in clinical or patient-level data;
- RMU is globally inferior or superior to other unlearning methods.

The current attack directly provides the original forget-set QA examples.

Therefore this experiment should be treated as a mechanism/recoverability
pilot rather than the final evidence for latent-memory persistence.

---

## 10. Next Research Question

The stronger next question is:

Can forgotten target information recover when the attacker does NOT directly
reintroduce the original forget-set QA pairs?

Candidate recovery channels include:

- paraphrased evidence;
- partial evidence;
- semantically related records;
- same-entity correlated records;
- ultimately, same-patient correlated clinical records.

Recovery through such indirect channels would provide substantially stronger
evidence about residual/distributed knowledge and is more relevant to the
planned patient-level medical unlearning setting.

---

## 11. Artifacts

Trajectory table:

results/recovery_trajectory.csv

Figures:

figures/01_relearning_probability.png
figures/02_relearning_rouge.png
figures/03_relearning_extraction.png

Formal relearning snapshots:

relearn-step-1
relearn-step-5
relearn-step-10
relearn-step-20
relearn-step-50

The earlier independent Step-1 feasibility probe is not used as a formal
trajectory point. The formal Step-1 point comes from the continuous 50-step
trajectory.

---

## 12. Step-50 Full TOFU Utility Control

A complete TOFU evaluation was additionally performed on the formal
continuous-trajectory Step-50 checkpoint.

The purpose was to test whether the observed forget-set recovery could be
explained simply by broad recovery of the RMU-damaged model.

### Step-0 vs Step-50

| Metric | RMU Step 0 | Relearning Step 50 |
|---|---:|---:|
| Forget Q/A Probability | 0.0000229001 | 0.0410003662 |
| Forget Q/A ROUGE | 0.0136615 | 0.2554944 |
| Extraction Strength | 0.0290594 | 0.0297004 |
| Forget Truth Ratio | 0.7866962 | 0.6312248 |
| Forget Quality | 0.0286031 | 0.2656871 |
| Model Utility | 0.0 | 0.0 |
| PrivLeak | 22.2949 | -98.6920 |

### Interpretation

After 50 cumulative relearning optimizer steps, target-answer probability
and free-generation ROUGE recovered substantially, while aggregate TOFU
Model Utility remained 0.0.

Therefore, under this experimental setting, the observed target-behavior
recovery is not accompanied by recovery of the aggregate TOFU utility metric.

This weakens the simple explanation that the recovery trajectory is merely
the consequence of broad model-utility repair.

However, this result does NOT establish latent-memory persistence.

The relearning attack directly reintroduced the original forget-set QA
examples. The observed recovery may therefore reflect rapid ordinary
re-learning, residual knowledge reactivation, or a combination of both.

A stronger test must remove direct access to the original target QA examples
and evaluate recovery through indirect evidence.

Forget Quality and PrivLeak are retained as reported benchmark outputs but
are not used as standalone evidence of memory deletion or recovery.
PrivLeak is interpreted cautiously because of the previously observed
Retain99 reference warning.

### Full evaluation artifact

Step-50 full TOFU summary:

/home/research/open-unlearning/saves/train/tofu_Llama-3.2-1B-Instruct_forget01_RMU_relearn_50step_continuous/relearn-step-50/evals/TOFU_SUMMARY.json
