#!/bin/bash
set -e

cd ~/open-unlearning

source ~/miniconda3/etc/profile.d/conda.sh
conda activate openunlearning

export CUDA_HOME=/usr/local/cuda-12.1
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:${LD_LIBRARY_PATH:-}

# WSL -> Windows proxy
WSL_HOST=$(ip route | awk '/default/ {print $3}')
export HTTP_PROXY=http://${WSL_HOST}:7897
export HTTPS_PROXY=http://${WSL_HOST}:7897

export HF_HUB_DISABLE_XET=1

CUDA_VISIBLE_DEVICES=0 python src/eval.py \
  eval=heldout_recovery_screen \
  task_name=exp006_RMU_step0_heldout \
  model=Llama-3.2-1B-Instruct \
  model.model_args.pretrained_model_name_or_path=saves/unlearn/tofu_Llama-3.2-1B-Instruct_forget01_RMU_test \
  model.tokenizer_args.pretrained_model_name_or_path=saves/unlearn/tofu_Llama-3.2-1B-Instruct_forget01_RMU_test \
  model.model_args.attn_implementation=sdpa \
  paths.output_dir=/home/research/research/reproduction/06-correlated-recovery/results/rmu_step0_heldout
