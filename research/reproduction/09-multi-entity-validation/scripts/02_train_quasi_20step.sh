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

DATA_FILE="${ROOT}/data/quasi_identifier_masked_v3.json"
PROTOCOL="${ROOT}/notes/recovery_training_protocol_v1.md"

EXPECTED_DATA_SHA="c60a2720057b0574e99b3bec5f18dedaf468fac24212b949cde26d74d1c0e8a6"
EXPECTED_PROTOCOL_SHA="73a29bf6871c9381ce94ec97ac0bd582d2ea41b9dc16eae93206ebf5f729831f"

ACTUAL_DATA_SHA=$(sha256sum "${DATA_FILE}" | awk '{print $1}')
ACTUAL_PROTOCOL_SHA=$(sha256sum "${PROTOCOL}" | awk '{print $1}')

echo "================================================================================"
echo "EXP009 — FORMAL QUASI RECOVERY TRAINING"
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
    echo "ERROR: frozen Quasi dataset hash mismatch."
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

echo
echo "Frozen inputs: PASS"
echo "Formal endpoint: 20 optimizer steps"
echo
echo "IMPORTANT:"
echo "  This run starts independently from RMU Step0."
echo "  The engineering probe is NOT used."
echo "  No heldout recovery evaluation occurs during training."
echo "================================================================================"

TASK_NAME="exp009_quasi_20step_formal"
OUT="saves/train/${TASK_NAME}"

# Avoid silently mixing with an old formal run.
if [ -e "${OUT}" ]; then
    echo "ERROR: formal output already exists:"
    echo "${OUT}"
    echo "Do not overwrite a formal trajectory."
    exit 1
fi

CUDA_VISIBLE_DEVICES=0 python src/train.py \
  --config-name=train.yaml \
  model=Llama-3.2-1B-Instruct \
  trainer=finetune \
  data/datasets@data.train=exp009_quasi_identifier_v3 \
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
echo "FORMAL QUASI OUTPUT:"
echo "${OUT}"
echo
echo "STATUS: EXP009_FORMAL_QUASI_20STEP_TRAINING_COMPLETE"
echo "IMPORTANT: DO NOT RUN HELDOUT EVALUATION YET"
echo "================================================================================"
