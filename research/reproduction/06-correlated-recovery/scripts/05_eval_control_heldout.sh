#!/usr/bin/env bash
set -euo pipefail

cd /home/research/open-unlearning

source ~/miniconda3/etc/profile.d/conda.sh
conda activate openunlearning

CKPT="/home/research/open-unlearning/saves/train/exp006_control_20step"
OUT="/home/research/research/reproduction/06-correlated-recovery/results/control_20step_heldout"

CUDA_VISIBLE_DEVICES=0 python src/eval.py \
  eval=heldout_recovery_screen \
  model=Llama-3.2-1B-Instruct \
  model.model_args.pretrained_model_name_or_path="${CKPT}" \
  model.tokenizer_args.pretrained_model_name_or_path="${CKPT}" \
  model.model_args.attn_implementation=sdpa \
  task_name=exp006_control_20step_heldout \
  eval.tofu.output_dir="${OUT}"
