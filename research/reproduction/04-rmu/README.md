# Experiment 004 — RMU on TOFU forget01

## 1. Purpose

This experiment evaluates the official OpenUnlearning RMU baseline under the same
TOFU forget01 setting used in Experiments 001–003.

The main goals are:

1. Verify whether RMU is feasible on a single RTX 4070 SUPER 12GB GPU.
2. Evaluate forgetting effectiveness under the unified TOFU protocol.
3. Measure retained model utility.
4. Inspect qualitative generation failures.
5. Establish a representation-level unlearning baseline for later latent-memory
   and relearning experiments.

This experiment is a generic LLM unlearning baseline experiment.
It is NOT yet a clinical or medical unlearning experiment.

---

## 2. Repository Version

OpenUnlearning repository:

    /home/research/open-unlearning

Exact git commit used in this experiment is stored in:

    code/git_commit.txt

Relevant source/configuration snapshots:

    code/source/rmu.py
    code/configs/RMU.yaml
    code/configs/single_gpu.yaml

---

## 3. Hardware

GPU:

    NVIDIA GeForce RTX 4070 SUPER

Available VRAM:

    approximately 12 GB

A dedicated one-step RMU memory probe was performed before formal training.

Observed peak GPU memory usage during the probe:

    approximately 7712 MiB

Therefore, the official RMU configuration was feasible on this GPU without
introducing a memory-saving modification to the RMU algorithm.

Memory probe log:

    rmu_memory_probe.csv

Probe script:

    scripts/00_rmu_memory_probe.sh

---

## 4. Model and Dataset

Model:

    Llama-3.2-1B-Instruct

OpenUnlearning pretrained TOFU checkpoint:

    open-unlearning/tofu_Llama-3.2-1B-Instruct_full

Dataset/evaluation setting:

    TOFU
    forget_split = forget01
    retain_split = retain99
    holdout_split = holdout01

The same Retain99 reference evaluation used in previous experiments was reused
for comparison.

---

## 5. RMU Objective

The OpenUnlearning RMU implementation applies a representation-level objective.

The configured module is:

    model.layers.7

For forget examples, RMU pushes the selected hidden representations toward a
random control vector.

For retain examples, the EMBED_DIFF retain objective penalizes deviation between
the current model representation and the reference model representation.

Conceptually:

    L_RMU = gamma * L_forget + alpha * L_retain

with the experiment configuration:

    gamma = 1.0
    alpha = 1
    steering_coeff = 2
    retain_loss_type = EMBED_DIFF
    module_regex = model\.layers\.7

Important implementation detail:

The loss is measured using representations at layer 7, but the configuration
contains:

    trainable_params_regex:
      - .*

Therefore, this experiment does NOT update only layer 7.

The optimizer includes all model parameters matched by the configuration.
The inspected model contained approximately:

    1,235,814,400 parameters

Thus, "layer-7 representation loss" and "only training layer 7" must not be
treated as equivalent descriptions.

---

## 6. Training Configuration

Formal training script:

    scripts/01_rmu_train.sh

Important settings:

    batch size = 1
    gradient accumulation = 4
    gradient checkpointing = true
    attention implementation = SDPA
    evaluation during training = disabled
    max steps = 100
    epochs = 10

Formal checkpoint:

    /home/research/open-unlearning/saves/unlearn/
    tofu_Llama-3.2-1B-Instruct_forget01_RMU_test

The large model checkpoint is intentionally NOT duplicated inside this
reproduction directory.

Training completed successfully without OOM.

Training runtime:

    364.441 seconds
    approximately 6.07 minutes

Final training state:

    global_step = 100
    epoch = 10

Twenty logged loss records were obtained.

Training loss:

    first logged loss = 0.0533
    final logged loss = 0.0162
    minimum logged loss = 0.0162

The decrease in training loss indicates optimization of the RMU training
objective. It does NOT by itself demonstrate successful high-quality unlearning.

---

## 7. Evaluation

Evaluation script:

    scripts/02_rmu_eval.sh

Evaluation uses:

    TOFU forget01
    TOFU holdout01
    eval.tofu.batch_size = 1
    SDPA
    shared Retain99 reference logs

Fine-grained results:

    results/rmu_forget01/TOFU_EVAL.json

Aggregated results:

    results/rmu_forget01/TOFU_SUMMARY.json

RMU summary:

    extraction_strength = 0.02905940823391865
    forget_Q_A_Prob = 2.2900104522705077e-05
    forget_Q_A_ROUGE = 0.013661529357140503
    forget_quality = 0.02860307028023343
    forget_truth_ratio = 0.7866961809766119
    model_utility = 0.0
    privleak = 22.294887034997405

---

## 8. Five-Method Comparison

The unified comparison includes:

    Retain99
    GradAscent
    GradDiff
    SimNPO
    RMU

Selected metrics:

| Metric | Retain99 | GradAscent | GradDiff | SimNPO | RMU |
|---|---:|---:|---:|---:|---:|
| Forget Q/A Prob | 0.1656097412 | 0 | 7.636845e-09 | 0.0177410126 | 2.290010e-05 |
| Forget Q/A ROUGE | 0.4121097991 | 0 | 0.0032608696 | 0.1629437052 | 0.0136615294 |
| Forget Truth Ratio | 0.6515836653 | ~0 | 0.0002510855 | 0.7764549262 | 0.7866961810 |
| Model Utility | 0.5988637092 | 0 | 0 | 0.0209650114 | 0 |
| Extraction Strength | 0.0692820568 | 0.0290594082 | 0.0290594082 | 0.0297004339 | 0.0290594082 |

Forget Quality and PrivLeak are retained in the raw result files but are not
placed on the same linear-scale comparison figure.

The Retain99 PrivLeak/reference warning from previous evaluation must be
considered before making direct absolute privacy comparisons.

---

## 9. Main Quantitative Observation

Under this unified experimental setting, RMU strongly suppresses target-answer
behavior:

    Forget Q/A Prob ≈ 2.29e-05
    Forget Q/A ROUGE ≈ 0.01366

However:

    Model Utility = 0.0

Therefore, the low forget-set output metrics cannot be interpreted by themselves
as successful selective unlearning.

Under this setting, strong target suppression is accompanied by severe loss of
overall evaluated utility.

---

## 10. Qualitative Analysis

All 40 forget examples were exported to:

    results/rmu_forget01/tables/forget_examples.csv

For visualization, the three examples with the largest decrease in ROUGE-L F1
from Retain99 to RMU were selected.

These examples are deliberately selected failure cases and are NOT a random
sample. They demonstrate the existence of degeneration but do not estimate its
prevalence across all forget examples.

Selected examples:

    sample 1:
        Retain99 ROUGE-L F1 = 1.0
        RMU ROUGE-L F1 = 0.0

    sample 0:
        Retain99 ROUGE-L F1 = 0.7142857143
        RMU ROUGE-L F1 = 0.0

    sample 2:
        Retain99 ROUGE-L F1 = 0.7142857143
        RMU ROUGE-L F1 = 0.0

The selected RMU generations show severe token-level repetitive degeneration,
including repeated characters/tokens such as:

    b b b ...
    222222 ...
    D D D ...
    z z z ...

Thus, in these selected failure cases, low ROUGE is associated with generation
breakdown rather than a clean, fluent answer that simply omits the forgotten
knowledge.

---

## 11. Interpretation

The experiment supports the following limited conclusion:

Under the current TOFU forget01 + Llama-3.2-1B-Instruct configuration, RMU
successfully optimizes its representation-level training objective and strongly
suppresses target-answer behavior, but this is accompanied by complete collapse
of the reported model utility and severe repetitive degeneration in selected
high-ROUGE-drop failure cases.

Therefore:

    low forget probability
    + low forget ROUGE

must not automatically be interpreted as:

    successful high-quality selective unlearning.

The experiment does NOT establish that latent memory has been erased.

It also does NOT establish resistance to relearning or recovery attacks.

Those questions require separate latent-representation and relearning
experiments.

---

## 12. Generated Artifacts

Figures:

    results/rmu_forget01/figures/01_training_loss.png
    results/rmu_forget01/figures/02_metrics_comparison.png
    results/rmu_forget01/figures/03_forget_examples.png

Tables:

    results/rmu_forget01/tables/training_loss.csv
    results/rmu_forget01/tables/metrics_comparison.csv
    results/rmu_forget01/tables/forget_examples.csv

Evaluation:

    results/rmu_forget01/TOFU_EVAL.json
    results/rmu_forget01/TOFU_SUMMARY.json

Scripts:

    scripts/00_rmu_memory_probe.sh
    scripts/01_rmu_train.sh
    scripts/02_rmu_eval.sh

---

## 13. Status

Experiment 004 experimental execution is complete.

Final archival integrity should be checked before marking the experiment SEALED.
