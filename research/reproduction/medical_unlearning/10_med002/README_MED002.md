# MED-002：患者条件化记忆 Pilot（16位患者）

## 为什么做
MED-000E 在医疗 QA NLL 上显著提升，但原问题或非答案病历线索下无法可靠恢复关键患者事实。此实验不修改 MED-000E，训练一个新 LoRA 分支学习“合成患者代号→该患者病历及问答”。

## 研究设计与限制

- 使用已审阅的16位患者：8 Forget、8 同病种 Retain；每位患者固定 Train QA 和 Holdout QA。它们从之前的 MED-000L-2 评测集中选出，并非新独立抽样。
- **新训练集**取自 `data/medical/amnesia_cv5/train_sft_qa.jsonl` 中这16人的所有已有训练QA，并取经确认的对应 `patient_note`，切分成可监督学习的病历段。**不直接使用 Holdout QA 的问答对训练**。
- **但Holdout问题对应的事实可能已经在训练病历中**，所以这里的Holdout是“未见问法”，不是“未见事实”也不是“未见患者”。
- 使用不含疾病/组别语义的稳定人工代号 `CASE_XXXX`，同一患者所有训练问答都带这一代号。错误代号在**相同患者组**内轮换，避免完全不同疾病类别导致的简单区分。
- 输入条件：Question-only / Correct code / Wrong code。对比未适配的MED-000E与MED-002，输出**参考答案NLL和自由生成**。
- **不能仅靠 NLL 或 tag 识别证明真实患者记忆/泄露**。需要回到原病历审阅模型的事实准确性。合成代号只证明受控索引条件下的可提取关联能力，不能代表真实临床身份识别。
- 这个16患者Pilot会明显过拟合；阳性结果仅作为后续更大、患者独立评测和防过拟合对照的依据，不能直接当作论文主要结论。

## 文件安装

从 ZIP 解压到 `~/open-unlearning` 根目录。脚本为 `scripts/medical/med002_patient_memory.py`。原模型 `saves/train/MED000E_QAFull_E1_Qwen05` 不会被覆盖；适配器保存到 `saves/train/MED002_TaggedPatient16_LoRA`。

## 运行步骤

```bash
cd ~/open-unlearning
conda activate openunlearning
python -m py_compile scripts/medical/med002_patient_memory.py
python scripts/medical/med002_patient_memory.py --prepare
cat reports/medical_unlearning/10_med002/med002_manifest.json
python -u scripts/medical/med002_patient_memory.py --smoke
# 通过Smoke后执行LoRA训练；先用轻量Pilot配置，不进行反复调参
set -o pipefail
python -u scripts/medical/med002_patient_memory.py --train --note-epochs 2 --qa-epochs 6 2>&1 | tee reports/medical_unlearning/10_med002/train.log
python -u scripts/medical/med002_patient_memory.py --eval 2>&1 | tee reports/medical_unlearning/10_med002/eval.log
```

如果发现 `peft` 缺失，先执行 `python -c 'import peft, transformers, datasets; print("dependencies OK")'` 核查，再决定是否在当前conda环境安装兼容版本。

## 验收要求

1. `--prepare` 输出16人，Forget 8/Retain 8，32条固定问题、96个条件提示；Holdout QA ID不在全量QA训练集中。
2. `--smoke` 对病历和QA各一次forward/backward成功，不保存权重。
3. `--train` 输出非NaN损失，生成完整的LoRA `adapter_config.json`、`adapter_model.safetensors`及训练日志。
4. `--eval` 保存 `med002_eval_predictions.csv`（2模型×32问题×3条件=192条）与 `med002_eval_summary.json`。
5. 临床证据核查后，重点看Forget和Retain的 **Holdout** 是否有完整正确的病历特异性回答，以及CorrectCode优于WrongCode的差异是否来自新训练。不能把训练问答记住而Holdout回答错误视为成功。

## 不同于旧实验

- 旧MED-000E不具备已验证的患者身份定位能力；MED-002专门让模型在训练中学习合成代号。
- 这个实验并不能证明代码/研究方法创新，仅验证患者条件化训练是否能生成可以评价遗忘的目标记忆。
- 后续正式版要扩展到更多患者、用患者级不交叉切分和固定预注册评测，加入相同训练预算下的无代号/不含病历适配对照，再研究遗忘算法和恢复攻击。

## 注意事项

- 采用存在性保护：脚本不会覆盖已有的训练文件、LoRA适配器或评测CSV。要重做请先备份对应文件夹，创建新的实验编号，而不是直接删除旧实验。
- 在Windows资源管理器打开 `\\wsl.localhost\Ubuntu\home\research\open-unlearning\reports\medical_unlearning\10_med002`；不要在Ubuntu shell中执行UNC路径。
