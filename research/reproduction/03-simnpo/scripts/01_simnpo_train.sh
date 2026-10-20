# WSL -> Windows proxy
WSL_HOST=$(ip route | awk '/default/ {print $3}')
export HTTP_PROXY=http://${WSL_HOST}:7897
export HTTPS_PROXY=http://${WSL_HOST}:7897#!/bin/bash
set -e

# Experiment 003
# OpenUnlearning + TOFU forget01 + SimNPO
# GPU: RTX 4070 SUPER 12GB
#
# SimNPO:
# beta = 4.5
# gamma = 0.125
# delta = 0.0
# alpha = 1.0
# retain_loss_type = NLL

cd ~/open-unlearning

source ~/miniconda3/etc/profile.d/conda.sh
conda activate openunlearning

export CUDA_HOME=/usr/local/cuda-12.1
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:${LD_LIBRARY_PATH:-}
export HF_HUB_DISABLE_XET=1

CUDA_VISIBLE_DEVICES=0 accelerate launch \
  --config_file configs/accelerate/single_gpu.yaml \
  src/train.py \
  --config-name=unlearn.yaml \
  experiment=unlearn/tofu/default.yaml \
  trainer=SimNPO \
  task_name=tofu_Llama-3.2-1B-Instruct_forget01_SimNPO_test \
  model=Llama-3.2-1B-Instruct \
  forget_split=forget01 \
  retain_split=retain99 \
  model.model_args.pretrained_model_name_or_path=open-unlearning/tofu_Llama-3.2-1B-Instruct_full \
  model.tokenizer_args.pretrained_model_name_or_path=open-unlearning/tofu_Llama-3.2-1B-Instruct_full \
  model.model_args.attn_implementation=sdpa \
  trainer.args.per_device_train_batch_size=1 \
  trainer.args.gradient_accumulation_steps=4 \
  trainer.args.gradient_checkpointing=true \
  trainer.args.do_eval=false \
  trainer.args.eval_on_start=false \
  trainer.args.eval_strategy=no
