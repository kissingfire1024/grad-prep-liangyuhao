# MED-004 | Patient identity ranking positive-control

## Goal

Determine if identity-conditioned learning can make a small medical QA model map **the same documented clinical question** to **different patients' documented answers**. An ordinary QA/SFT arm (CE) and a contrastive-ranking arm (RANK) start from identical original MED-000E weights, with the same 8 patient anchor QA, learning rate, epoch count, seed, and 4 optimizer updates per epoch. RANK adds explicit pressure to lower the reference-answer NLL under the correct patient code relative to the other patient's code.

**This is not a patient privacy, machine unlearning or clinically validated benchmark.** It tests whether the training procedure can associate synthetic case codes with anchor facts. MED-003 inputs were cherry-picked and AI-audited; clinical expert verification is outstanding.

### Exact training inputs

- MED-003 frozen source `reports/medical_unlearning/11_med003/med003_eval_fixed.jsonl` (120 records)
- Four fixed documented anchor groups `MEDI-01,MEDI-02,MEDI-09,MEDI-10` (eight patients)
- Two distinct true anchor reference answers per group
- **No patient-note training during MED-004**, so it isolates association on anchor QA and cannot itself teach untrained heldout facts. MED-000E had earlier seen patient notes.
- Heldout questions are reserved for evaluation only; they include factual and reasoning examples and should be reported separately.

### Objective

For each anchor answer `y_i`, calculate mean teacher-forced answer-token NLL under the correct code `c_i` and the other code `c_j`:

```
advantage_i = NLL(y_i | wrong_code=c_j, q) - NLL(y_i | correct_code=c_i, q)
L_rank = mean(softplus(margin - advantage_i))
L_total = mean(NLL(y_i | c_i, q)) + lambda * L_rank
```

CE-only optimizes the first term alone. Same patients and same optimizer step budget; RANK needs additional forward passes.

### Installation

Unzip the package at the root of `~/open-unlearning`. Files go into `scripts/medical/` and `reports/medical_unlearning/12_med004/`. This package **does not overwrite MED-003** code, models or data.

### Commands

```bash
conda activate openunlearning
cd ~/open-unlearning
python -m py_compile scripts/medical/med004_identity_rank.py
python scripts/medical/med004_identity_rank.py --prepare
python scripts/medical/med004_identity_rank.py --smoke

set -o pipefail
python -u scripts/medical/med004_identity_rank.py --train --arm ce --epochs 24 \
  2>&1 | tee reports/medical_unlearning/12_med004/train_ce.log
python -u scripts/medical/med004_identity_rank.py --train --arm rank --epochs 24 \
  2>&1 | tee reports/medical_unlearning/12_med004/train_rank.log
python -u scripts/medical/med004_identity_rank.py --eval \
  2>&1 | tee reports/medical_unlearning/12_med004/eval.log
```

### Output

- `saves/train/MED004_Identity_CE_LoRA/` and `saves/train/MED004_Identity_RANK_LoRA/` (the two adapters)
- `reports/medical_unlearning/12_med004/med004_eval_predictions.csv`: 144 generation records (3 models x 8 patients x 2 QA x 3 conditions)
- `med004_anchor_identity_matrix.csv`: 12 model-group rows with reference-token rank matrix and model-generated responses under code swapping
- `med004_eval_summary.json`: aggregate NLL and patient-code ranking

### What counts as success

Under patient code A, probability of patient A's answer should exceed B's and vice versa **within each collision pair**; free generated answers should also correctly switch and match each patient's documented facts. Under wrong patient codes, the model should avoid copying the wrong patient's fact. The CE vs RANK contrast should outperform on held-out group IDs if scaling; the current 4-group study is a targeted positive control only. Even a successful anchor result is **not evidence of general patient-note recall, de-identification, or medical machine unlearning**.

### Safety/checkpoints

- Preparation refuses to overwrite outputs, and stores a SHA-256 of the immutable MED003 source.
- Each training arm refuses to overwrite existing adapter or log.
- Evaluation refuses to overwrite previous predictions.
- A smoke test verifies that correct/wrong codes change the input tokens and that case codes appear before answer tokens.
- For a full-size experiment, expand groups only with a **new destination/outdir or archived run**, and pre-register heldout evaluation.
