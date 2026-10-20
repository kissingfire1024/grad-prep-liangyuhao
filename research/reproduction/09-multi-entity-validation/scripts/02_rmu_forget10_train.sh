#!/bin/bash
set -e

# ============================================================
# EXP009 — Formal RMU forget10 training
#
# Base:
#   open-unlearning/tofu_Llama-3.2-1B-Instruct_full
#
# Forget:
#   TOFU forget10 (400 QA / 20 entities)
#
# Retain:
#   TOFU retain90
#
# RMU:
#   gamma              = 1.0
#   alpha              = 1.0
#   steering_coeff     = 2
#   retain_loss_type   = EMBED_DIFF
#   module_regex       = model.layers.7
#   trainable params   = all
#
# Training:
#   max_steps          = 100
#   batch_size         = 1
#   grad accumulation  = 4
#   learning_rate      = 1e-5
#   weight_decay       = 0.01
#
# IMPORTANT:
#   This is the formal EXP009 unlearning base.
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

TASK=tofu_Llama-3.2-1B-Instruct_forget10_RMU_exp009

echo "======================================================================"
echo "EXP009 — FORMAL RMU FORGET10 TRAINING"
echo "======================================================================"
echo "Task          : $TASK"
echo "Forget split  : forget10"
echo "Retain split  : retain90"
echo "Max steps     : 100"
echo "Batch size    : 1"
echo "Grad accum    : 4"
echo "======================================================================"

CUDA_VISIBLE_DEVICES=0 accelerate launch \
  --config_file configs/accelerate/single_gpu.yaml \
  src/train.py \
  --config-name=unlearn.yaml \
  experiment=unlearn/tofu/default.yaml \
  trainer=RMU \
  task_name=$TASK \
  model=Llama-3.2-1B-Instruct \
  forget_split=forget10 \
  retain_split=retain90 \
  model.model_args.pretrained_model_name_or_path=open-unlearning/tofu_Llama-3.2-1B-Instruct_full \
  model.tokenizer_args.pretrained_model_name_or_path=open-unlearning/tofu_Llama-3.2-1B-Instruct_full \
  model.model_args.attn_implementation=sdpa \
  trainer.args.per_device_train_batch_size=1 \
  trainer.args.gradient_accumulation_steps=4 \
  trainer.args.gradient_checkpointing=true \
  +trainer.args.max_steps=100 \
  trainer.args.num_train_epochs=10 \
  trainer.args.do_eval=false \
  trainer.args.eval_on_start=false \
  trainer.args.eval_strategy=no \
  2>&1 | tee ~/research/reproduction/09-multi-entity-validation/logs/rmu_forget10_train.log

echo
echo "======================================================================"
echo "CHECKPOINT"
echo "======================================================================"

du -sh ./saves/unlearn/$TASK || true

echo
echo "======================================================================"
echo "STATUS: EXP009_RMU_FORGET10_FORMAL_TRAINING_FINISHED"
echo "======================================================================"
