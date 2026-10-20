# Experiment 005 — Relearning 攻击 协议 v1

## 研究问题

After an 机器遗忘 method strongly suppresses the 目标 behavior, can the
forgotten 知识 be rapidly recovered through a small amount 的 subsequent
训练?

目的 是到distinguish:

1. observable 遗忘 / 行为抑制
2. resistance到知识 恢复

本实验 does NOT assume that 成功 恢复 proves a specific
latent-memory 机制. It measures empirical recoverability.

---

## Stage A — 试验 方法

The first 试验 攻击 will use:

    RMU

Base unlearned checkpoint:

    /home/research/open-unlearning/saves/unlearn/
    tofu_Llama-3.2-1B-Instruct_forget01_RMU_test

模型:

    Llama-3.2-1B-Instruct

数据集:

    TOFU forget01

Reason用于using RMU first:

RMU 是 a representation-level 机器遗忘 baseline already 已完成 in
Experiment 004. It因此provides a useful first case用于testing whether
强 机器遗忘后 行为抑制 remains recoverable.

This choice 是用于the 试验 experiment 仅 和 是 not a claim that RMU is
better 或 worse比the other baselines.

---

## Stage B — 攻击

The 攻击 starts 来自 the already-unlearned RMU checkpoint.

The attacker performs ordinary supervised fine-tuning using forget-set
question-answer 训练 examples.

The 攻击 objective 是 NOT another 机器遗忘 objective.

Conceptually:

    RMU checkpoint
        +
    small amount 的 forget-data supervised 训练
        ->
    attacked checkpoint

该实验 asks how quickly previously suppressed 目标 behavior returns.

---

## Stage C — Relearning 检查点

Evaluate 恢复 at:

    step 0
    step 1
    step 5
    step 10
    step 20
    step 50

步骤 0 是 the original RMU checkpoint 来自 Experiment 004.

No additional 训练 是 performed用于step 0.

The remaining checkpoints 是 produced 来自 the 相同 RMU starting checkpoint
under the 相同 再学习 配置.

---

## Stage D — Primary 恢复 指标

At every checkpoint, 记录 at least:

    Forget 问答概率
    Forget 问答 ROUGE
    提取强度
    模型 Utility

The main object 的 analysis 是 the 恢复 trajectory rather比仅 the
final checkpoint.

Example:

    再学习 step -> 遗忘 metric

This produces a 恢复 curve.

---

## Stage E — Utility Constraint

恢复 的 forget-set performance alone 是 insufficient.

模型 Utility 必须 also be monitored so that apparent 恢复 can be
distinguished 来自 general model 不稳定性 或 degeneration.

---

## Stage F — 解释

If 目标 performance rapidly increases 之后 仅 a small number 的 supervised
updates, the correct conclusion is:

    the 机器遗忘后 behavior 是 empirically recoverable under this
    再学习 攻击.

This alone does NOT prove:

    the 精确 forgotten representation 为 preserved unchanged,
    a specific latent-memory 机制 exists,
    或 no genuine parameter-level modification occurred.

Additional representation-level analysis 是 required用于such claims.

Likewise, 失败到recover under one 攻击 does NOT prove 完成 deletion.

It 仅 establishes resistance到the tested 攻击 配置.

---

## Stage G — Later Extension

After the RMU 试验 protocol 是 validated, apply the 相同 攻击 protocol to:

    GradAscent
    GradDiff
    SimNPO
    RMU

using 匹配:

    starting conditions
    再学习 data
    optimizer 配置
    学习率
    number 的 steps
    评估 protocol

This will allow 比较 的 恢复 trajectories 跨 机器遗忘 methods.

---

## Stage H — Long-Term Medical Extension

The later 临床 version will replace generic TOFU 目标 知识 使用
patient-level 记录.

A future threat model will test whether:

    same-patient correlated 记录

can act作为a 恢复 channel 之后 patient-level 机器遗忘.

That 医学 extension 是 outside Experiment 005 v1.
