# SimNPO Recovery01 Extension — Stage Report V1

## 1. Experiment and scope

- Method: SimNPO, Clean01 forget01 starting checkpoint.
- Attack: quasi-identifier association fine-tuning.
- Control: matched unrelated fine-tuning.
- Seed: 42; learning rate: 1e-5; training steps: 20.
- Checkpoints: steps 5, 10, 15, and 20.
- Dataset: TOFU forget01 (40 QA items concerning TWO fictional people).
- Identity targets: B0 (Basil Mahfouz Al-Kuwaiti) and N20 (Nikolai Abilov).
- No real patients or clinical records are involved.

## 2. Source files and integrity

| Source | SHA256 |
|---|---|
| Clean01 | `ece1096e852a009db068b27621c3079539b741eff90f20f75d443f5d7d245620` |
| Attack | `a8406dd9c6cf4bcd798704c5d6a82d249ff515718698af8173b5ca8c745a5c61` |
| Control | `fa7f04dfeffc6e07d05cf8be6a144defcd5f1a2e4d1923fa6438da22397f612a` |
| Step0 | `a196efa93be6945f8d79f497c4a4fb08aa4c02287c7cd3688fc4d254f4550302` |
| Recovery | `d841971bb85a354302808b3a3a341b5688d0a7e21d8e7adb4c874de0ba9056f7` |
| Protocol | `79da6189b916d06fe019021a24a249a013b74cae1178df6efbea65f3dc6a6cd0` |
| Manifest | `05f22a8c78c6bff924249d70dec5ccf2a92c3fda6b61ca58a42991e6ca91a3b7` |

## 3. Official TOFU results

| Metric | Clean01 | Attack20 | Control20 | Attack-Control |
|---|---:|---:|---:|---:|
| Forget QA Probability | 0.76220703 | 0.79248047 | 0.79492188 | -0.00244141 |
| Forget ROUGE-L Recall | 0.62745290 | 0.59463657 | 0.62548633 | -0.03084976 |
| Retain QA Probability | 0.87250488 | 0.84769043 | 0.85139160 | -0.00370117 |
| Retain ROUGE-L Recall | 0.77660385 | 0.74153545 | 0.76657960 | -0.02504415 |
| Model Utility | 0.59699232 | 0.59973292 | 0.60080974 | -0.00107682 |
| Forget Quality | 0.00676073 | 0.01430155 | 0.00676073 | +0.00754082 |
| Min-K% MIA AUC | 0.98937500 | 0.99812500 | 0.99875000 | -0.00062500 |
| Privacy Leakage | -97.97859689 | -99.64328179 | -99.76218785 | +0.11890606 |
| Extraction Strength | 0.37496344 | 0.37392518 | 0.35512734 | +0.01879784 |

## 4. Paired per-question analysis

Counts represent questions, NOT independent people.

| Metric | Group | Mean A-C | Median A-C | Positive | Equal | Negative |
|---|---|---:|---:|---:|---:|---:|
| Forget QA Probability | All | -0.00244141 | -0.00195312 | 11 | 9 | 20 |
| Forget QA Probability | B0 questions | +0.00058594 | +0.00000000 | 3 | 8 | 9 |
| Forget QA Probability | N20 questions | -0.00546875 | -0.00781250 | 8 | 1 | 11 |
| Forget ROUGE-L Recall | All | -0.03084976 | +0.00000000 | 6 | 20 | 14 |
| Forget ROUGE-L Recall | B0 questions | -0.01403009 | +0.00000000 | 2 | 12 | 6 |
| Forget ROUGE-L Recall | N20 questions | -0.04766944 | +0.00000000 | 4 | 8 | 8 |
| Retain ROUGE-L Recall | All | -0.02504415 | +0.00000000 | 45 | 277 | 78 |

## 5. Identity-target evaluation

| Target | Step0 exact | Attack20 exact | Control20 exact | Attack-Control correct-name LogP | Attack-Control name margin |
|---|---|---|---|---:|---:|
| B0 | False | False | False | +0.10123014 | -0.06706190 |
| N20 | True | True | True | +0.07526016 | +0.08303738 |

## 6. Findings

1. Forget QA Probability (Attack-Control) is slightly negative overall. The paired distribution is not consistently positive.
2. Attack has lower average Forget and Retain ROUGE-L Recall than Control under the evaluated configuration.
3. B0 has no exact-name success at Step0 or either Step20 model.
4. N20 is already an exact-name success at Step0. Later hits do NOT constitute newly recovered identity.
5. Correct-name teacher-forced LogP shifts do not by themselves demonstrate successful free-generation identity recovery.

## 7. Limitations

- One random seed and one 20-step fine-tuning schedule.
- Forty forget questions describe only TWO fictional entities; question-level counts are not independent-person replicates.
- No uncertainty intervals or independent-seed significance tests yet.
- The SimNPO Clean01 model already has high forget-answer probability and a pre-existing exact-name hit for N20.
- Higher MIA AUC reflects greater separability for the tested MIA statistic; it is not an identity-extraction success rate.
- These observations do not establish a causal mechanism or prove that recovery is impossible.

## 8. Next experiment

Prepare a cross-method comparison against RMU and GradDiff using the same baselines, Attack-Control contrasts and identity-hit definitions, then proceed to GradAscent.

