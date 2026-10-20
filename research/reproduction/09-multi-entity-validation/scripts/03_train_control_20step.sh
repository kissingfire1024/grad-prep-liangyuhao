#!/usr/bin/env bash
set -euo pipefail

cd /home/research/open-unlearning

source ~/miniconda3/etc/profile.d/conda.sh
conda activate openunlearning

export CUDA_HOME=/usr/local/cuda-12.1
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:${LD_LIBRARY_PATH:-}
export HF_HUB_DISABLE_XET=1

ROOT="/home/research/research/reproduction/09-multi-entity-validation"

RMU_CKPT="/home/research/open-unlearning/saves/unlearn/tofu_Llama-3.2-1B-Instruct_forget10_RMU_exp009"

DATA_FILE="${ROOT}/data/control_masked_v3.json"
PROTOCOL="${ROOT}/notes/recovery_training_protocol_v1.md"

EXPECTED_DATA_SHA="edb0db3629f21a41d4d7fb91a531546784da1c7285a291e96e0e2e04c2c99511"
EXPECTED_PROTOCOL_SHA="73a29bf6871c9381ce94ec97ac0bd582d2ea41b9dc16eae93206ebf5f729831f"

ACTUAL_DATA_SHA=$(sha256sum "${DATA_FILE}" | awk '{print $1}')
ACTUAL_PROTOCOL_SHA=$(sha256sum "${PROTOCOL}" | awk '{print $1}')

echo "================================================================================"
echo "EXP009 — FORMAL MATCHED CONTROL RECOVERY TRAINING"
echo "================================================================================"

echo "RMU Step0:"
echo "${RMU_CKPT}"

echo
echo "Dataset SHA"
echo " expected: ${EXPECTED_DATA_SHA}"
echo " actual  : ${ACTUAL_DATA_SHA}"

echo
echo "Protocol SHA"
echo " expected: ${EXPECTED_PROTOCOL_SHA}"
echo " actual  : ${ACTUAL_PROTOCOL_SHA}"

if [ "${ACTUAL_DATA_SHA}" != "${EXPECTED_DATA_SHA}" ]; then
    echo "ERROR: frozen Control dataset hash mismatch."
    exit 1
fi

if [ "${ACTUAL_PROTOCOL_SHA}" != "${EXPECTED_PROTOCOL_SHA}" ]; then
    echo "ERROR: frozen training protocol hash mismatch."
    exit 1
fi

if [ ! -d "${RMU_CKPT}" ]; then
    echo "ERROR: RMU Step0 checkpoint missing."
    exit 1
fi

# ------------------------------------------------------------
# Create Control dataset config from the already-working
# Exp009 Quasi config. Change ONLY data_files.
# ------------------------------------------------------------

SRC_CFG="configs/data/datasets/exp009_quasi_identifier_v3.yaml"
DST_CFG="configs/data/datasets/exp009_control_masked_v3.yaml"

if [ ! -f "${SRC_CFG}" ]; then
    echo "ERROR: Exp009 Quasi dataset config missing:"
    echo "${SRC_CFG}"
    exit 1
fi

cp "${SRC_CFG}" "${DST_CFG}"

python - <<'PY'
from pathlib import Path

p=Path("configs/data/datasets/exp009_control_masked_v3.yaml")

s=p.read_text()

old=(
    "/home/research/research/reproduction/"
    "09-multi-entity-validation/data/"
    "quasi_identifier_masked_v3.json"
)

new=(
    "/home/research/research/reproduction/"
    "09-multi-entity-validation/data/"
    "control_masked_v3.json"
)

if old not in s:
    raise RuntimeError(
        "Expected Quasi path not found in copied config."
    )

p.write_text(s.replace(old,new))

print("Control dataset config:")
print("-"*80)
print(p.read_text())
PY

TASK_NAME="exp009_control_20step_formal"
OUT="saves/train/${TASK_NAME}"

if [ -e "${OUT}" ]; then
    echo "ERROR: formal Control output already exists:"
    echo "${OUT}"
    echo "Do not overwrite a formal trajectory."
    exit 1
fi

echo
echo "Frozen inputs: PASS"
echo "Formal endpoint: 20 optimizer steps"
echo
echo "IMPORTANT:"
echo "  Control starts independently from RMU Step0."
echo "  It does NOT start from the Quasi model."
echo "  It does NOT start from the engineering probe."
echo "  No heldout evaluation occurs during training."
echo "================================================================================"

CUDA_VISIBLE_DEVICES=0 python src/train.py \
  --config-name=train.yaml \
  model=Llama-3.2-1B-Instruct \
  trainer=finetune \
  data/datasets@data.train=exp009_control_masked_v3 \
  task_name="${TASK_NAME}" \
  model.model_args.pretrained_model_name_or_path="${RMU_CKPT}" \
  model.tokenizer_args.pretrained_model_name_or_path="${RMU_CKPT}" \
  model.model_args.attn_implementation=sdpa \
  trainer.args.per_device_train_batch_size=1 \
  trainer.args.per_device_eval_batch_size=1 \
  trainer.args.gradient_accumulation_steps=4 \
  trainer.args.learning_rate=1e-5 \
  trainer.args.gradient_checkpointing=true \
  trainer.args.weight_decay=0.01 \
  trainer.args.logging_steps=1 \
  +trainer.args.max_steps=20 \
  trainer.args.save_strategy=no \
  trainer.args.eval_strategy=no \
  trainer.args.do_eval=false \
  ~eval \
  paths.output_dir="${OUT}"

echo
echo "================================================================================"
echo "FORMAL CONTROL OUTPUT:"
echo "${OUT}"
echo
echo "STATUS: EXP009_FORMAL_CONTROL_20STEP_TRAINING_COMPLETE"
echo "IMPORTANT: DO NOT RUN HELDOUT EVALUATION YET"
echo "================================================================================"
