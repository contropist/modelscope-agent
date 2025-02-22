## train

We release a tool dataset in **ModelScope** for training and evaluation of finetune LLM([Tool dataset](https://www.modelscope.cn/datasets/modelscope/ms_hackathon_23_agent_train_dev/summary)). A corresponding training script using **ModelScope** library are provided .


### training options

The training script supports various training methods based on your available resources:

- Supervised fine-tuning with full-parameters or Lora.
- Distributed training by integration with ModelScope DeepspeedHook.

### data preprocess

A piece of dat may be formulated as follow. Since we use a text-generation task scheme to train LLM, the origin data need to be preprocessed.

```Python
System: system info(agent info, tool info...).
User: user inputs.
Assistants:
# agent call
<|startofthink|>...<|endofthink|>\n\n
# tool execute
<|startofexec|>...<|endofexec|>\n
# summarize
...
# may be multiple rounds
```

- Each data instance consists of three roles: system, user, and assistant. The LLM should only focus on the **assistant** part.
- The **assistant** part is typically composed of three sections. The LLM should only consider the content of the agent call and the final summary.
- The other unnecessary parts are masked using `IGNORE_INDEX` to exclude them from loss calculation.

### training scripts

To start a training, you can use the script `run_train_ddp.sh'

```Shell
DATA_PARALLEL_SIZE=2
TENSOR_MODEL_PARALLEL_SIZE=2

WORLD_SIZE=$(($DATA_PARALLEL_SIZE * $TENSOR_MODEL_PARALLEL_SIZE))
DATE_TIME=$(date +%Y%m%d-%H%M%S)
export PYTHONPATH=$PYTHONPATH:./
torchrun --nproc_per_node $WORLD_SIZE demo/tool_agent_finetune/finetune_tool.py \
    --work_dir './tmp/tmp_baichuan/'$DATE_TIME \
    --model 'baichuan-inc/baichuan-7B' \
    --dataset_json_file 'demo/tool_agent_finetune/train_v1.2_plugins_sample.json' \
    --train_split 'train' \
    --val_split 'validation' \
    --max_epochs 1 \
    --per_device_train_batch_size 8 \
    --train_data_worker 1 \
    --lr 1e-4 \
    --lr_scheduler 'CosineAnnealingLR' \
    --bf16 1 \
    --device_map 'auto' \
    --train_shuffle 'True' \
    --save_best_checkpoint 'True' \
    --logging_interval 5 \
    --save_strategy 'by_step' \
    --save_interval 2000 \
    --max_checkpoint_num 1 \
    --use_lora 1 \
    --lora_rank 8 \
    --lora_alpha 32 \
    --lora_dropout 0.1 \
    --lora_replace_module 'pack' \
    --enable_gradient_checkpoint 1 \
    --max_length 2048 \
    --eval_strategy 'by_step' \
    --eval_interval 300 \
    --eval_metrics 'ppl' \
    --metric_for_best_model 'ppl' \
    --metric_rule_for_best_model 'min' \
    --per_device_eval_batch_size 8 \
    --eval_data_worker 1 \
    --max_checkpoint_num_best 1 \
    --deepspeed 'demo/tool_agent_finetune/default_offload_opt_param.json' \
```

### evaluate

After training, we also provided an evluation script to judege the performance of agents in testing datasets. The groud truth of testing datasets are generated by ...

The evaluation metrics include:
- Accuracy of tool names and parameters.
- `Rouge-l` metric for similarity of summarization.
