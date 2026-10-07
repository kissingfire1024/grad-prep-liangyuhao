# Experiment 009 — Multi-Entity Statistical Validation

## Final Status

**SEALED**

Experiment 009 is a frozen multi-entity validation of the
quasi-identifier-associated recovery signal observed in Experiment 008.

The formal recovery outcomes were evaluated only after the recovery
training protocol, datasets, controls, heldout targets, and analysis
plan had been frozen.

No post-outcome entity replacement, evidence replacement, control
rematching, training-step adjustment, or hyperparameter adjustment was
performed.

---

## 1. Research Question

Experiment 008 produced a preliminary quasi-identifier-associated
target-likelihood recovery signal using only two target entities.

Its formal Quasi/Control mean probability ratio was approximately:

**2.488x**

Experiment 009 tests whether that signal generalizes across a larger
set of previously unused independent TOFU author entities.

The primary statistical unit is the **entity**, not the QA example.

Validation cohort:

**18 independent entities (E01-E18)**

The Basil Mahfouz Al-Kuwaiti and Nikolai Abilov entities used during
Experiments 006-008 were excluded from this validation cohort.

---

## 2. Experimental Design

Official TOFU `forget10` contains 400 QA records organized into
20 author blocks of 20 QA records.

Experiment 009 uses the first 18 previously unused author entities.

For every validation entity:

- one identity question is held out as the recovery target;
- five frozen multi-attribute quasi-identifier evidence records are
  used in the Quasi condition;
- five unrelated matched-control records are used in the Control
  condition.

The heldout target records are never included in either recovery
training dataset.

Total formal recovery evidence:

- Quasi: 90 QA records;
- Control: 90 QA records;
- Heldout targets: 18 QA records.

---

## 3. RMU Step-0 Base Model

Formal recovery training begins independently from:

`/home/research/open-unlearning/saves/unlearn/tofu_Llama-3.2-1B-Instruct_forget10_RMU_exp009`

RMU forget10 training:

- method: RMU;
- base model: Llama-3.2-1B-Instruct;
- forget split: forget10;
- retain split: retain90;
- optimizer steps: 100;
- batch size: 1;
- gradient accumulation: 4;
- steering coefficient: 2;
- gamma: 1;
- alpha: 1;
- retain loss: EMBED_DIFF;
- representation module: model.layers.7;
- trainable parameter regex: `.*`;
- attention implementation: SDPA.

The 100-step RMU run completed at epoch 1.0.

RMU Step-0 mean heldout target-answer probability:

**0.0001351965798272027**

All 18 validation targets had lower target-answer probability after RMU
than in the corresponding full-model baseline.

---

## 4. Frozen Quasi Dataset

File:

`data/quasi_identifier_masked_v3.json`

SHA256:

`c60a2720057b0574e99b3bec5f18dedaf468fac24212b949cde26d74d1c0e8a6`

Properties:

- 18 entities;
- 5 records/entity;
- 90 total records;
- 90 unique records;
- direct target identities removed;
- direct birth/geography bridges excluded;
- book-title proxies excluded;
- synthetic identifiers excluded.

Final status:

`EXP009_QUASI_IDENTIFIER_MASKED_V3_FROZEN`

---

## 5. Frozen Matched Unrelated Control

File:

`data/control_masked_v3.json`

SHA256:

`edb0db3629f21a41d4d7fb91a531546784da1c7285a291e96e0e2e04c2c99511`

Properties:

- official TOFU retain90 source only;
- 18 unrelated source profiles;
- one distinct control profile per validation entity;
- 5 records/entity;
- 90 total records;
- identity masking applied;
- heldout target identities excluded.

Final audit:

90/90 PASS.

Final status:

`EXP009_CONTROL_MASKED_V3_FROZEN`

---

## 6. Frozen Heldout Targets

File:

`data/heldout_targets_18entity_v1.json`

SHA256:

`1236a72d8ffb9ac5bb90fd04551ae43b57bc5ae9d2f4e679bc2ad61359195f6a`

Heldout source indices:

`[0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340]`

Quasi/target source overlap:

**0**

Control/target source overlap:

**0**

Final status:

`EXP009_HELDOUT_TARGETS_18ENTITY_V1_FROZEN`

---

## 7. Token Exposure Matching

Final tokenizer exposure:

- Quasi: 3604 tokens;
- Control: 3498 tokens;
- Control/Quasi: 0.970588;
- global relative difference: approximately 2.94%.

Residual entity-level exposure mismatch greater than 25% remained for:

- E06;
- E13;
- E17.

These entities were retained in the primary analysis according to the
pre-outcome protocol.

No post-outcome rematching was performed.

---

## 8. Frozen Recovery Training Protocol

File:

`notes/recovery_training_protocol_v1.md`

SHA256:

`73a29bf6871c9381ce94ec97ac0bd582d2ea41b9dc16eae93206ebf5f729831f`

Status:

`EXP009_RECOVERY_TRAINING_PROTOCOL_V1_FROZEN`

Formal configuration for **both** Quasi and Control:

- starting checkpoint: identical RMU forget10 Step-0;
- trainer: finetune;
- model: Llama-3.2-1B-Instruct;
- attention: SDPA;
- per-device train batch size: 1;
- per-device eval batch size: 1;
- gradient accumulation: 4;
- effective examples/optimizer step: 4;
- learning rate: 1e-5;
- weight decay: 0.01;
- gradient checkpointing: true;
- logging steps: 1;
- optimizer steps: 20;
- training-time evaluation: disabled;
- save strategy: no;
- same default OpenUnlearning seed;
- same scheduler behavior.

Observed learning-rate trajectory for both formal runs:

`1e-5 -> 5e-7`

Both trajectories completed:

- global step: 20;
- epoch: 0.8888888888888888;
- no OOM;
- no NaN;
- no Inf.

Formal Quasi train loss:

**6.538412976264953**

Formal Control train loss:

**6.346207809448242**

Both final model checkpoints contained one
2,471,645,608-byte `model.safetensors` file.

Formal trajectory symmetry audit:

`EXP009_FORMAL_TRAJECTORIES_SYMMETRY_AUDIT_PASS`

---

## 9. Formal Evaluation

Both trajectories were evaluated using the same frozen 18-target
evaluator before any entity-level outcome analysis.

Primary metric:

**heldout target-answer probability**

Auxiliary metric:

**ROUGE-L recall**

Aggregate formal results:

| Condition | Mean Target Probability | ROUGE-L Recall |
|---|---:|---:|
| RMU Step-0 | 0.0001351965798 | N/A |
| Quasi 20-step | 0.00127251943 | 0.185069888 |
| Control 20-step | 0.001223140293 | 0.1782797645 |

Ratio of arithmetic mean probabilities:

**1.040371x**

---

## 10. Entity-Level Formal Results

| Entity | P_RMU | P_Quasi | P_Control | R=Q/C | GQ=Q/RMU | GC=C/RMU |
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

## 11. Primary Statistical Analysis

Primary estimand:

`R_i = P_Quasi_i / P_Control_i`

Number of independent entities:

**18**

Median R:

**1.049345**

Mean log(R):

**0.035391**

Geometric mean R:

**1.036025**

Entities with R > 1:

**10/18 (0.556)**

Entities with R < 1:

**5/18**

Exact ties:

**3/18**

---

## 12. Bootstrap Confidence Intervals

Entity-level bootstrap:

- seed: 0;
- replicates: 100000;
- sampling unit: entity.

95% bootstrap CI for median R:

**[0.925573,
1.268738]**

95% bootstrap CI for geometric mean R:

**[0.886387,
1.203981]**

Both confidence intervals include the no-excess-recovery reference value
of **1**.

---

## 13. Paired Sign Test

Entity-level directions:

- Quasi > Control: 10;
- Quasi < Control: 5;
- ties: 3.

Two-sided exact paired sign-test p-value:

**0.3017578125**

This analysis does not provide strong evidence of a consistent
directional Quasi-over-Control recovery effect across the 18 entities.

---

## 14. Generic Post-Unlearning Recovery

Although the Quasi-over-Control difference is small, both post-RMU
fine-tuning conditions produce large increases relative to RMU Step-0.

Using ratios of arithmetic mean target-answer probabilities:

Quasi / RMU:

**9.4124x**

Control / RMU:

**9.0471x**

Therefore, substantial target-answer recovery occurs after both
correlated quasi-identifier training and unrelated control training.

This shows that generic post-unlearning supervised fine-tuning is an
important recovery baseline and confounder.

A recovery increase after correlated evidence alone cannot be
interpreted as evidence of entity-specific recovery without comparison
against such a control.

---

## 15. Relationship to Experiment 008

Experiment 008 observed a preliminary Quasi/Control excess-recovery
signal of approximately:

**2.488x**

using only two target entities.

Experiment 009 increases the statistical unit to 18 independent,
previously unused entities.

Formal Experiment 009 results are:

- ratio of arithmetic mean probabilities:
  **1.0404x**;
- median entity-level R:
  **1.0493x**;
- geometric mean entity-level R:
  **1.0360x**;
- R > 1:
  **10/18**;
- sign-test p:
  **0.3018**;
- bootstrap intervals include 1.

Therefore:

**The approximately 2.488x quasi-identifier-associated excess recovery
observed in the two-entity Experiment 008 was not stably reproduced in
the 18-entity Experiment 009 validation cohort.**

The Experiment 008 result should therefore remain characterized as a
preliminary, entity-dependent signal rather than a robust general
effect.

---

## 16. Main Conclusion

Experiment 009 does **not** provide strong evidence that masked
multi-attribute quasi-identifier evidence consistently produces greater
heldout identity recovery than matched unrelated evidence under this
frozen TOFU/RMU protocol.

However, Experiment 009 provides clear evidence of a different and
important phenomenon:

**target-answer probabilities recover substantially after generic
post-unlearning supervised fine-tuning, even when the fine-tuning data
are unrelated to the forgotten target entity.**

Under the present protocol:

- Quasi/RMU aggregate recovery is approximately
  **9.41x**;
- Control/RMU aggregate recovery is approximately
  **9.05x**;
- Quasi/Control is only approximately
  **1.04x**.

This motivates treating **generic post-unlearning instability** as a
first-class baseline in subsequent recovery studies.

---

## 17. Interpretation Boundaries

Experiment 009 does not establish:

- exact latent-memory persistence;
- semantic identity recovery;
- universal failure of RMU;
- universal failure of machine unlearning;
- clinical patient-level recovery;
- cardiovascular-data recovery;
- statistical evidence for a universal quasi-identifier effect.

The results apply to the present:

- TOFU benchmark;
- Llama-3.2-1B-Instruct model;
- RMU configuration;
- 20-step SFT recovery protocol;
- 18-entity validation cohort.

---

## 18. Frozen Analysis Artifacts

Formal entity table:

`results/formal_recovery_entity_analysis_v1.csv`

SHA256:

`f0405d82a956b57577a03f5a0e87782b3b244b1f39b80ef080395610a2b87880`

Formal statistics:

`results/formal_recovery_statistics_v1.json`

SHA256:

`a20c0622ce9608a87748d2cd9c014de1a9be27d06a1d87f82c19fb2f14676b31`

RMU Step-0 evaluation:

`results/rmu_step0_18entity/TOFU_EVAL.json`

SHA256:

`63a8505fabc42109d2c847cc0f00bf45f02f380f9f6269d9d7d8be2ef9a00a61`

Quasi formal evaluation:

`results/quasi_20step_18entity/TOFU_EVAL.json`

SHA256:

`289919415e396bf21e7fc08ae4161fd35eaeb4e4da09ef8acf0d53aad11f0f6d`

Control formal evaluation:

`results/control_20step_18entity/TOFU_EVAL.json`

SHA256:

`d26eb837c9ee940db1ff8b0ec71620b9467d4f7743e633ae7f8c389c201fac9c`

---

## 19. Core Frozen SHA256 Records

### Primary datasets

Quasi v3:

`c60a2720057b0574e99b3bec5f18dedaf468fac24212b949cde26d74d1c0e8a6`

Control v3:

`edb0db3629f21a41d4d7fb91a531546784da1c7285a291e96e0e2e04c2c99511`

Heldout targets:

`1236a72d8ffb9ac5bb90fd04551ae43b57bc5ae9d2f4e679bc2ad61359195f6a`

### Protocols

Recovery training protocol:

`73a29bf6871c9381ce94ec97ac0bd582d2ea41b9dc16eae93206ebf5f729831f`

Recovery analysis plan:

`7b660ecb201b151cefea9410768c465f49095ad29d51d782fb346ebfd09774fa`

Matched control protocol:

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

Experiment 009 began as a statistical validation of the
quasi-identifier recovery signal observed in Experiment 008.

The larger validation did not stably reproduce that excess-recovery
effect.

At the same time, the experiment revealed that both correlated and
unrelated post-unlearning SFT can produce large target-answer recovery
relative to the RMU Step-0 state.

The resulting research direction is therefore refined from:

> quasi-identifiers reliably recover forgotten identities

to the more general mechanism question:

> how robust is machine unlearning to ordinary post-unlearning model
> updates, and when does correlated evidence produce recovery beyond
> this generic update-induced baseline?

This distinction must be preserved in subsequent experiments and in
paper claims.

---

## 21. Seal

Status:

`EXP009_SEALED`

After sealing, Experiment 009 artifacts are treated as immutable.

Any new analysis must be created as a separately versioned artifact.

Any new training experiment must use a new experiment number.

No Exp009 dataset, protocol, formal checkpoint, evaluation output, or
formal result may be overwritten.
