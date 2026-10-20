# Experiment 009 — Multi-Entity Statistical Validation

## Final 状态

**已封存**

Experiment 009 是 a frozen multi-entity validation 的 the
quasi-identifier-associated 恢复 signal observed在Experiment 008.

The 正式 恢复 outcomes 为 evaluated 仅 之后 the 恢复
训练 protocol, datasets, controls, heldout targets, 和 analysis
plan had been frozen.

No post-outcome 实体 replacement, 证据 replacement, 对照
rematching, training-step adjustment, 或 hyperparameter adjustment was
performed.

---

## 1. 研究问题

Experiment 008 produced a 初步 quasi-identifier-associated
target-likelihood 恢复 signal using 仅 two 目标 实体.

Its 正式 Quasi/对照 均值 概率 比率 为 approximately:

**2.488x**

Experiment 009 tests whether that signal generalizes 跨 a larger
set 的 previously unused independent TOFU 作者 实体.

The 主要 统计 unit 是 the **实体**, not the QA example.

Validation cohort:

**18 independent 实体 (E01-E18)**

The Basil Mahfouz Al-Kuwaiti 和 Nikolai Abilov 实体 used during
Experiments 006-008 为 已排除 来自 this validation cohort.

---

## 2. Experimental Design

官方 TOFU `forget10` 包含 400 QA 记录 organized into
20 作者 blocks 的 20 QA 记录.

Experiment 009 uses the first 18 previously unused 作者 实体.

For every validation 实体:

- one identity 问题 是 held out作为the 恢复 目标;
- five frozen multi-attribute 准标识符 证据 记录 are
  used在the Quasi condition;
- five 无关 matched-control 记录 是 used在the 对照
  condition.

The heldout 目标 记录 是 never 已纳入在either 恢复
训练 dataset.

Total 正式 恢复 证据:

- Quasi: 90 QA 记录;
- 对照: 90 QA 记录;
- Heldout targets: 18 QA 记录.

---

## 3. RMU Step-0 Base 模型

正式 恢复 训练 begins independently 来自:

`/home/research/open-unlearning/saves/unlearn/tofu_Llama-3.2-1B-Instruct_forget10_RMU_exp009`

RMU forget10 训练:

- method: RMU;
- base model: Llama-3.2-1B-Instruct;
- 遗忘 split: forget10;
- 保留 split: retain90;
- 优化器步数: 100;
- batch size: 1;
- 梯度累积: 4;
- steering coefficient: 2;
- gamma: 1;
- alpha: 1;
- 保留 损失: EMBED_DIFF;
- representation module: model.layers.7;
- trainable parameter regex: `.*`;
- attention 实现: SDPA.

The 100-step RMU run 已完成 at 轮次 1.0.

RMU Step-0 均值 heldout target-答案概率:

**0.0001351965798272027**

All 18 validation targets had 更低 target-答案概率 之后 RMU
than在the corresponding full-model baseline.

---

## 4. 已冻结 Quasi 数据集

File:

`data/quasi_identifier_masked_v3.json`

SHA256:

`c60a2720057b0574e99b3bec5f18dedaf468fac24212b949cde26d74d1c0e8a6`

Properties:

- 18 实体;
- 5 记录/实体;
- 90 total 记录;
- 90 unique 记录;
- direct 目标 identities removed;
- direct birth/geography bridges 已排除;
- book-title proxies 已排除;
- synthetic identifiers 已排除.

Final status:

`EXP009_QUASI_IDENTIFIER_MASKED_V3_FROZEN`

---

## 5. 已冻结 Matched Unrelated 对照

File:

`data/control_masked_v3.json`

SHA256:

`edb0db3629f21a41d4d7fb91a531546784da1c7285a291e96e0e2e04c2c99511`

Properties:

- 官方 TOFU retain90 source 仅;
- 18 无关 source profiles;
- one 不同的 对照 档案 per validation 实体;
- 5 记录/实体;
- 90 total 记录;
- identity masking applied;
- heldout 目标 identities 已排除.

Final 审计:

90/90 通过.

Final status:

`EXP009_CONTROL_MASKED_V3_FROZEN`

---

## 6. 已冻结 Heldout Targets

File:

`data/heldout_targets_18entity_v1.json`

SHA256:

`1236a72d8ffb9ac5bb90fd04551ae43b57bc5ae9d2f4e679bc2ad61359195f6a`

Heldout 源索引:

`[0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340]`

Quasi/目标 source overlap:

**0**

对照/目标 source overlap:

**0**

Final status:

`EXP009_HELDOUT_TARGETS_18ENTITY_V1_FROZEN`

---

## 7. Token Exposure Matching

Final tokenizer exposure:

- Quasi: 3604 tokens;
- 对照: 3498 tokens;
- 对照/Quasi: 0.970588;
- global relative difference: approximately 2.94%.

Residual entity-level exposure mismatch greater比25% remained for:

- E06;
- E13;
- E17.

These 实体 为 retained在the 主要 analysis according到the
pre-outcome protocol.

No post-outcome rematching 为 performed.

---

## 8. 已冻结 恢复 训练 协议

File:

`notes/recovery_training_protocol_v1.md`

SHA256:

`73a29bf6871c9381ce94ec97ac0bd582d2ea41b9dc16eae93206ebf5f729831f`

状态:

`EXP009_RECOVERY_TRAINING_PROTOCOL_V1_FROZEN`

正式 配置用于**both** Quasi 和 对照:

- starting checkpoint: identical RMU forget10 Step-0;
- trainer: finetune;
- model: Llama-3.2-1B-Instruct;
- attention: SDPA;
- per-device train batch size: 1;
- per-device eval batch size: 1;
- 梯度累积: 4;
- effective examples/优化器步: 4;
- 学习率: 1e-5;
- 权重衰减: 0.01;
- 梯度检查点: true;
- logging steps: 1;
- 优化器步数: 20;
- training-time 评估: disabled;
- save strategy: no;
- 相同 default OpenUnlearning 随机种子;
- 相同 scheduler behavior.

Observed learning-rate trajectory用于both 正式 runs:

`1e-5 -> 5e-7`

Both trajectories 已完成:

- global step: 20;
- 轮次: 0.8888888888888888;
- no OOM;
- no NaN;
- no Inf.

正式 Quasi train 损失:

**6.538412976264953**

正式 对照 train 损失:

**6.346207809448242**

Both final model checkpoints contained one
2,471,645,608-byte `model.safetensors` file.

正式 trajectory symmetry 审计:

`EXP009_FORMAL_TRAJECTORIES_SYMMETRY_AUDIT_PASS`

---

## 9. 正式 评估

Both trajectories 为 evaluated using the 相同 frozen 18-target
evaluator 之前 any entity-level outcome analysis.

主要指标:

**heldout target-答案概率**

Auxiliary metric:

**ROUGE-L recall**

Aggregate 正式 results:

| Condition | Mean Target 概率 | ROUGE-L Recall |
|---|---:|---:|
| RMU Step-0 | 0.0001351965798 | N/A |
| Quasi 20-step | 0.00127251943 | 0.185069888 |
| 对照 20-step | 0.001223140293 | 0.1782797645 |

Ratio 的 算术均值 probabilities:

**1.040371x**

---

## 10. Entity-Level 正式 结果

| 实体 | P_RMU | P_Quasi | P_Control | R=Q/C | GQ=Q/RMU | GC=C/RMU |
|---|---:|---:|---:|---:|---:|---:|
| E01 | 2.014637e-05 | 0.00044441223 | 0.00068664551 | 0.6472 | 22.0592 | 34.0828 |
| E02 | 0.00012302399 | 0.001701355 | 0.0019989014 | 0.8511 | 13.8295 | 16.2481 |
| E03 | 0.00014877319 | 0.0010681152 | 0.0010681152 | 1.0000 | 7.1795 | 7.1795 |
| E04 | 8.4877014e-05 | 0.00070953369 | 0.00070953369 | 1.0000 | 8.3596 | 8.3596 |
| E05 | 0.0003452301 | 0.0019989014 | 0.0013656616 | 1.4637 | 5.7901 | 3.9558 |
| E06 | 4.529953e-05 | 0.0016479492 | 0.0022583008 | 0.7297 | 36.3789 | 49.8526 |
| E07 | 7.0095062e-05 | 0.00099945068 | 0.00091171265 | 1.0962 | 14.2585 | 13.0068 |
| E08 | 4.8398972e-05 | 0.0016021729 | 0.0013656616 | 1.1732 | 33.1034 | 28.2167 |
| E09 | 9.6321106e-05 | 0.0018157959 | 0.0012435913 | 1.4601 | 18.8515 | 12.9109 |
| E10 | 1.7762184e-05 | 0.00068664551 | 0.0011367798 | 0.6040 | 38.6577 | 64.0000 |
| E11 | 0.00013160706 | 0.0018692017 | 0.0017547607 | 1.0652 | 14.2029 | 13.3333 |
| E12 | 3.3140182e-05 | 0.00091171265 | 0.001701355 | 0.5359 | 27.5108 | 51.3381 |
| E13 | 4.2676926e-05 | 0.00051879883 | 0.00031471252 | 1.6485 | 12.1564 | 7.3743 |
| E14 | 0.00048828125 | 0.0014572144 | 0.00080490112 | 1.8104 | 2.9844 | 1.6484 |
| E15 | 4.8398972e-05 | 0.00094223022 | 0.00091171265 | 1.0335 | 19.4680 | 18.8374 |
| E16 | 6.1988831e-05 | 0.0015029907 | 0.0012054443 | 1.2468 | 24.2462 | 19.4462 |
| E17 | 0.00051879883 | 0.0019989014 | 0.0015487671 | 1.2906 | 3.8529 | 2.9853 |
| E18 | 0.00010871887 | 0.0010299683 | 0.0010299683 | 1.0000 | 9.4737 | 9.4737 |

---

## 11. Primary 统计分析

Primary estimand:

`R_i = P_Quasi_i / P_Control_i`

Number 的 independent 实体:

**18**

Median R:

**1.049345**

Mean log(R):

**0.035391**

Geometric 均值 R:

**1.036025**

Entities 使用 R > 1:

**10/18 (0.556)**

Entities 使用 R < 1:

**5/18**

精确 ties:

**3/18**

---

## 12. Bootstrap Confidence Intervals

Entity-level Bootstrap:

- 随机种子: 0;
- replicates: 100000;
- sampling unit: 实体.

95% Bootstrap CI用于中位数 R:

**[0.925573,
1.268738]**

95% Bootstrap CI用于几何均值 R:

**[0.886387,
1.203981]**

Both 置信区间s 纳入 the no-excess-recovery reference value
of **1**.

---

## 13. Paired Sign Test

Entity-level directions:

- Quasi > 对照: 10;
- Quasi < 对照: 5;
- ties: 3.

Two-sided 精确 paired sign-test p-value:

**0.3017578125**

This analysis does not provide 强证据 的 a consistent
directional Quasi-over-Control 恢复 effect 跨 the 18 实体.

---

## 14. Generic Post-Unlearning 恢复

Although the Quasi-over-Control difference 是 small, both post-RMU
fine-tuning conditions produce large increases 相对于 RMU Step-0.

Using ratios 的 算术均值 target-answer probabilities:

Quasi / RMU:

**9.4124x**

对照 / RMU:

**9.0471x**

Therefore, substantial target-answer 恢复 occurs 之后 both
correlated 准标识符 训练 和 无关对照 训练.

This shows that generic 机器遗忘后 supervised fine-tuning 是 an
important 恢复 baseline 和 confounder.

A 恢复 增加 之后 相关证据 alone cannot be
interpreted作为证据 的 entity-specific 恢复 不使用 比较
against such a 对照.

---

## 15. Relationship到Experiment 008

Experiment 008 observed a 初步 Quasi/对照 excess-recovery
signal 的 approximately:

**2.488x**

using 仅 two 目标 实体.

Experiment 009 increases the 统计 unit到18 independent,
previously unused 实体.

正式 Experiment 009 results are:

- 比率 的 算术均值 probabilities:
  **1.0404x**;
- 中位数 entity-level R:
  **1.0493x**;
- 几何均值 entity-level R:
  **1.0360x**;
- R > 1:
  **10/18**;
- sign-test p:
  **0.3018**;
- Bootstrap intervals 纳入 1.

Therefore:

**The approximately 2.488x quasi-identifier-associated excess 恢复
observed在the two-entity Experiment 008 为 not stably reproduced in
the 18-entity Experiment 009 validation cohort.**

The Experiment 008 result 应当因此remain characterized作为a
初步, entity-dependent signal rather比a robust general
effect.

---

## 16. Main 结论

Experiment 009 does **not** provide 强证据 that masked
multi-attribute 准标识符 证据 consistently produces greater
heldout identity 恢复比匹配 无关 证据 under this
frozen TOFU/RMU protocol.

However, Experiment 009 provides clear 证据 的 a 不同 and
important phenomenon:

**target-answer probabilities recover substantially 之后 generic
机器遗忘后 supervised fine-tuning, even when the fine-tuning data
are 无关到the 遗忘目标 实体.**

Under the present protocol:

- Quasi/RMU aggregate 恢复 是 approximately
  **9.41x**;
- 对照/RMU aggregate 恢复 是 approximately
  **9.05x**;
- Quasi/对照 是 仅 approximately
  **1.04x**.

This motivates treating **机器遗忘后的通用不稳定性**作为a
first-class baseline在subsequent 恢复 studies.

---

## 17. 解释 Boundaries

Experiment 009 does not establish:

- 精确 latent-memory persistence;
- semantic identity 恢复;
- universal 失败 的 RMU;
- universal 失败 的 machine 机器遗忘;
- 临床 patient-level 恢复;
- cardiovascular-data 恢复;
- 统计 证据用于a universal 准标识符 effect.

结果 apply到the present:

- TOFU benchmark;
- Llama-3.2-1B-Instruct model;
- RMU 配置;
- 20-step SFT 恢复 protocol;
- 18-entity validation cohort.

---

## 18. 已冻结 分析 实验产物

正式 实体 table:

`results/formal_recovery_entity_analysis_v1.csv`

SHA256:

`f0405d82a956b57577a03f5a0e87782b3b244b1f39b80ef080395610a2b87880`

正式 statistics:

`results/formal_recovery_statistics_v1.json`

SHA256:

`a20c0622ce9608a87748d2cd9c014de1a9be27d06a1d87f82c19fb2f14676b31`

RMU Step-0 评估:

`results/rmu_step0_18entity/TOFU_EVAL.json`

SHA256:

`63a8505fabc42109d2c847cc0f00bf45f02f380f9f6269d9d7d8be2ef9a00a61`

Quasi 正式 评估:

`results/quasi_20step_18entity/TOFU_EVAL.json`

SHA256:

`289919415e396bf21e7fc08ae4161fd35eaeb4e4da09ef8acf0d53aad11f0f6d`

对照 正式 评估:

`results/control_20step_18entity/TOFU_EVAL.json`

SHA256:

`d26eb837c9ee940db1ff8b0ec71620b9467d4f7743e633ae7f8c389c201fac9c`

---

## 19. Core 已冻结 SHA256 记录

### Primary datasets

Quasi v3:

`c60a2720057b0574e99b3bec5f18dedaf468fac24212b949cde26d74d1c0e8a6`

对照 v3:

`edb0db3629f21a41d4d7fb91a531546784da1c7285a291e96e0e2e04c2c99511`

Heldout targets:

`1236a72d8ffb9ac5bb90fd04551ae43b57bc5ae9d2f4e679bc2ad61359195f6a`

### Protocols

恢复 训练 protocol:

`73a29bf6871c9381ce94ec97ac0bd582d2ea41b9dc16eae93206ebf5f729831f`

恢复 analysis plan:

`7b660ecb201b151cefea9410768c465f49095ad29d51d782fb346ebfd09774fa`

Matched 对照 protocol:

`1406a62e77fd3262bd55fcdc8d58b988ef1ff3751f72c458bdf9291df11eb6e7`

### Additional verified provenance

- `source_manifest_v2.json`: `338fc61c8f5046cfe9e64cabe7dd07de19d3667398e0aa7069e769fb8746a8d6`
- `identity_dictionary_v1.json`: `949a4e4725595a9dd11e95e709537965a00ce1993f7169bdc038d9f334c8f1a3`
- `control_profile_assignment_v1.json`: `fa50af811763b6333333f30c6d8d8704a4c7d0e9c960ff3ff1cc038669b5aae0`
- `control_selection_manifest_v2.json`: `58a7e3040b3700eecab2b7bcd778df63498d5ce67507071df2ff602fbfa84814`
- `control_identity_dictionary_v1.json`: `f12b7fc4164975b452870d48a749fc2dcdc3a8d54bd0fb9eb02594a8e6dd2889`
- `control_masked_v3_final_audit_v2.json`: `1cafa7a7b6748b921bcf5fb0b29f5daa5a215a50b438ccceffa7643389a2e1ba`
- `quasi_control_token_matching_v2_final.json`: `80473b353e26f184aaecd6d8436da55d2cfb04e05f361ac66cc49fac0657bf91`


---

## 20. Final Research Record

Experiment 009 began作为a 统计 validation 的 the
准标识符 恢复 signal observed在Experiment 008.

The larger validation did not stably 复现 that excess-recovery
effect.

At the 相同 time, 该实验 revealed that both correlated and
无关 机器遗忘后 SFT can produce large target-answer 恢复
相对于 the RMU Step-0 state.

结果ing research direction 是因此refined 来自:

> quasi-identifiers reliably recover forgotten identities

to the more general 机制 问题:

> how robust 是 machine 机器遗忘到ordinary 机器遗忘后 model
> updates, 和 when does 相关证据 produce 恢复 beyond
> this generic update-induced baseline?

This distinction 必须 be preserved在subsequent experiments 和 in
paper claims.

---

## 21. Seal

状态:

`EXP009_SEALED`

After sealing, Experiment 009 artifacts 是 treated作为不可修改.

Any new analysis 必须 be 已创建作为a separately versioned artifact.

Any new 训练 experiment 必须 use a new experiment number.

No Exp009 dataset, protocol, 正式 checkpoint, 评估 output, or
正式 result 可能 be 已覆盖.
