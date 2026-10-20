# MED-006：患者身份区分—医学知识保留折衷试验

## 重要背景

MED-004: `lambda=3, beta=0` 的 Ranking 在4组训练锚点双向排序 4/4，但8条同患者 Holdout NLL≈5.0095。

MED-005: `lambda=3, beta=1` 的 Ranking + Replay 仍为4/4，96位同病种 Retain NLL≈1.9311（MED-000E 为1.8574），96位其他病种 Retain NLL≈1.9503（MED-000E 为1.8685）。8条 Holdout NLL≈2.4385。上述统计是已经观察到的开发结果，不是MED-006的独立验证结果。

## 设计与防数据复用

* 冻结 MED-004 的4组真实身份冲突QA、8位患者及8条原有同患者Holdout问答；所有新模型从 `MED000E_QAFull_E1_Qwen05` 出发，不从MED-004/005后续权重继续训练。
* 冻结 MED-005 的96条同病种 Retain Replay，每步1条，24轮×4组=96优化步。
* 使用此前已经观察结果的192位 MED-005 Retain患者中的96位（各病种48位）作为 **development/validation**；不再视其为独立新测试。
* 从 AMNESIA 的其余患者中额外抽取**新的96位患者（同病种48、其他病种48）**作为一次性 Retain Test，排除所有身份锚点患者、MED-005 Replay患者和MED-005 Retain评测患者。患者间不重叠。
* 不使用那8条已经在MED-004/005多次查看过的Holdout问答来选择权重或检查点；最终仅作为探索性跨问题诊断，不是新的盲测集。
* 上述 Test 患者很可能已经参加MED-000E原始训练。**它们不是原始模型的患者独立外部测试**，只是在MED-006微调/选参阶段没有再次使用。

## 三组新训练配置

| 实验臂 | Ranking系数 λ | Replay系数 β | 训练Epoch | 步数 | 保存检查点 |
|---|---:|---:|---:|---:|---|
| L1_B1 | 1 | 1 | 24 | 96 | 12/24 |
| L2_B1 | 2 | 1 | 24 | 96 | 12/24 |
| L3_B2 | 3 | 2 | 24 | 96 | 12/24 |

另用已有MED-005 `L3_B1_E24` 作为第7个候选。选参时以4组**训练锚点**全部通过双向身份概率排序作为必要条件，然后最小化两类Dev Retain的**最坏平均NLL增幅**（相对于MED-000E）。这是一项谨慎的工程筛选规则；锚点不是身份泛化验证集，不能据此声称未见患者身份成功。

## Ubuntu WSL 操作

将包解压到 `~/open-unlearning`，确保依赖 `med004_identity_rank.py`、`med005_retain_replay.py` 和以前的归档仍在原位置。

```bash
conda activate openunlearning
cd ~/open-unlearning
python -m py_compile scripts/medical/med006_joint_ablation.py
python -u scripts/medical/med006_joint_ablation.py --prepare
python -u scripts/medical/med006_joint_ablation.py --smoke

set -o pipefail
for arm in L1_B1 L2_B1 L3_B2; do
    python -u scripts/medical/med006_joint_ablation.py --train --arm "$arm" \
        2>&1 | tee "reports/medical_unlearning/14_med006/train_${arm}.log" || exit 1
done

python -u scripts/medical/med006_joint_ablation.py --validate \
    2>&1 | tee reports/medical_unlearning/14_med006/validate.log
python -u scripts/medical/med006_joint_ablation.py --select
cat reports/medical_unlearning/14_med006/med006_selection.json

# 只有 SELECTION FROZEN 且决策允许时执行一次新的测试
python -u scripts/medical/med006_joint_ablation.py --test \
    2>&1 | tee reports/medical_unlearning/14_med006/test.log
```

## 输出

* `med006_manifest.json`: 数据来源SHA256和注意事项
* `med006_retain_dev.jsonl`、`med006_retain_test.jsonl`: 患者级划分
* `med006_L*_train_log.json`, `saves/train/MED006_*_E12_LoRA` 与 `..._E24_LoRA`: 不会覆盖旧模型
* `med006_validation_summary.csv` 与 `med006_validation_by_qa.csv`: 基于旧Retain Dev的候选模型结果
* `med006_selection.json`: 在查看新的Test结果**之前**冻结最优模型
* `med006_test_summary.json`, `med006_test_retain_by_qa.csv`, `med006_test_holdout_generations.csv`: 新Retain评测与旧Holdout探索性生成

## 科研解释约束

1. 即使验证集表现改善且训练锚点身份排序4/4，也**不能宣称**对新患者的身份关联泛化。
2. 只有8条已经多次查看过的同患者Holdout题，本轮不用于选择模型；单靠其结果不能证明跨问题患者事实记忆。
3. 只保存Retain NLL，并不等于医学事实正确率；应使用独立病例原文及专家审核补充生成评测。
4. 所有训练组具有相同优化步数，但不同损失项意味着每步计算成本不完全一致。
5. 本轮是构建机器遗忘起始模型的正对照，不是机器遗忘算法实验或医学隐私保证。
