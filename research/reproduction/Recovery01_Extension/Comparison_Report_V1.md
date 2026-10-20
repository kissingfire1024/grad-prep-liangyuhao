# Recovery01 三种遗忘算法横向对比 — V1

## 1. 实验范围

- 对比方法：RMU、GradDiff、SimNPO。
- 比较各方法自身 Clean01、Attack Step20、Control Step20。
- Attack 为准标识符关联微调，Control 为匹配无关数据微调。
- 身份目标：B0 与 N20，两名虚构人物。
- TOFU forget01 共 40 条问答，不能视为 40 名独立人物。
- 报告仅包含已验证的原始实验，不包含 GradAscent。

## 2. 官方 TOFU 聚合指标

### RMU

| 指标 | Clean01 | Attack20 | Control20 | Attack-Control |
|---|---:|---:|---:|---:|
| Forget QA Probability | 0.03190904 | 0.04714088 | 0.05333080 | -0.00618992 |
| Forget ROUGE-L Recall | 0.23698820 | 0.20292625 | 0.22675584 | -0.02382960 |
| Retain QA Probability | 0.82958008 | 0.80274414 | 0.80359375 | -0.00084961 |
| Retain ROUGE-L Recall | 0.74166341 | 0.67665407 | 0.69421915 | -0.01756508 |
| Model Utility | 0.58685130 | 0.58918605 | 0.58781742 | +0.00136862 |
| Forget Quality | 0.16497270 | 0.16497270 | 0.16497270 | +0.00000000 |
| MIA Min-K AUC | 0.07500000 | 0.10187500 | 0.10500000 | -0.00312500 |
| Extraction Strength | 0.02905941 | 0.03029567 | 0.03154567 | -0.00125000 |

### GradDiff

| 指标 | Clean01 | Attack20 | Control20 | Attack-Control |
|---|---:|---:|---:|---:|
| Forget QA Probability | 0.00854999 | 0.11296997 | 0.04662037 | +0.06634960 |
| Forget ROUGE-L Recall | 0.31618777 | 0.34008848 | 0.36309527 | -0.02300679 |
| Retain QA Probability | 0.41005066 | 0.77523926 | 0.79724609 | -0.02200684 |
| Retain ROUGE-L Recall | 0.41204508 | 0.61108807 | 0.60903194 | +0.00205613 |
| Model Utility | 0.47151575 | 0.56782680 | 0.58709047 | -0.01926368 |
| Forget Quality | 0.40458741 | 0.16497270 | 0.40458741 | -0.23961471 |
| MIA Min-K AUC | 0.12312500 | 0.28687500 | 0.15937500 | +0.12750000 |
| Extraction Strength | 0.04834426 | 0.07070754 | 0.06471853 | +0.00598901 |

### SimNPO

| 指标 | Clean01 | Attack20 | Control20 | Attack-Control |
|---|---:|---:|---:|---:|
| Forget QA Probability | 0.76220703 | 0.79248047 | 0.79492188 | -0.00244141 |
| Forget ROUGE-L Recall | 0.62745290 | 0.59463657 | 0.62548633 | -0.03084976 |
| Retain QA Probability | 0.87250488 | 0.84769043 | 0.85139160 | -0.00370117 |
| Retain ROUGE-L Recall | 0.77660385 | 0.74153545 | 0.76657960 | -0.02504415 |
| Model Utility | 0.59699232 | 0.59973292 | 0.60080974 | -0.00107682 |
| Forget Quality | 0.00676073 | 0.01430155 | 0.00676073 | +0.00754082 |
| MIA Min-K AUC | 0.98937500 | 0.99812500 | 0.99875000 | -0.00062500 |
| Extraction Strength | 0.37496344 | 0.37392518 | 0.35512734 | +0.01879784 |

## 3. 跨算法 Attack-Control 汇总

| 指标 | RMU | GradDiff | SimNPO |
|---|---:|---:|---:|
| Forget QA Probability | -0.00618992 | +0.06634960 | -0.00244141 |
| Forget ROUGE-L Recall | -0.02382960 | -0.02300679 | -0.03084976 |
| Retain QA Probability | -0.00084961 | -0.02200684 | -0.00370117 |
| Retain ROUGE-L Recall | -0.01756508 | +0.00205613 | -0.02504415 |
| Model Utility | +0.00136862 | -0.01926368 | -0.00107682 |
| Forget Quality | +0.00000000 | -0.23961471 | +0.00754082 |
| MIA Min-K AUC | -0.00312500 | +0.12750000 | -0.00062500 |
| Extraction Strength | -0.00125000 | +0.00598901 | +0.01879784 |

## 4. Forget QA 逐样本配对分析

| 方法 | 问题组 | 平均 A-C | 中位 A-C | 正向 | 相等 | 负向 |
|---|---|---:|---:|---:|---:|---:|
| RMU | 全部 40 问题 | -0.00618992 | -0.00216675 | 6 | 0 | 34 |
| RMU | B0 的 20 问题 | -0.00893250 | -0.00170898 | 5 | 0 | 15 |
| RMU | N20 的 20 问题 | -0.00344734 | -0.00257874 | 1 | 0 | 19 |
| GradDiff | 全部 40 问题 | +0.06634960 | +0.04635620 | 40 | 0 | 0 |
| GradDiff | B0 的 20 问题 | +0.08472977 | +0.05560303 | 20 | 0 | 0 |
| GradDiff | N20 的 20 问题 | +0.04796944 | +0.04074097 | 20 | 0 | 0 |
| SimNPO | 全部 40 问题 | -0.00244141 | -0.00195312 | 11 | 9 | 20 |
| SimNPO | B0 的 20 问题 | +0.00058594 | +0.00000000 | 3 | 8 | 9 |
| SimNPO | N20 的 20 问题 | -0.00546875 | -0.00781250 | 8 | 1 | 11 |

## 5. 身份恢复结果

| 方法 | 目标 | Step0 命中 | Attack20 命中 | Control20 命中 | A-C 姓名 LogP | A-C 姓名 Margin |
|---|---|---|---|---|---:|---:|
| RMU | B0 | False | False | False | -0.60924983 | -0.38993621 |
| RMU | N20 | False | False | False | -0.02795124 | +0.35997343 |
| GradDiff | B0 | False | False | False | +0.70536780 | -0.08575845 |
| GradDiff | N20 | False | False | False | +1.40658236 | +0.32107878 |
| SimNPO | B0 | False | False | False | +0.10123014 | -0.06706190 |
| SimNPO | N20 | True | True | True | +0.07526016 | +0.08303738 |

## 6. 初步观察

1. GradDiff 的 Attack-Control Forget QA Probability 差值为正；RMU 与 SimNPO 在当前实验中为负。
2. 必须区分教师强制条件概率上升和自由生成完整身份成功；二者不是同一指标。
3. SimNPO 的 N20 在 Step0 已经能够正确生成姓名，不能计为 Attack 新增的恢复成功。
4. GradDiff 的 40/40 同向差异是问答层面的描述性结果，不是 40 名独立人物的统计证据。
5. 不同 Clean01 的初始遗忘强度差异较大，直接比较 Step20 绝对值容易产生误导。

## 7. 局限与后续工作

- 每种方法当前仅有一个随机种子。
- 两名虚构人物不足以支持人群层面的泛化结论。
- 尚未计算跨种子置信区间或显著性检验。
- 无新的完整姓名命中时，不应声称身份提取攻击成功。
- 现有结果不能直接证明具体的表征恢复机制。
- 后续继续核验并运行 GradAscent，以补齐第四种遗忘方法。

## 8. 来源文件及 SHA256

| 方法 | 来源 | 相对路径 | SHA256 |
|---|---|---|---|
| RMU | Clean01 | `saves/eval/tofu_Llama-3.2-1B-Instruct_forget01_RMU_Clean01_eval/TOFU_EVAL.json` | `96fca2d39b02e0bbf968f39d196454a26cdfac6bd08013788e8864073ea43b29` |
| RMU | Attack20 | `saves/eval/Recovery01_Analysis03_Attack_Step20/TOFU_EVAL.json` | `e13ee4f926f6680c4c314a3a1b15d88e526dde4d368d6634b3b3997ae7e3addd` |
| RMU | Control20 | `saves/eval/Recovery01_Analysis03_Control_Step20/TOFU_EVAL.json` | `ec750a0960d0ac6f3f9ffce802a5d40253650af62361d2c3df6fce70ad929bf8` |
| RMU | step0 | `reports/Recovery01_Clean_RMU_QuasiIdentifier/step0_baseline.json` | `59d86758d1bb8d1be0177948c58d63461f46b8fac2583fbb9069ee3451459410` |
| RMU | recovery | `reports/Recovery01_Clean_RMU_QuasiIdentifier/recovery_checkpoint_results.json` | `42bb26e0ff0c2503858c4b943a8d535c4113b6b02ed59858076de0f4c5a709de` |
| GradDiff | Clean01 | `saves/eval/tofu_Llama-3.2-1B-Instruct_forget01_GradDiff_Clean01_eval/TOFU_EVAL.json` | `460f84a9724b85bf99dcc6b5a407ee1b3e61c14e64cec8f869760a05c93577b1` |
| GradDiff | Attack20 | `saves/eval/Recovery01_Extension_GradDiff_Attack_Step20/TOFU_EVAL.json` | `77f088bf7c6dc538924aa141645004f9b9a9c171fdb0b96eaac6e1898e61bd13` |
| GradDiff | Control20 | `saves/eval/Recovery01_Extension_GradDiff_Control_Step20/TOFU_EVAL.json` | `f7ed7b9dfe7b67b1ad4bf2d47d1a1e846038c2910205ffea200d97ab36a860ca` |
| GradDiff | step0 | `reports/Recovery01_Extension/GradDiff_step0_baseline.json` | `0e238e9953c86ca218c5255eeeff0f4aaa00e57d204f8cf539ff5e03a45e7661` |
| GradDiff | recovery | `reports/Recovery01_Extension/GradDiff_checkpoint_recovery_results.json` | `4ae03cdf0cffff014477a8d1242fd5312553fd8565afc5922dcc60f83ae068ab` |
| SimNPO | Clean01 | `saves/eval/tofu_Llama-3.2-1B-Instruct_forget01_SimNPO_Clean01_eval/TOFU_EVAL.json` | `ece1096e852a009db068b27621c3079539b741eff90f20f75d443f5d7d245620` |
| SimNPO | Attack20 | `saves/eval/Recovery01_Extension_SimNPO_Attack_Step20/TOFU_EVAL.json` | `a8406dd9c6cf4bcd798704c5d6a82d249ff515718698af8173b5ca8c745a5c61` |
| SimNPO | Control20 | `saves/eval/Recovery01_Extension_SimNPO_Control_Step20/TOFU_EVAL.json` | `fa7f04dfeffc6e07d05cf8be6a144defcd5f1a2e4d1923fa6438da22397f612a` |
| SimNPO | step0 | `reports/Recovery01_Extension/SimNPO_step0_baseline.json` | `a196efa93be6945f8d79f497c4a4fb08aa4c02287c7cd3688fc4d254f4550302` |
| SimNPO | recovery | `reports/Recovery01_Extension/SimNPO_checkpoint_recovery_results.json` | `d841971bb85a354302808b3a3a341b5688d0a7e21d8e7adb4c874de0ba9056f7` |

