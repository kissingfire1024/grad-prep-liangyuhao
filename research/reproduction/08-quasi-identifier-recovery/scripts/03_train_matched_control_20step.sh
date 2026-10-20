#!/usr/bin/env bash
set -euo pipefail

cd /home/research/open-unlearning

source ~/miniconda3/etc/profile.d/conda.sh
conda activate openunlearning

export CUDA_HOME=/usr/local/cuda-12.1
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:${LD_LIBRARY_PATH:-}

WSL_HOST=$(ip route | awk '/default/ {print $3}')
export HTTP_PROXY=http://${WSL_HOST}:7897
export HTTPS_PROXY=http://${WSL_HOST}:7897

export HF_HUB_DISABLE_XET=1

RMU_CKPT="/home/research/open-unlearning/saves/unlearn/tofu_Llama-3.2-1B-Instruct_forget01_RMU_test"

DATA_FILE="/home/research/research/reproduction/08-quasi-identifier-recovery/data/matched_unrelated_control_v1.json"

EXPECTED_SHA256="9e0f1e158e87e37adee4931e13791f09b47f390e829837d7d2676e179b8d41f0"

ACTUAL_SHA256=$(sha256sum "${DATA_FILE}" | awk '{print $1}')

echo "================================================================"
echo "EXP008 — MATCHED UNRELATED CONTROL"
echo "================================================================"
echo "RMU checkpoint : ${RMU_CKPT}"
echo "Dataset        : ${DATA_FILE}"
echo "Expected SHA256: ${EXPECTED_SHA256}"
echo "Actual SHA256  : ${ACTUAL_SHA256}"
echo

if [ "${ACTUAL_SHA256}" != "${EXPECTED_SHA256}" ]; then
    echo "ERROR: Frozen control dataset hash mismatch."
    exit 1
fi

echo "Frozen dataset integrity: PASS"
echo
echo "Starting matched-control 20-step training..."
echo "================================================================"

TASK_NAME="exp008_matched_control_20step"

CUDA_VISIBLE_DEVICES=0 python src/train.py \
  --config-name=train.yaml \
  model=Llama-3.2-1B-Instruct \
  trainer=finetune \
  data/datasets@data.train=exp008_matched_control_v1 \
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
  paths.output_dir=saves/train/exp008_matched_control_20step

echo
echo "================================================================"
echo "STATUS: EXP008_MATCHED_CONTROL_TRAINING_COMPLETE"
echo "================================================================"
