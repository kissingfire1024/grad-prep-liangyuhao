# Experiment 005 — RMU Relearning 恢复

## 1. 研究问题

After RMU suppresses the 目标 forget-set behavior, how rapidly can the
遗忘目标 知识 become recoverable under subsequent ordinary
supervised fine-tuning?

本实验 measures empirical recoverability. It does not by itself
establish whether 恢复 originates 来自 residual latent 知识,
ordinary re-learning 来自 the supplied 遗忘 data, 或 a combination 的 both.

---

## 2. Base Unlearned 模型

方法: RMU

模型:
Llama-3.2-1B-Instruct

数据集:
TOFU forget01

Initial checkpoint:

/home/research/open-unlearning/saves/unlearn/tofu_Llama-3.2-1B-Instruct_forget01_RMU_test

The Step-0 RMU model showed 强 suppression 的 forget-set behavior but
模型 Utility = 0 under the unified TOFU 评估.

---

## 3. Relearning 攻击

攻击 type:
ordinary supervised fine-tuning在the TOFU forget01 QA data.

This 是 NOT an 机器遗忘 objective.

The 攻击 directly reintroduces the original forget-set 训练 data and
therefore represents a strong-access 再学习 攻击.

Important limitation:

Successful 恢复在this setting 不能证明 that RMU retained the
original information internally,因为模型 是 explicitly exposed
again到the forgotten examples.

---

## 4. 训练 协议

A single continuous 再学习 trajectory 为 used.

Snapshots:

- 步骤 0: original RMU checkpoint
- 步骤 1
- 步骤 5
- 步骤 10
- 步骤 20
- 步骤 50

The 步骤 1/5/10/20/50 snapshots因此belong到the 相同 optimizer and
scheduler trajectory rather比independent retraining runs.

Main 训练 settings:

- 学习率: 1e-5
- batch size: 1
- 梯度累积: 4
- 权重衰减: 0.01
- 梯度检查点: enabled
- maximum 优化器步数: 50
- attention 实现: SDPA
- optimizer: paged_adamw_32bit
- scheduler: linear decay, no 显式 warmup
- 随机种子: 0
- BF16: enabled

Approximate 轮次 mapping:

- 步骤 5: 0.5 轮次
- 步骤 10: 1 轮次
- 步骤 20: 2 epochs
- 步骤 50: 5 epochs

---

## 5. 恢复 指标

Three 官方 OpenUnlearning TOFU metrics 为 used:

1. Forget 问答概率
2. Forget 问答 ROUGE
3. 提取强度

步骤 0 values come 来自 the 完成 Experiment 004 TOFU 评估.

步骤 1/5/10/20/50 values come 来自 the lightweight recovery-screen
evaluator using the 相同 官方 metric implementations.

---

## 6. 结果

| Relearning 步骤 | Forget Q/A Prob | Forget 问答 ROUGE | 提取强度 |
|---:|---:|---:|---:|
| 0  | 0.0000229001 | 0.0136615 | 0.0290594 |
| 1  | 0.0002258897 | 0.0556710 | 0.0290594 |
| 5  | 0.0015385628 | 0.0225540 | 0.0290594 |
| 10 | 0.0062427521 | 0.0174940 | 0.0290594 |
| 20 | 0.0219810486 | 0.2502909 | 0.0290594 |
| 50 | 0.0410003662 | 0.2554944 | 0.0297004 |

---

## 7. Main Observations

### 7.1 Target-答案概率 recovers rapidly

Forget 问答概率 增加 来自 approximately:

2.29e-5 at 步骤 0

to:

4.10e-2 at 步骤 50.

This corresponds到approximately a 1790x 增加 相对于 the very small
Step-0 value.

Because the baseline 是 extremely small, absolute metric values 应当 be
reported together 使用 relative changes.

### 7.2 Free-generation 恢复 是 delayed 和 non-monotonic

Forget 问答 ROUGE did not recover monotonically during the early trajectory.

It 增加 at 步骤 1, 下降 again at 步骤 5 和 10, 和 then showed a
large 增加 之间 步骤 10 和 20:

步骤 10: 0.01749
步骤 20: 0.25029
步骤 50: 0.25549

This suggests that target-answer likelihood 和 free-generation behavior can
recover at 不同 rates under this setting.

### 7.3 提取强度 是 comparatively insensitive

提取强度 remained exactly:

0.0290594082

来自 步骤 0 through 步骤 20.

At 步骤 50 it changed 仅 slightly to:

0.0297004339.

Thus the three 恢复 metrics capture 不同 aspects 的 机器遗忘后
behavior 和 应当 not be treated作为interchangeable.

---

## 8. 解释

Under the current TOFU forget01 setting, 知识 behavior suppressed by RMU
is empirically recoverable under subsequent supervised 再学习.

The 恢复 appears staged:

1. target-答案概率 begins recovering early;
2. free-generation ROUGE shows delayed但substantial 恢复;
3. extraction strength remains comparatively insensitive over the 相同
   trajectory.

This provides 证据 that low 机器遗忘后 遗忘 metrics do not by
themselves imply resistance到subsequent 恢复.

---

## 9. What This Experiment Does NOT Prove

本实验 does NOT establish that:

- RMU 失败到erase a specific latent representation;
- the original 记忆 necessarily remained intact 之后 机器遗忘;
- Step-50 恢复 是 entirely retrieval 的 residual 记忆 rather than
  ordinary re-learning;
- the 相同 behavior necessarily occurs在临床 或 patient-level data;
- RMU 是 globally inferior 或 superior到other 机器遗忘 methods.

The current 攻击 directly provides the original forget-set QA examples.

Therefore 本实验 应当 be treated作为a 机制/recoverability
试验 rather比the final 证据用于latent-memory persistence.

---

## 10. Next 研究问题

The 更强 next 问题 is:

Can 遗忘目标 information recover when the attacker does NOT directly
reintroduce the original forget-set QA pairs?

候选 恢复 channels 纳入:

- paraphrased 证据;
- partial 证据;
- semantically related 记录;
- 同实体 correlated 记录;
- ultimately, same-patient correlated 临床 记录.

恢复 through such indirect channels would provide substantially 更强
证据 about residual/distributed 知识 和 是 more relevant到the
planned patient-level 医学 机器遗忘 setting.

---

## 11. 实验产物

Trajectory table:

results/recovery_trajectory.csv

Figures:

figures/01_relearning_probability.png
figures/02_relearning_rouge.png
figures/03_relearning_extraction.png

正式 再学习 snapshots:

relearn-step-1
relearn-step-5
relearn-step-10
relearn-step-20
relearn-step-50

The earlier independent Step-1 feasibility probe 是 not used作为a 正式
trajectory point. The 正式 Step-1 point comes 来自 the continuous 50-step
trajectory.

---

## 12. Step-50 Full TOFU Utility 对照

A 完成 TOFU 评估 为 additionally performed在the 正式
continuous-trajectory Step-50 checkpoint.

目的 为到test whether the observed forget-set 恢复 could be
explained simply by broad 恢复 的 the RMU-damaged model.

### Step-0 vs Step-50

| 指标 | RMU 步骤 0 | Relearning 步骤 50 |
|---|---:|---:|
| Forget 问答概率 | 0.0000229001 | 0.0410003662 |
| Forget 问答 ROUGE | 0.0136615 | 0.2554944 |
| 提取强度 | 0.0290594 | 0.0297004 |
| Forget 真实性比率 | 0.7866962 | 0.6312248 |
| 遗忘质量 | 0.0286031 | 0.2656871 |
| 模型 Utility | 0.0 | 0.0 |
| PrivLeak | 22.2949 | -98.6920 |

### 解释

After 50 cumulative 再学习 优化器步数, target-答案概率
and free-generation ROUGE recovered substantially,而aggregate TOFU
模型 Utility remained 0.0.

Therefore, 在当前实验设置下, the observed target-behavior
恢复 是 not accompanied by 恢复 的 the aggregate TOFU utility metric.

This weakens the simple explanation that the 恢复 trajectory 是 merely
the consequence 的 broad model-utility repair.

However, this result does NOT establish latent-memory persistence.

The 再学习 攻击 directly reintroduced the original forget-set QA
examples. The observed 恢复 可能因此reflect rapid ordinary
re-learning, residual 知识 reactivation, 或 a combination 的 both.

A 更强 test 必须 remove direct access到the original 目标 QA examples
and evaluate 恢复 through indirect 证据.

遗忘质量 和 PrivLeak 是 retained作为reported benchmark outputs but
are not used作为standalone 证据 的 记忆 deletion 或 恢复.
PrivLeak 是 interpreted cautiously因为的 the previously observed
Retain99 reference 警告.

### Full 评估 artifact

Step-50 full TOFU summary:

/home/research/open-unlearning/saves/train/tofu_Llama-3.2-1B-Instruct_forget01_RMU_relearn_50step_continuous/relearn-step-50/evals/TOFU_SUMMARY.json
