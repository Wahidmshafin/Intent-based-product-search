from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import textwrap, pathlib

BASE_DIR = "/opt/ml-pipeline"
default_args = {
    "owner": "mlops",
    "retries": 1,
    "retry_delay": timedelta(minutes=10),
}

with DAG(
    dag_id="ner_llm_finetuning",
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
) as dag:

    finetune = BashOperator(
        task_id="finetune_unsloth",
        bash_command=textwrap.dedent(f"""
            python {BASE_DIR}/scripts/finetuning_ner.py \
              --dataset {BASE_DIR}/data/ner_instruct_v3.jsonl \
              --out_dir {BASE_DIR}/artifacts/ner_lora_1b
        """),
    )

    merge = BashOperator(
        task_id="merge_fp16",
        bash_command=textwrap.dedent(f"""
            python {BASE_DIR}/scripts/merge_to_fp16.py \
              --adapter {BASE_DIR}/artifacts/ner_lora_1b \
              --out_dir {BASE_DIR}/artifacts/ner_merged_fp16
        """),
    )

    convert = BashOperator(
        task_id="convert_to_gguf",
        bash_command=textwrap.dedent(f"""
            python {BASE_DIR}/llama.cpp/convert.py \
              {BASE_DIR}/artifacts/ner_merged_fp16 \
              --outfile {BASE_DIR}/artifacts/tinyner.f16.gguf \
              --outtype f16
        """),
    )

    quant = BashOperator(
        task_id="quantize_q4",
        bash_command=textwrap.dedent(f"""
            {BASE_DIR}/llama.cpp/build/bin/quantize \
              {BASE_DIR}/artifacts/tinyner.f16.gguf \
              {BASE_DIR}/artifacts/tinyner.Q4_K_M.gguf \
              Q4_K_M
        """),
    )

    def write_modelfile():
        m = pathlib.Path(f"{BASE_DIR}/artifacts/Modelfile")
        m.write_text("FROM ./tinyner.Q4_K_M.gguf\n")

    modelfile = PythonOperator(
        task_id="write_modelfile",
        python_callable=write_modelfile,
    )

    # no Ollama steps here—just training+artifact creation
    finetune >> merge >> convert >> quant >> modelfile
