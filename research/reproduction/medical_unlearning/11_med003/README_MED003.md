# MED-003 | 相同问题、不同患者事实的受控记忆实验

**目标：** 验证 MED-000E 上附加新 LoRA 后，模型是否真正利用“患者代号”区分不同患者，而非机械记忆“问题 → 答案”。

## 数据与来源

- `med003_curated_evidence.jsonl` 直接摘取前期 MED-000I 的 **10组**原文证据，涵盖 **20位患者**；答案和病历文字均未捏造或改写。
- 组别：MEDI-01/02/06/07/09/10/11/13/14/16。排除了语义等价、近似单位换算和部分有争议的病例。
- 每组为 **两位不同患者，经过标点统一后相同问题文本、不同参考答案**；错误代号只在该组内交换。
- 此次是经过前期 AI 辅助病历核对的研究预审，不等于独立临床专家确认。
- 每位患者使用1条“冲突锚点 QA”进行 MED-003 微调，再从该患者**原始 AMNESIA holdout**挑选另一条事实性 QA，作为 MED-003 的未见问答评测。它的事实可能已经暴露于完整病历。
- **重要：** 一些冲突锚点原本来自 AMNESIA 原始 holdout，此处明确把它们划到 MED-003 训练集，生成新的 MED-003 划分；不得再将这些锚点称为“未见问题”。
- MED-000E 已见过不少原始训练 QA 与患者病历，不能把 MED-000E 称为全新无接触基座。代号是此次新分配的随机合成ID，不含原患者身份信息。

## 系统需求

沿用 `~/open-unlearning` 的 `openunlearning` conda 环境，已安装 PyTorch、Transformers、PEFT、datasets、omegaconf，CUDA GPU；使用原项目 `src/data/qa.py` 的 QADataset 和现有 `configs/model/Qwen2.5-0.5B-Instruct-MED.yaml`。原始 MED-000E 权重绝不修改。

## 执行

先将本 ZIP 放到 `~/open-unlearning/` 并解压到项目根目录（不是 scripts 子目录）：

```bash
cd ~/open-unlearning
conda activate openunlearning
python - <<'PY'
from zipfile import ZipFile
with ZipFile('MED003_患者身份区分对照实验包_已校验.zip') as z:
    z.extractall('.')
print('MED003 FILES INSTALLED')
PY
python -m py_compile scripts/medical/med003_collision_memory.py
python scripts/medical/med003_collision_memory.py --prepare
```

此步创建 `reports/medical_unlearning/11_med003/med003_collision_review.csv`（20条患者事实与测试QA审计表），`med003_manifest.json`，训练和固定评测 JSONL。**无需人工重新填写已核对的数据，但建议抽查审计表。** 如果数据表或患者哈希不能与本地原文件一致，脚本会显式报错并拒绝继续。

接着：

```bash
python -u scripts/medical/med003_collision_memory.py --smoke
```

通过后：

```bash
set -o pipefail
python -u scripts/medical/med003_collision_memory.py --train \
  --note-epochs 2 --qa-epochs 12 \
  2>&1 | tee reports/medical_unlearning/11_med003/train.log
```

最后：

```bash
python -u scripts/medical/med003_collision_memory.py --eval \
  2>&1 | tee reports/medical_unlearning/11_med003/eval.log
cat reports/medical_unlearning/11_med003/med003_eval_summary.json
```

## 评测矩阵与判读

- 20位患者 × (冲突锚点已见 QA、其他 Holdout QA) × (无线索、正确代号、同组错误代号) × (MED-000E、MED-003 LoRA) = **240条模型生成回答**。
- 总计40个患者-问题实例，120个提示/模型。每组的锚点问题经统一极少数排版标点后，在MED-003训练与评测提示中对两位患者**字面完全一致**。
- `correct_code_NLL - wrong_code_NLL`：越负表示正确代号相对错误代号更有利于预测目标患者参考答案，但 **NLL 并非事实正确率**。
- 真正关键的是逐患者原文事实核查：同一道问题，在正确代号下能否输出正确患者的事实，错误代号下是否转向另一患者事实；Holdout 是否也具备相同关联；有无幻觉或病例混淆。
- 若只在锚点表现好而 Holdout 仍差，说明患者代号关联可能局限于训练的问答模板，不能声称病历事实泛化。
- 本阶段是小样本、经过筛选的*正对照实验*，不可直接写成临床数据患者级遗忘的全面性能结论。即使通过，也需要扩大预注册测试集并检验忘记患者、保留他人的目标。

## 文件保护

- 模型输出：`saves/train/MED003_CollisionTagged20_LoRA`（独立新目录）。
- 训练与评测路径为 `reports/medical_unlearning/11_med003/`。
- `--prepare`、`--train`、`--eval` 遇到自己的既有输出会拒绝覆盖；先归档旧结果，再开始不同种子实验。
- 不会覆盖 MED-000D、MED-000E、MED-002 的模型权重或历史结果。
