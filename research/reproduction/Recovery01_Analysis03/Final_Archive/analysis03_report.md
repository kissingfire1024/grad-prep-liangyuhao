# Recovery01-Analysis03：恢复后的遗忘有效性、模型效用与隐私风险

## 1. 实验目的与范围

在已完成的 Recovery01 实验基础上，对比 RMU_Clean01、
Attack Step20 和 Control Step20 的遗忘指标、保留知识能力与成员推断风险。

本次仅分析已有官方 TOFU 评估结果，没有重新训练或重新评估模型。

## 2. 数据与方法

- Forget：TOFU forget01，40 条问答
- Holdout：TOFU holdout01，40 条 MIA 样本
- Retain：400 条评估问答
- 攻击组：20 步准标识符相关数据微调
- 对照组：20 步匹配无关数据微调
- Min-K%：k=0.4，沿用历史评估口径
- 参考日志：历史 retain99 官方评估结果
- 所有数值可通过 SOURCE_MANIFEST.json 追溯来源

## 3. 官方聚合评估结果

| 指标 | RMU | Attack | Control | Attack-Control |
|---|---:|---:|---:|---:|
| forget_Q_A_Prob | 0.031909 | 0.047141 | 0.053331 | -0.006190 |
| forget_Q_A_ROUGE | 0.236988 | 0.202926 | 0.226756 | -0.023830 |
| forget_quality | 0.164973 | 0.164973 | 0.164973 | +0.000000 |
| model_utility | 0.586851 | 0.589186 | 0.587817 | +0.001369 |
| retain_Q_A_Prob | 0.829580 | 0.802744 | 0.803594 | -0.000850 |
| retain_Q_A_ROUGE | 0.741663 | 0.676654 | 0.694219 | -0.017565 |
| mia_min_k | 0.075000 | 0.101875 | 0.105000 | -0.003125 |
| privleak | 75.980975 | 70.868014 | 70.273484 | +0.594530 |

## 4. 遗忘有效性

Forget QA Probability 相对 RMU 的变化：

- Attack：+0.015232
- Control：+0.021422

40 条 Forget 问答中，Attack 概率上升 40/40，
Control 概率上升 40/40。

**这些概率变化不等于成功生成或提取 40 条事实。**

两组对 B0/N20 姓名提取题的变化也需与其余 38 条其他问答区分。
其余 38 条可能仍涉及同两名被遗忘人物，
不能标记为 38 名非目标个体。

## 5. ROUGE 指标口径

本次确认官方 `Q_A_ROUGE.agg_value` 等于
`value_by_index` 中 `rougeL_recall` 的算术平均值，
而不是 `rougeL_f1` 的均值。

因此，官方 Recall 与辅助 F1 的变化方向可能不同，
报告及论文中不可混为一个指标。

Retain 官方 ROUGE-L Recall 相对 RMU 的变化：

- Attack：-0.065009
- Control：-0.047444

## 6. 模型效用

Model Utility：

- RMU：0.586851
- Attack：0.589186
- Control：0.587817

综合效用指标与单项 Retain ROUGE 的变化方向不必一致。
两者均应报告，不能用综合指标掩盖局部退化。

## 7. 成员推断与隐私解释

| 模型 | 原始 Min-K% AUC | 方向无关 AUC |
|---|---:|---:|
| RMU | 0.075000 | 0.925000 |
| Attack | 0.101875 | 0.898125 |
| Control | 0.105000 | 0.895000 |

方向无关 AUC 定义为 max(AUC, 1-AUC)，用于描述
当前评分在允许反转方向后的可区分性，不是隐私泄漏概率。

privleak 使用历史参考日志及特定相对变换，也不能直接
解释为患者隐私泄漏百分比。

## 8. 核心结论

20 步后续微调使 Attack 与 Control 的 Forget 标准答案概率均上升，
但没有观察到 Attack 在这一指标上稳定优于 Control。

与此同时，两组 Retain ROUGE-L Recall 均下降，表明存在一定的
保留知识文本表现退化；Min-K% 分数与 AUC 也发生变化。

结合 Recovery01 的完整姓名命中 0/16，
当前结果尚不足以证明准标识符训练实现了额外身份恢复。

## 9. 局限性

- Forget01 仅涉及两名虚构人物，不能推广为患者级隐私结论。
- 只有一个随机种子及一个恢复训练预算。
- MIA 样本规模有限，且方向反转解释依赖威胁模型。
- 数据训练属性与无关对照的匹配仍有条件性局限。
- 尚未进行跨随机种子置信区间、独立盲测和真实医疗数据验证。
- 本轮归档属于已完成实验的观察性分析，不提供显著性推断。

## 10. 可复核文件

- analysis03_summary.csv
- forget_per_sample.csv
- retain_per_sample.csv
- mia_per_sample.csv
- SOURCE_MANIFEST.json

归档不修改 Recovery01 Final_Archive、冻结协议、模型或 Checkpoint。
