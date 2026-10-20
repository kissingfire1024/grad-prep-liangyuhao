# Recovery01 四算法完整横向对比报告 — V2

## 1. 实验设计与解释范围

- 方法：RMU、GradDiff、SimNPO、GradAscent。
- 每种方法分别比较 Clean01、Attack Step20、Control Step20。
- Attack：准标识符关联微调；Control：匹配无关数据微调。
- 固定设置：Seed 42、Learning Rate 1e-5、20步。
- 身份目标：B0 与 N20，两名虚构人物。
- Forget 集合共40条问答，每名人物20条，不是40个独立身份。
- 主要比较 Attack-Control，避免仅根据 Attack-Clean01 推断定向恢复。
- 此报告为单种子描述性分析，不包含统计显著性结论。

## 2. 各算法官方 TOFU 指标

### RMU

| 指标 | Clean01 | Attack20 | Control20 | Attack-Control |
|---|---:|---:|---:|---:|
| Forget QA Probability | 0.0319090366 | 0.0471408844 | 0.0533308029 | -0.00618991852 |
| Forget ROUGE-L Recall | 0.236988198 | 0.202926246 | 0.226755843 | -0.0238295972 |
| Retain QA Probability | 0.829580078 | 0.802744141 | 0.80359375 | -0.000849609375 |
| Retain ROUGE-L Recall | 0.741663411 | 0.676654072 | 0.694219151 | -0.0175650783 |
| Model Utility | 0.586851301 | 0.589186049 | 0.587817425 | +0.00136862427 |
| Forget Quality | 0.1649727 | 0.1649727 | 0.1649727 | +0 |
| Min-K MIA AUC | 0.075 | 0.101875 | 0.105 | -0.003125 |
| Extraction Strength | 0.0290594082 | 0.030295672 | 0.031545672 | -0.00125 |
| Privacy Leakage | 75.980975 | 70.8680143 | 70.2734839 | +0.594530321 |

### GradDiff

| 指标 | Clean01 | Attack20 | Control20 | Attack-Control |
|---|---:|---:|---:|---:|
| Forget QA Probability | 0.00854998529 | 0.112969971 | 0.046620369 | +0.0663496017 |
| Forget ROUGE-L Recall | 0.316187773 | 0.340088479 | 0.363095266 | -0.0230067868 |
| Retain QA Probability | 0.410050659 | 0.775239258 | 0.797246094 | -0.0220068359 |
| Retain ROUGE-L Recall | 0.412045078 | 0.611088066 | 0.609031937 | +0.00205612912 |
| Model Utility | 0.471515751 | 0.567826797 | 0.587090473 | -0.0192636764 |
| Forget Quality | 0.404587406 | 0.1649727 | 0.404587406 | -0.239614706 |
| Min-K MIA AUC | 0.123125 | 0.286875 | 0.159375 | +0.1275 |
| Extraction Strength | 0.048344262 | 0.0707075423 | 0.0647185313 | +0.00598901099 |
| Privacy Leakage | 66.8252081 | 35.6718193 | 59.9286564 | -24.2568371 |

### SimNPO

| 指标 | Clean01 | Attack20 | Control20 | Attack-Control |
|---|---:|---:|---:|---:|
| Forget QA Probability | 0.762207031 | 0.792480469 | 0.794921875 | -0.00244140625 |
| Forget ROUGE-L Recall | 0.627452896 | 0.59463657 | 0.625486333 | -0.0308497629 |
| Retain QA Probability | 0.872504883 | 0.84769043 | 0.851391602 | -0.00370117188 |
| Retain ROUGE-L Recall | 0.77660385 | 0.741535448 | 0.766579601 | -0.0250441537 |
| Model Utility | 0.596992323 | 0.599732921 | 0.60080974 | -0.00107681824 |
| Forget Quality | 0.0067607323 | 0.014301548 | 0.0067607323 | +0.00754081574 |
| Min-K MIA AUC | 0.989375 | 0.998125 | 0.99875 | -0.000625 |
| Extraction Strength | 0.374963437 | 0.37392518 | 0.355127338 | +0.0187978413 |
| Privacy Leakage | -97.9785969 | -99.6432818 | -99.7621879 | +0.118906064 |

### GradAscent

| 指标 | Clean01 | Attack20 | Control20 | Attack-Control |
|---|---:|---:|---:|---:|
| Forget QA Probability | 4.35575105e-11 | 0.00070777153 | 0.0115949273 | -0.0108871558 |
| Forget ROUGE-L Recall | 0 | 0.187683072 | 0.221461738 | -0.0337786668 |
| Retain QA Probability | 2.0959171e-08 | 0.0971976089 | 0.340247803 | -0.243050194 |
| Retain ROUGE-L Recall | 0.00296259681 | 0.309199782 | 0.37424937 | -0.0650495879 |
| Model Utility | 0 | 0.32184754 | 0.473339557 | -0.151492017 |
| Forget Quality | 1.48827229e-21 | 0.578600142 | 0.404587406 | +0.174012736 |
| Min-K MIA AUC | 0.16875 | 0.05125 | 0.091875 | -0.040625 |
| Extraction Strength | 0.0290594082 | 0.0298927416 | 0.039689184 | -0.00979644243 |
| Privacy Leakage | 58.1450654 | 80.4994055 | 72.7705113 | +7.72889417 |

## 3. 跨算法 Attack-Control 核心差值

| 指标 | RMU | GradDiff | SimNPO | GradAscent |
|---|---:|---:|---:|---:|---:|
| Forget QA Probability | -0.00618992 | +0.06634960 | -0.00244141 | -0.01088716 |
| Forget ROUGE-L Recall | -0.02382960 | -0.02300679 | -0.03084976 | -0.03377867 |
| Retain QA Probability | -0.00084961 | -0.02200684 | -0.00370117 | -0.24305019 |
| Retain ROUGE-L Recall | -0.01756508 | +0.00205613 | -0.02504415 | -0.06504959 |
| Model Utility | +0.00136862 | -0.01926368 | -0.00107682 | -0.15149202 |
| Forget Quality | +0.00000000 | -0.23961471 | +0.00754082 | +0.17401274 |
| Min-K MIA AUC | -0.00312500 | +0.12750000 | -0.00062500 | -0.04062500 |
| Extraction Strength | -0.00125000 | +0.00598901 | +0.01879784 | -0.00979644 |
| Privacy Leakage | +0.59453032 | -24.25683709 | +0.11890606 | +7.72889417 |

## 4. Forget QA逐样本配对分析

| 算法 | 人物组 | 平均A-C | 中位A-C | 正向 | 相等 | 负向 |
|---|---|---:|---:|---:|---:|---:|
| RMU | 全部40条 | -0.00618992 | -0.00216675 | 6 | 0 | 34 |
| RMU | B0的20条 | -0.00893250 | -0.00170898 | 5 | 0 | 15 |
| RMU | N20的20条 | -0.00344734 | -0.00257874 | 1 | 0 | 19 |
| GradDiff | 全部40条 | +0.06634960 | +0.04635620 | 40 | 0 | 0 |
| GradDiff | B0的20条 | +0.08472977 | +0.05560303 | 20 | 0 | 0 |
| GradDiff | N20的20条 | +0.04796944 | +0.04074097 | 20 | 0 | 0 |
| SimNPO | 全部40条 | -0.00244141 | -0.00195312 | 11 | 9 | 20 |
| SimNPO | B0的20条 | +0.00058594 | +0.00000000 | 3 | 8 | 9 |
| SimNPO | N20的20条 | -0.00546875 | -0.00781250 | 8 | 1 | 11 |
| GradAscent | 全部40条 | -0.01088716 | -0.00300161 | 0 | 0 | 40 |
| GradAscent | B0的20条 | -0.00802873 | -0.00067656 | 0 | 0 | 20 |
| GradAscent | N20的20条 | -0.01374558 | -0.01109028 | 0 | 0 | 20 |

## 5. 身份恢复评估

| 算法 | 目标 | Step0命中 | Attack20命中 | Control20命中 | A-C姓名LogP | A-C姓名Margin |
|---|---|---|---|---|---:|---:|
| RMU | B0 | False | False | False | -0.60924983 | -0.38993621 |
| RMU | N20 | False | False | False | -0.02795124 | +0.35997343 |
| GradDiff | B0 | False | False | False | +0.70536780 | -0.08575845 |
| GradDiff | N20 | False | False | False | +1.40658236 | +0.32107878 |
| SimNPO | B0 | False | False | False | +0.10123014 | -0.06706190 |
| SimNPO | N20 | True | True | True | +0.07526016 | +0.08303738 |
| GradAscent | B0 | False | False | False | -2.79914117 | +0.40060782 |
| GradAscent | N20 | False | False | False | -3.28616476 | -1.35001755 |

## 6. 四算法主要实验观察

### RMU

- Attack整体Forget QA Probability低于Control。
- 两个目标均未出现新增完整姓名生成成功。

### GradDiff

- Attack-Control Forget QA Probability为正。
- 40/40条Forget QA均为正向差异。
- 两个目标的姓名LogP在Attack下高于Control，但没有新增完整姓名生成成功。

### SimNPO

- Clean01本身已表现出高Forget QA Probability。
- N20在Step0已经正确生成完整姓名，之后的命中不应视为新增恢复。
- Attack-Control整体Forget Probability略为负值。

### GradAscent

- Clean01的Model Utility为0，生成主要为重复标点，属于严重效用崩溃。
- Attack和Control微调后都出现部分语言能力恢复。
- Control20的Model Utility明显高于Attack20。
- 40/40条Forget QA的Attack-Control概率差值均为负。
- 两个目标均未出现新增完整姓名生成成功。

## 7. 重要局限和论文表述边界

- 现有实验每种方法仅一个随机种子。
- 只有两名虚构人物，40条QA具有明显组内相关性。
- 概率回升不等于成功的身份信息提取。
- 不应将GradAscent的模型效用崩溃视为更强隐私保护。
- SimNPO存在Step0残余知识，具有基线混杂因素。
- 目前没有跨种子置信区间或跨实体显著性分析。
- 不应声称已证明特定机器遗忘算法的因果恢复机制。
- 下一步建议扩充独立遗忘实体、重复随机种子，并检验攻击强度与模型效用之间的关系。

## 8. 原始数据来源及SHA256

| 算法 | 类型 | 相对路径 | SHA256 |
|---|---|---|---|
| RMU | Clean01 | `saves/eval/tofu_Llama-3.2-1B-Instruct_forget01_RMU_Clean01_eval/TOFU_EVAL.json` | `96fca2d39b02e0bbf968f39d196454a26cdfac6bd08013788e8864073ea43b29` |
| RMU | Attack | `saves/eval/Recovery01_Analysis03_Attack_Step20/TOFU_EVAL.json` | `e13ee4f926f6680c4c314a3a1b15d88e526dde4d368d6634b3b3997ae7e3addd` |
| RMU | Control | `saves/eval/Recovery01_Analysis03_Control_Step20/TOFU_EVAL.json` | `ec750a0960d0ac6f3f9ffce802a5d40253650af62361d2c3df6fce70ad929bf8` |
| RMU | step0 | `reports/Recovery01_Clean_RMU_QuasiIdentifier/step0_baseline.json` | `59d86758d1bb8d1be0177948c58d63461f46b8fac2583fbb9069ee3451459410` |
| RMU | recovery | `reports/Recovery01_Clean_RMU_QuasiIdentifier/recovery_checkpoint_results.json` | `42bb26e0ff0c2503858c4b943a8d535c4113b6b02ed59858076de0f4c5a709de` |
| GradDiff | Clean01 | `saves/eval/tofu_Llama-3.2-1B-Instruct_forget01_GradDiff_Clean01_eval/TOFU_EVAL.json` | `460f84a9724b85bf99dcc6b5a407ee1b3e61c14e64cec8f869760a05c93577b1` |
| GradDiff | Attack | `saves/eval/Recovery01_Extension_GradDiff_Attack_Step20/TOFU_EVAL.json` | `77f088bf7c6dc538924aa141645004f9b9a9c171fdb0b96eaac6e1898e61bd13` |
| GradDiff | Control | `saves/eval/Recovery01_Extension_GradDiff_Control_Step20/TOFU_EVAL.json` | `f7ed7b9dfe7b67b1ad4bf2d47d1a1e846038c2910205ffea200d97ab36a860ca` |
| GradDiff | step0 | `reports/Recovery01_Extension/GradDiff_step0_baseline.json` | `0e238e9953c86ca218c5255eeeff0f4aaa00e57d204f8cf539ff5e03a45e7661` |
| GradDiff | recovery | `reports/Recovery01_Extension/GradDiff_checkpoint_recovery_results.json` | `4ae03cdf0cffff014477a8d1242fd5312553fd8565afc5922dcc60f83ae068ab` |
| SimNPO | Clean01 | `saves/eval/tofu_Llama-3.2-1B-Instruct_forget01_SimNPO_Clean01_eval/TOFU_EVAL.json` | `ece1096e852a009db068b27621c3079539b741eff90f20f75d443f5d7d245620` |
| SimNPO | Attack | `saves/eval/Recovery01_Extension_SimNPO_Attack_Step20/TOFU_EVAL.json` | `a8406dd9c6cf4bcd798704c5d6a82d249ff515718698af8173b5ca8c745a5c61` |
| SimNPO | Control | `saves/eval/Recovery01_Extension_SimNPO_Control_Step20/TOFU_EVAL.json` | `fa7f04dfeffc6e07d05cf8be6a144defcd5f1a2e4d1923fa6438da22397f612a` |
| SimNPO | step0 | `reports/Recovery01_Extension/SimNPO_step0_baseline.json` | `a196efa93be6945f8d79f497c4a4fb08aa4c02287c7cd3688fc4d254f4550302` |
| SimNPO | recovery | `reports/Recovery01_Extension/SimNPO_checkpoint_recovery_results.json` | `d841971bb85a354302808b3a3a341b5688d0a7e21d8e7adb4c874de0ba9056f7` |
| GradAscent | Clean01 | `saves/eval/tofu_Llama-3.2-1B-Instruct_forget01_GradAscent_Clean01_eval/TOFU_EVAL.json` | `abc16e2f7895aadbf59e8a75e7a5671313be247210aa8452c8a9e4ffac83c11e` |
| GradAscent | Attack | `saves/eval/Recovery01_Extension_GradAscent_Attack_Step20/TOFU_EVAL.json` | `a30e7a9e99f6675af7d3b1614f4c862fb5c7c34a8e9ca5a803d2980c527e3955` |
| GradAscent | Control | `saves/eval/Recovery01_Extension_GradAscent_Control_Step20/TOFU_EVAL.json` | `0cab49508ded605c5b246bbb726ba9cd10c0e3f361835f81efcd834e873c1882` |
| GradAscent | step0 | `reports/Recovery01_Extension/GradAscent_step0_baseline.json` | `c73d4cf7bcec167dfe4837d81425d547efa4030e163bb2f3dc9c8eb435da5775` |
| GradAscent | recovery | `reports/Recovery01_Extension/GradAscent_checkpoint_recovery_results.json` | `23d14f65a3a3e5002e05e21014aa029b0b68883f29b2757b095654203564eb79` |

## 9. 已冻结阶段报告

| 算法 | 文件 | SHA256 |
|---|---|---|
| GradDiff | `reports/Recovery01_Extension/GradDiff_Stage_Report_V1.md` | `d2cab90877cd57e4ebea7191ab24e04d01fe3ad54d7d976107af3323b7170d3e` |
| SimNPO | `reports/Recovery01_Extension/SimNPO_Stage_Report_V1.md` | `9fe6363c6f356feb0f4c10138431334cd27a207af7ce6e52dedf5074b6043ef2` |
| GradAscent | `reports/Recovery01_Extension/GradAscent_Stage_Report_V1.md` | `06024e6fcbabbb5b6fe13a982de314d9608ed5a9d68e3fb10a3d9c8b3baf88ff` |

- Comparison V1 SHA256: `b251ba8702dc0192cb3ad072a5bf41a9ebfb1ae6362c52e9a54a6fed9fe8a62f`

