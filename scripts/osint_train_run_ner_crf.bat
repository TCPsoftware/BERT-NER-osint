
set TASK_NAME=osint
set BERT_BASE_DIR=%~dp0/../

python %BERT_BASE_DIR%/run_ner_crf.py ^
  --model_type=bert ^
  --model_name_or_path=%BERT_BASE_DIR%/prev_trained_model/chinese_roberta_wwm_ext_pytorch ^
  --task_name=%TASK_NAME% ^
  --do_train ^
  --do_eval ^
  --do_lower_case ^
  --data_dir=%BERT_BASE_DIR%/datasets/APT-NER-source-char-1104_token-json_char_BIO_detail/ ^
  --train_max_seq_length=128 ^
  --eval_max_seq_length=512 ^
  --per_gpu_train_batch_size=24 ^
  --per_gpu_eval_batch_size=24 ^
  --learning_rate=3e-5 ^
  --crf_learning_rate=1e-3 ^
  --num_train_epochs=4.0 ^
  --logging_steps=-1 ^
  --save_steps=-1 ^
  --output_dir=%BERT_BASE_DIR%/outputs/%TASK_NAME%_output/ ^
  --overwrite_output_dir ^
  --seed=42
