from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator

dag_parameters = {
    "dag_id": "my_first_dummy_dag",
    "start_date": datetime(2024, 1, 1),
    "schedule_interval": None,
    "catchup": False,
    "tags": ["test"],
}

with DAG(**dag_parameters) as dag:
    # 1. define task
    start_task = EmptyOperator(task_id="start_task")
    some_task = EmptyOperator(task_id="some_task")
    end_task = EmptyOperator(task_id="end_task")

    # 2. Setup task flow
    start_task >> some_task >> end_task  # This is part of the airflow DSL (DOMAIN specific language)
