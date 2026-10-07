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
TASK_NAME="exp006_correlated_20step"

CUDA_VISIBLE_DEVICES=0 python src/train.py \
  --config-name=train.yaml \
  model=Llama-3.2-1B-Instruct \
  trainer=finetune \
  data/datasets@data.train=explicit_correlated_v1 \
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
  paths.output_dir=saves/train/exp006_correlated_20step
