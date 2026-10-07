#!/usr/bin/env bash
set -euo pipefail

cd /home/research/open-unlearning

source ~/miniconda3/etc/profile.d/conda.sh
conda activate openunlearning

CKPT="/home/research/open-unlearning/saves/train/exp008_matched_control_20step"

OUT="/home/research/research/reproduction/08-quasi-identifier-recovery/results/matched_control_20step_heldout"

echo "================================================================"
echo "EXP008 — MATCHED CONTROL HELD-OUT EVALUATION"
echo "================================================================"
echo "Checkpoint: ${CKPT}"
echo "Output    : ${OUT}"
echo

test -f "${CKPT}/model.safetensors" || {
    echo "ERROR: model.safetensors not found."
    exit 1
}

CUDA_VISIBLE_DEVICES=0 python src/eval.py \
  eval=heldout_recovery_screen \
  model=Llama-3.2-1B-Instruct \
  model.model_args.pretrained_model_name_or_path="${CKPT}" \
  model.tokenizer_args.pretrained_model_name_or_path="${CKPT}" \
  model.model_args.attn_implementation=sdpa \
  task_name=exp008_matched_control_20step_heldout \
  eval.tofu.output_dir="${OUT}"

echo
echo "================================================================"
echo "STATUS: EXP008_MATCHED_CONTROL_EVAL_COMPLETE"
echo "================================================================"
