#!/usr/bin/env bash
set -euo pipefail

cd /home/research/open-unlearning

CKPT="saves/train/tofu_Llama-3.2-1B-Instruct_forget01_RMU_relearn_50step_continuous/relearn-step-20"

CUDA_VISIBLE_DEVICES=0 python src/eval.py \
  --config-name=eval.yaml \
  eval=tofu_recovery_screen \
  eval.tofu.forget_split=forget01 \
  eval.tofu.holdout_split=holdout01 \
  task_name=tofu_RMU_relearn_continuous_step20_screen \
  model=Llama-3.2-1B-Instruct \
  model.model_args.pretrained_model_name_or_path="${CKPT}" \
  model.tokenizer_args.pretrained_model_name_or_path="${CKPT}" \
  model.model_args.attn_implementation=sdpa \
  eval.tofu.batch_size=1 \
  paths.output_dir="${CKPT}/recovery_screen"
