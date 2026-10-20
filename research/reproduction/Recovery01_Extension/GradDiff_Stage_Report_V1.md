# Recovery01-Extension — GradDiff 阶段性实验报告

## 1. 数据来源及完整性

所有来源文件已经通过 SHA256 验证；本报告不改变源文件。

| 来源 | SHA256 |
|---|---|
| Clean01 (`saves/eval/tofu_Llama-3.2-1B-Instruct_forget01_GradDiff_Clean01_eval/TOFU_EVAL.json`) | `460f84a9724b85bf99dcc6b5a407ee1b3e61c14e64cec8f869760a05c93577b1` |
| Attack (`saves/eval/Recovery01_Extension_GradDiff_Attack_Step20/TOFU_EVAL.json`) | `77f088bf7c6dc538924aa141645004f9b9a9c171fdb0b96eaac6e1898e61bd13` |
| Control (`saves/eval/Recovery01_Extension_GradDiff_Control_Step20/TOFU_EVAL.json`) | `f7ed7b9dfe7b67b1ad4bf2d47d1a1e846038c2910205ffea200d97ab36a860ca` |
| Recovery (`reports/Recovery01_Extension/GradDiff_checkpoint_recovery_results.json`) | `4ae03cdf0cffff014477a8d1242fd5312553fd8565afc5922dcc60f83ae068ab` |
| Step0 (`reports/Recovery01_Extension/GradDiff_step0_baseline.json`) | `0e238e9953c86ca218c5255eeeff0f4aaa00e57d204f8cf539ff5e03a45e7661` |

## 2. 官方聚合指标

| 指标 | Clean01 | Attack20 | Control20 | Attack-Control |
|---|---:|---:|---:|---:|
| forget_Q_A_Prob | 0.00854999 | 0.11296997 | 0.04662037 | +0.06634960 |
| forget_Q_A_ROUGE | 0.31618777 | 0.34008848 | 0.36309527 | -0.02300679 |
| retain_Q_A_ROUGE | 0.41204508 | 0.61108807 | 0.60903194 | +0.00205613 |
| model_utility | 0.47151575 | 0.56782680 | 0.58709047 | -0.01926368 |
| forget_quality | 0.40458741 | 0.16497270 | 0.40458741 | -0.23961471 |
| mia_min_k | 0.12312500 | 0.28687500 | 0.15937500 | +0.12750000 |

## 3. Forget QA 逐人物配对统计

全部 40 条问题来自两名虚构人物，每人 20 条。

| 人物组 | 问题数 | Attack-Control 平均概率差 | 中位数 | 正/平/负 |
|---|---:|---:|---:|---|
| B0 | 20 | +0.08472977 | +0.05560303 | 20/0/0 |
| N20 | 20 | +0.04796944 | +0.04074097 | 20/0/0 |
| 全部 | 40 | +0.06634960 | +0.04635620 | 40/0/0 |

## 4. Forget ROUGE 与 Retain ROUGE 的配对结果

| 指标 | Attack-Control 均值差 | 正/平/负样本数 |
|---|---:|---|
| forget_Q_A_ROUGE | -0.02300679 | 11/12/17 |
| retain_Q_A_ROUGE | +0.00205613 | 128/150/122 |

## 5. 定向身份恢复

| 目标 | Attack20-Control20 姓名 LogP 差 | Margin 差 | Attack 完整姓名命中 | Control 完整姓名命中 |
|---|---:|---:|---|---|
| B0 | +0.70536780 | -0.08575845 | False | False |
| N20 | +1.40658236 | +0.32107878 | False | False |

全部八个 Checkpoint、两个目标的完整姓名命中合计：**0/16**。

## 6. 阶段性解释与局限

- Attack 在 40/40 个遗忘问答上均具有更高的参考答案概率；该现象在两名人物中均存在。
- Forget ROUGE 并未同步改善，故不能把概率回升等同于成功生成被遗忘身份。
- Model Utility、Forget Quality 和 MIA AUC 的变化需要与对照组联合解释。
- 40 条问答仅涉及两名虚构人物，不能视为 40 个独立人物或真实患者。
- 当前结果来自一套训练配置与种子，尚不能得出跨种子的统计显著性或普适性结论。
- 后续需要比较 SimNPO、GradAscent，并考虑增加种子及独立目标人物。
