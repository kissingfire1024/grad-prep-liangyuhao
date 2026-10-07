#!/bin/bash
set -e

# Experiment 004 preflight
# RMU memory feasibility probe
# NOT a formal experiment result.
#
# Hardware:
# NVIDIA RTX 4070 SUPER 12GB
#
# OpenUnlearning RMU defaults:
# gamma = 1.0
# alpha = 1.0
# steering_coeff = 2
# retain_loss_type = EMBED_DIFF
# module_regex = model.layers.7
# trainable_params_regex = .*
#
# Only ONE optimization step is executed.

# WSL -> Windows proxy
WSL_HOST=$(ip route | awk '/default/ {print $3}')
export HTTP_PROXY=http://${WSL_HOST}:7897
export HTTPS_PROXY=http://${WSL_HOST}:7897

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
  trainer=RMU \
  task_name=tofu_Llama-3.2-1B-Instruct_forget01_RMU_memory_probe \
  model=Llama-3.2-1B-Instruct \
  forget_split=forget01 \
  retain_split=retain99 \
  model.model_args.pretrained_model_name_or_path=open-unlearning/tofu_Llama-3.2-1B-Instruct_full \
  model.tokenizer_args.pretrained_model_name_or_path=open-unlearning/tofu_Llama-3.2-1B-Instruct_full \
  model.model_args.attn_implementation=sdpa \
  trainer.args.per_device_train_batch_size=1 \
  trainer.args.gradient_accumulation_steps=4 \
  trainer.args.gradient_checkpointing=true \
  +trainer.args.max_steps=1 \
  trainer.args.num_train_epochs=1 \
  trainer.args.do_eval=false \
  trainer.args.eval_on_start=false \
  trainer.args.eval_strategy=no
