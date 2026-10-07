#!/usr/bin/env bash
set -euo pipefail

cd /home/research/open-unlearning

RMU_CKPT="/home/research/open-unlearning/saves/unlearn/tofu_Llama-3.2-1B-Instruct_forget01_RMU_test"

TASK_NAME="tofu_Llama-3.2-1B-Instruct_forget01_RMU_relearn_50step_continuous"

CUDA_VISIBLE_DEVICES=0 python src/train.py \
  --config-name=train.yaml \
  model=Llama-3.2-1B-Instruct \
  trainer=finetune \
  data/datasets@data.train=TOFU_QA_forget \
  task_name="${TASK_NAME}" \
  model.model_args.pretrained_model_name_or_path="${RMU_CKPT}" \
  model.model_args.attn_implementation=sdpa \
  model.tokenizer_args.pretrained_model_name_or_path="${RMU_CKPT}" \
  data.train.TOFU_QA_forget.args.hf_args.name=forget01 \
  trainer.args.per_device_train_batch_size=1 \
  trainer.args.per_device_eval_batch_size=1 \
  trainer.args.gradient_accumulation_steps=4 \
  trainer.args.learning_rate=1e-5 \
  trainer.args.gradient_checkpointing=true \
  trainer.args.weight_decay=0.01 \
  trainer.args.logging_steps=1 \
  +trainer.args.max_steps=50 \
  trainer.args.save_strategy=no \
  trainer.args.eval_strategy=no \
  trainer.args.do_eval=false \
  ~eval \
  +relearning_snapshot.enabled=true \
  +relearning_snapshot.callback_dir=/home/research/research/reproduction/05-relearning/code \
  +relearning_snapshot.steps='[1,5,10,20,50]'
