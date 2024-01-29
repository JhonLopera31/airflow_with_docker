from datetime import datetime

from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
# modules must be imported assuming that dags is the parent folder this to be recognized by airflow
from test_etl.extractor import data_extractor
from test_etl.transformer import data_transformer
from test_etl.loader import data_loader

# Define the default_args dictionary to specify the default parameters of the DAG
default_args = {
    'owner': "airflow",
    "start_date": datetime(2024, 1, 1),
}


@dag(dag_id="test_etl", schedule_interval=None, default_args=default_args, catchup=False, tags=['etl'])
def dag():
    # 1. define tasks
    start_task = EmptyOperator(task_id="start_task")
    extraction = data_extractor()
    transformation = data_transformer(extraction)
    loading = data_loader(transformation)
    end_task = EmptyOperator(task_id="end_task")

    # 2 define workflow
    start_task >> extraction >> transformation >> loading >> end_task


my_dag = dag()
