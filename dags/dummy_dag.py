from datetime import datetime
from airflow import DAG
from airflow.operators.empty import EmptyOperator

with DAG(
        dag_id="my_dag",
        start_date=datetime(2024, 1, 1),
        schedule_interval=None,
        catchup=False,
        tags=["test"],
) as dag:
    start = EmptyOperator(task_id="start_task")
    task_1 = EmptyOperator(task_id="task-1")
    end = EmptyOperator(task_id="end_task")
    start >> task_1 >> end
