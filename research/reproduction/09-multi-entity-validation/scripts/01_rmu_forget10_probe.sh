#!/bin/bash
set -e

# ============================================================
# EXP009 — RMU forget10 1-step GPU probe
#
# Purpose:
#   Verify RMU + forget10 + retain90 can run safely
#   on RTX 4070 SUPER 12GB.
#
# This is NOT a formal experiment result.
# ============================================================

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

echo "============================================================"
echo "EXP009 — RMU FORGET10 1-STEP GPU PROBE"
echo "============================================================"
echo "Forget split : forget10"
echo "Retain split : retain90"
echo "Trainer      : RMU"
echo "Max steps    : 1"
echo "Batch size   : 1"
echo "Grad accum   : 4"
echo "============================================================"

CUDA_VISIBLE_DEVICES=0 accelerate launch \
  --config_file configs/accelerate/single_gpu.yaml \
  src/train.py \
  --config-name=unlearn.yaml \
  experiment=unlearn/tofu/default.yaml \
  trainer=RMU \
  task_name=tofu_Llama-3.2-1B-Instruct_forget10_RMU_probe \
  model=Llama-3.2-1B-Instruct \
  forget_split=forget10 \
  retain_split=retain90 \
  model.model_args.pretrained_model_name_or_path=open-unlearning/tofu_Llama-3.2-1B-Instruct_full \
  model.tokenizer_args.pretrained_model_name_or_path=open-unlearning/tofu_Llama-3.2-1B-Instruct_full \
  model.model_args.attn_implementation=sdpa \
  trainer.args.per_device_train_batch_size=1 \
  trainer.args.gradient_accumulation_steps=4 \
  trainer.args.gradient_checkpointing=true \
  +trainer.args.max_steps=1 \
  trainer.args.num_train_epochs=10 \
  trainer.args.do_eval=false \
  trainer.args.eval_on_start=false \
  trainer.args.eval_strategy=no \
  2>&1 | tee ~/research/reproduction/09-multi-entity-validation/logs/rmu_forget10_probe.log

echo
echo "============================================================"
echo "STATUS: EXP009_RMU_FORGET10_PROBE_FINISHED"
echo "============================================================"
