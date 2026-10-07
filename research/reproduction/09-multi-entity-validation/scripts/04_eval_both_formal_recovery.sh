#!/usr/bin/env bash
set -euo pipefail

cd /home/research/open-unlearning

source ~/miniconda3/etc/profile.d/conda.sh
conda activate openunlearning

export CUDA_HOME=/usr/local/cuda-12.1
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:${LD_LIBRARY_PATH:-}
export HF_HUB_DISABLE_XET=1

ROOT="/home/research/research/reproduction/09-multi-entity-validation"

TARGET="${ROOT}/data/heldout_targets_18entity_v1.json"
EXPECTED_TARGET_SHA="1236a72d8ffb9ac5bb90fd04551ae43b57bc5ae9d2f4e679bc2ad61359195f6a"

ACTUAL_TARGET_SHA=$(sha256sum "${TARGET}" | awk '{print $1}')

if [ "${ACTUAL_TARGET_SHA}" != "${EXPECTED_TARGET_SHA}" ]; then
    echo "ERROR: frozen heldout target hash mismatch."
    exit 1
fi

QUASI="/home/research/open-unlearning/saves/train/exp009_quasi_20step_formal"
CONTROL="/home/research/open-unlearning/saves/train/exp009_control_20step_formal"

QOUT="${ROOT}/results/quasi_20step_18entity"
COUT="${ROOT}/results/control_20step_18entity"

for P in "${QUASI}" "${CONTROL}"; do
    test -f "${P}/model.safetensors" || {
        echo "ERROR: checkpoint missing: ${P}"
        exit 1
    }
done

# Prevent accidental overwrite of formal results.
for P in "${QOUT}" "${COUT}"; do
    if [ -e "${P}" ]; then
        echo "ERROR: formal evaluation output already exists:"
        echo "${P}"
        echo "Do not overwrite formal outcomes."
        exit 1
    fi
done

echo "================================================================================"
echo "EXP009 — FORMAL RECOVERY EVALUATION"
echo "================================================================================"
echo "Target SHA: ${ACTUAL_TARGET_SHA}"
echo
echo "Both formal trajectories will be evaluated before analysis."
echo "No hyperparameter changes are permitted."
echo "================================================================================"

echo
echo "############################"
echo "# 1/2 FORMAL QUASI"
echo "############################"

CUDA_VISIBLE_DEVICES=0 python src/eval.py \
  --config-name=eval.yaml \
  model=Llama-3.2-1B-Instruct \
  eval=exp009_heldout_recovery_screen \
  task_name=exp009_quasi_20step_18entity_eval \
  model.model_args.pretrained_model_name_or_path="${QUASI}" \
  model.tokenizer_args.pretrained_model_name_or_path="${QUASI}" \
  model.model_args.attn_implementation=sdpa \
  eval.tofu.batch_size=1 \
  paths.output_dir="${QOUT}"

echo
echo "QUASI EVALUATION COMPLETE."
echo "Proceeding immediately to Control."
echo

echo "############################"
echo "# 2/2 FORMAL CONTROL"
echo "############################"

CUDA_VISIBLE_DEVICES=0 python src/eval.py \
  --config-name=eval.yaml \
  model=Llama-3.2-1B-Instruct \
  eval=exp009_heldout_recovery_screen \
  task_name=exp009_control_20step_18entity_eval \
  model.model_args.pretrained_model_name_or_path="${CONTROL}" \
  model.tokenizer_args.pretrained_model_name_or_path="${CONTROL}" \
  model.model_args.attn_implementation=sdpa \
  eval.tofu.batch_size=1 \
  paths.output_dir="${COUT}"

echo
echo "================================================================================"
echo "STATUS: EXP009_BOTH_FORMAL_RECOVERY_EVALUATIONS_COMPLETE"
echo
echo "Quasi results  : ${QOUT}"
echo "Control results: ${COUT}"
echo "================================================================================"
