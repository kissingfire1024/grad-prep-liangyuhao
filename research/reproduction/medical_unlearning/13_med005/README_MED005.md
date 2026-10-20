# MED-005：身份排序与医学知识保留（Retain Replay）受控对照

## 目的

MED-004 排序损失在4组真实病例锚点上建立了条件化答案区分，但同患者Holdout问答出现严重退化。本实验检验：在**完全相同**的病例、起始权重、种子、优化器、96个优化步骤和排序损失系数下，加入患者互不重叠的Retain QA重放，能否缓解知识损伤。

**本实验不是机器遗忘**。只评估起始模型患者代号关联和保留知识的折衷；不声称可验证真实身份泄露、完全患者记忆或方法的泛化有效性。

## 预备条件

- 在 `~/open-unlearning` 运行，已完成 MED-004 `--prepare`、双模型训练及 `--eval`。
- `scripts/medical/med004_identity_rank.py` 保留为原版本，本脚本直接导入其统一问答模板、LoRA和NLL方法，不修改 MED-004。
- MED-000E 权重存在；Python环境中安装 `peft`, `transformers`, `torch`, `datasets`, `omegaconf`。
- 保留真实AMNESIA文件：`train_sft_qa.jsonl`, `eval_same_disease.jsonl`, `eval_other_disease.jsonl`。

## 运行

```bash
conda activate openunlearning
cd ~/open-unlearning
python -m py_compile scripts/medical/med005_retain_replay.py
python scripts/medical/med005_retain_replay.py --prepare
python scripts/medical/med005_retain_replay.py --smoke

set -o pipefail
python -u scripts/medical/med005_retain_replay.py --train --arm rank_only --epochs 24 \
  2>&1 | tee reports/medical_unlearning/13_med005/train_rank_only.log
python -u scripts/medical/med005_retain_replay.py --train --arm rank_replay --epochs 24 \
  2>&1 | tee reports/medical_unlearning/13_med005/train_rank_replay.log
python -u scripts/medical/med005_retain_replay.py --eval \
  2>&1 | tee reports/medical_unlearning/13_med005/eval.log

cat reports/medical_unlearning/13_med005/med005_eval_summary.json
```

## 固定实验方案

- 身份锚点：MED-004 的4组相同问题、8位患者、8条QA（仅训练锚点）。
- 评测：MED-004 冻结的8条同患者Holdout问题、3种代号条件。
- Retain Replay：96位不属于8位身份任务患者的同病种Retain患者，每人1条原始训练QA，固定顺序、每步用1条，96步各用一次。
- 外部Retain评测：另外96位同病种Retain患者的Holdout QA，以及96位其他病种患者的Holdout QA。训练Retain和评测Retain**患者不重叠**；但原始MED-000E曾接触这些患者数据。
- 双实验臂： `rank_only` = CE + 3.0 Ranking； `rank_replay` = CE + 3.0 Ranking + 1.0 Replay CE。均从MED-000E启动，seed=42，lr=2e-4，24 epochs × 4组=96 optimizer steps。无新增病历预训练。
- 额外比较：读取MED-004已经冻结的 MED000E、CE、Ranking 原始锚点评测结果；对外部保留数据统一重新评分5个模型。

## 输出

`reports/medical_unlearning/13_med005/`：

- `med005_manifest.json`：抽样方案及依赖数据SHA256。
- `med005_replay_train.jsonl`、`med005_retain_eval.jsonl`：训练与评测QA。
- `med005_rank_only_train_log.json`、`med005_rank_replay_train_log.json`。
- `med005_eval_predictions.csv`：MED004基线和MED005两模型，5模型 ×48个身份任务提示=240条。
- `med005_identity_matrix.csv`：每个模型各4组的患者交叉评分和实际生成。
- `med005_retain_nll_by_qa.csv`：5模型×192 Retain评测QA=960条。
- `med005_paired_retain_bootstrap.csv`：按患者成对重采样的Retain NLL变化95%区间（探索性）。
- `med005_eval_summary.json`：各分组平均指标与上述对照。

模型只新建：

- `saves/train/MED005_RANK_ONLY_LoRA`
- `saves/train/MED005_RANK_REPLAY_LoRA`

不会覆盖MED-000E/MED-004。已存在输出时拒绝覆盖；`--prepare`在来源和参数不变时可以复用。

## 结果判读

核心同时检查：（1）正确代号下的4组双向身份排序与病例事实准确性；（2）8条Holdout QA相对于原始MED000E的变化；（3）同病种Retain患者Holdout NLL和95%配对区间；（4）其他病种Retain NLL；（5）是否产生无意义、重复、严重幻觉输出。

最重要的是判断 **Rank + Replay 相对 Rank-only** 是否在不明显牺牲身份区分的情况下改善知识保留。不能只挑最低Holdout NLL模型；若要调超参数，应该另设验证病例，不要反复用同8条Holdout选优。研究正式结论需要扩大病例、跨随机种子和独立医生事实核查。

注意 `Sliding Window Attention ... sdpa` 属Transformers既有提示；`temperature/top_p`与贪婪解码不匹配属于配置警告，通常不阻断实验。
