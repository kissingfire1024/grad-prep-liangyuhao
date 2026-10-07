# Experiment 004 — RMU在TOFU forget01

## 1. 目的

本实验 evaluates the 官方 OpenUnlearning RMU baseline under the 相同
TOFU forget01 setting used在Experiments 001–003.

The main goals are:

1. Verify whether RMU 是 feasible在a single RTX 4070 SUPER 12GB GPU.
2. Evaluate 遗忘 effectiveness under the unified TOFU protocol.
3. Measure retained 模型效用.
4. Inspect qualitative generation failures.
5. Establish a representation-level 机器遗忘 baseline用于later latent-memory
   和 再学习 experiments.

本实验 是 a generic LLM 机器遗忘 baseline experiment.
It 是 NOT yet a 临床 或 医学 机器遗忘 experiment.

---

## 2. Repository Version

OpenUnlearning repository:

    /home/research/open-unlearning

精确 git commit used在本实验 是 stored in:

    code/git_commit.txt

Relevant source/配置 snapshots:

    code/source/rmu.py
    code/configs/RMU.yaml
    code/configs/single_gpu.yaml

---

## 3. 硬件

GPU:

    NVIDIA GeForce RTX 4070 SUPER

Available VRAM:

    approximately 12 GB

A dedicated one-step RMU 记忆 probe 为 performed 之前 正式 训练.

Observed peak GPU 记忆 usage during the probe:

    approximately 7712 MiB

Therefore, the 官方 RMU 配置 为 feasible在this GPU 不使用
introducing a memory-saving modification到the RMU algorithm.

Memory probe log:

    rmu_memory_probe.csv

Probe script:

    scripts/00_rmu_memory_probe.sh

---

## 4. 模型 和 数据集

模型:

    Llama-3.2-1B-Instruct

OpenUnlearning pretrained TOFU checkpoint:

    open-unlearning/tofu_Llama-3.2-1B-Instruct_full

数据集/评估 setting:

    TOFU
    forget_split = forget01
    retain_split = retain99
    holdout_split = holdout01

The 相同 Retain99 reference 评估 used在previous experiments 为 重复使用
for 比较.

---

## 5. RMU 目标

The OpenUnlearning RMU 实现 applies a representation-level objective.

The configured module is:

    model.layers.7

For 遗忘 examples, RMU pushes the 已选择 hidden representations toward a
random 对照 vector.

For 保留 examples, the EMBED_DIFF 保留 objective penalizes deviation 之间
the current model representation 和 the 参考模型 representation.

Conceptually:

    L_RMU = gamma * L_forget + alpha * L_retain

使用 该实验 配置:

    gamma = 1.0
    alpha = 1
    steering_coeff = 2
    retain_loss_type = EMBED_DIFF
    module_regex = model\.layers\.7

Important 实现 detail:

The 损失 是 measured using representations at layer 7,但the 配置
包含:

    trainable_params_regex:
      - .*

Therefore, 本实验 does NOT update 仅 layer 7.

The optimizer includes 全部 model parameters 匹配 by the 配置.
The inspected model contained approximately:

    1,235,814,400 parameters

Thus, "layer-7 representation 损失" 和 "仅 训练 layer 7" 不得 be
treated作为equivalent descriptions.

---

## 6. 训练配置

正式 训练 script:

    scripts/01_rmu_train.sh

Important settings:

    batch size = 1
    梯度累积 = 4
    梯度检查点 = true
    attention 实现 = SDPA
    评估 during 训练 = disabled
    max steps = 100
    epochs = 10

正式 checkpoint:

    /home/research/open-unlearning/saves/unlearn/
    tofu_Llama-3.2-1B-Instruct_forget01_RMU_test

The large model checkpoint 是 intentionally NOT duplicated inside this
reproduction directory.

训练 已完成 successfully 不使用 OOM.

训练 运行时间:

    364.441 seconds
    approximately 6.07 minutes

Final 训练 state:

    global_step = 100
    轮次 = 10

Twenty logged 损失 记录 为 obtained.

训练 损失:

    first logged 损失 = 0.0533
    final logged 损失 = 0.0162
    minimum logged 损失 = 0.0162

The 下降在训练 损失 indicates optimization 的 the RMU 训练
objective. It does NOT by itself demonstrate 成功 high-quality 机器遗忘.

---

## 7. 评估

评估 script:

    scripts/02_rmu_eval.sh

评估 uses:

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

## 8. Five-Method 比较

The unified 比较 includes:

    Retain99
    GradAscent
    GradDiff
    SimNPO
    RMU

Selected metrics:

| 指标 | Retain99 | GradAscent | GradDiff | SimNPO | RMU |
|---|---:|---:|---:|---:|---:|
| Forget Q/A Prob | 0.1656097412 | 0 | 7.636845e-09 | 0.0177410126 | 2.290010e-05 |
| Forget 问答 ROUGE | 0.4121097991 | 0 | 0.0032608696 | 0.1629437052 | 0.0136615294 |
| Forget 真实性比率 | 0.6515836653 | ~0 | 0.0002510855 | 0.7764549262 | 0.7866961810 |
| 模型 Utility | 0.5988637092 | 0 | 0 | 0.0209650114 | 0 |
| 提取强度 | 0.0692820568 | 0.0290594082 | 0.0290594082 | 0.0297004339 | 0.0290594082 |

遗忘质量 和 PrivLeak 是 retained在the raw result files但是 not
placed在the 相同 linear-scale 比较 figure.

The Retain99 PrivLeak/reference 警告 来自 previous 评估 必须 be
considered 之前 making direct absolute 隐私 comparisons.

---

## 9. Main Quantitative Observation

Under this unified experimental setting, RMU strongly suppresses target-answer
behavior:

    Forget Q/A Prob ≈ 2.29e-05
    Forget 问答 ROUGE ≈ 0.01366

However:

    模型 Utility = 0.0

Therefore, the low forget-set output metrics cannot be interpreted by themselves
as 成功 selective 机器遗忘.

Under this setting, 强 目标 suppression 是 accompanied by severe 损失 of
overall evaluated utility.

---

## 10. Qualitative 分析

All 40 遗忘 examples 为 exported to:

    results/rmu_forget01/tables/forget_examples.csv

For visualization, the three examples 使用 the largest 下降在ROUGE-L F1
来自 Retain99到RMU 为 已选择.

These examples 是 deliberately 已选择 失败 cases 和 是 NOT a random
sample. They demonstrate the existence 的 degeneration但do not estimate its
prevalence 跨 全部 遗忘 examples.

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

The 已选择 RMU generations show severe token-level repetitive degeneration,
including repeated characters/tokens such as:

    b b b ...
    222222 ...
    D D D ...
    z z z ...

Thus,在these 已选择 失败 cases, low ROUGE 是 associated 使用 generation
breakdown rather比a clean, fluent 答案 that simply omits the forgotten
知识.

---

## 11. 解释

该实验 支持 the following limited conclusion:

Under the current TOFU forget01 + Llama-3.2-1B-Instruct 配置, RMU
successfully optimizes its representation-level 训练 objective 和 strongly
suppresses target-answer behavior,但this 是 accompanied by 完成 collapse
of the reported 模型效用 和 severe repetitive degeneration在已选择
high-ROUGE-drop 失败 cases.

Therefore:

    low 遗忘 概率
    + low 遗忘 ROUGE

不得 automatically be interpreted as:

    成功 high-quality selective 机器遗忘.

该实验 does NOT establish that 潜在记忆 has been erased.

It also does NOT establish resistance到再学习 或 恢复 attacks.

Those questions require separate latent-representation 和 再学习
experiments.

---

## 12. Generated 实验产物

Figures:

    results/rmu_forget01/figures/01_training_loss.png
    results/rmu_forget01/figures/02_metrics_comparison.png
    results/rmu_forget01/figures/03_forget_examples.png

Tables:

    results/rmu_forget01/tables/training_loss.csv
    results/rmu_forget01/tables/metrics_comparison.csv
    results/rmu_forget01/tables/forget_examples.csv

评估:

    results/rmu_forget01/TOFU_EVAL.json
    results/rmu_forget01/TOFU_SUMMARY.json

Scripts:

    scripts/00_rmu_memory_probe.sh
    scripts/01_rmu_train.sh
    scripts/02_rmu_eval.sh

---

## 13. 状态

Experiment 004 experimental execution 是 完成.

Final archival integrity 应当 be checked 之前 marking 该实验 已封存.
