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

EXPECTED_SHA256="c60a2720057b0574e99b3bec5f18dedaf468fac24212b949cde26d74d1c0e8a6"

ACTUAL_SHA256=$(sha256sum "${DATA_FILE}" | awk '{print $1}')

if [ "${ACTUAL_SHA256}" != "${EXPECTED_SHA256}" ]; then
    echo "ERROR: frozen Quasi dataset hash mismatch."
    exit 1
fi

if [ ! -d "${RMU_CKPT}" ]; then
    echo "ERROR: RMU checkpoint not found:"
    echo "${RMU_CKPT}"
    exit 1
fi

TASK_NAME="exp009_quasi_1step_engineering_probe"

echo "================================================================"
echo "EXP009 — QUASI 1-STEP ENGINEERING PROBE"
echo "================================================================"
echo "RMU checkpoint : ${RMU_CKPT}"
echo "Dataset        : ${DATA_FILE}"
echo "Dataset SHA256 : ${ACTUAL_SHA256}"
echo
echo "NO HELDOUT EVALUATION WILL BE RUN."
echo "THIS IS NOT A FORMAL RECOVERY OUTCOME."
echo "================================================================"

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
  +trainer.args.max_steps=1 \
  trainer.args.save_strategy=no \
  trainer.args.eval_strategy=no \
  trainer.args.do_eval=false \
  ~eval \
  paths.output_dir=saves/train/exp009_quasi_1step_engineering_probe

echo
echo "================================================================"
echo "STATUS: EXP009_QUASI_1STEP_ENGINEERING_PROBE_COMPLETE"
echo "IMPORTANT: NO HELDOUT RECOVERY EVALUATION PERFORMED"
echo "================================================================"
