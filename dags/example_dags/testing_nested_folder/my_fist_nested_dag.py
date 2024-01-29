import logging
from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

dag_parameters = {
    "dag_id": "testing_dag_in_nested_folder",
    "start_date": datetime(2024, 1, 1),
    "schedule_interval": None,
    "catchup": False,
    "tags": ["test"],
}


def testing_function(message: str = "test"):
    logging.info(message)


with DAG(**dag_parameters) as dag:
    # 1. define task
    start_task = EmptyOperator(task_id="start_task")
    some_task = PythonOperator(task_id="python_function_1", python_callable=testing_function, dag=dag)
    end_task = EmptyOperator(task_id="end_task")

    # 2. Setup task flow
    start_task >> some_task >> end_task  # This is part of the airflow DSL (DOMAIN specific language)
