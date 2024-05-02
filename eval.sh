#!/bin/bash
#SBATCH --job-name=qa
#SBATCH --output=eval_rule.out
#SBATCH --error=eval_rule.err
#SBATCH --partition=shire-general
#SBATCH --nodelist=shire-2-16
#SBATCH --nodes=1
#SBATCH --mem=32G
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --time=12:00:00
#SBATCH --gres=gpu:2

module load cuda-11.6
export PYTHONPATH='pwd'
source activate multab

python trainer.py predict --ckpt_path checkpoints/retriever_model.ckpt --config inference_configs/retriever_inference_dev.yaml
# python trainer.py predict --ckpt_path checkpoints/retriever_model.ckpt --config inference_configs/retriever_inference.yaml

python trainer.py predict --ckpt_path checkpoints/question_classification_model.ckpt --config inference_configs/question_classification_inference_dev.yaml
# # python trainer.py predict --ckpt_path checkpoints/question_classification_model.ckpt --config inference_configs/question_classification_inference.yaml

python convert_retriever_result.py

python trainer.py predict --ckpt_path checkpoints/program_generation_model.ckpt --config inference_configs/program_generation_inference_dev.yaml
python trainer.py predict --ckpt_path checkpoints/span_selection_model.ckpt --config inference_configs/span_selection_inference_dev.yaml

# python trainer.py predict --ckpt_path checkpoints/program_generation_model.ckpt --config inference_configs/program_generation_inference.yaml
# python trainer.py predict --ckpt_path checkpoints/span_selection_model.ckpt --config inference_configs/span_selection_inference.yaml


python evaluate.py dataset/dev.json