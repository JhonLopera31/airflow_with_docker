import logging
from datetime import datetime, timedelta

from airflow.decorators import dag
from airflow.decorators import task
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

# Define the default_args dictionary to specify the default parameters of the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022, 1, 1),
    'retry_delay': timedelta(minutes=5),
}


def additional_task(**kwargs):
    logging.info("Task running in parallel to ETL")
    # Add your additional task logic here


@dag(schedule_interval=timedelta(days=1), default_args=default_args, catchup=False, tags=['test'])
def dag_with_decorators():
    # 1. Define tasks
    @task(multiple_outputs=True)
    def extract_dummy_data() -> dict:
        logging.info("Executing extract task")

        dummy_data = {
            "name": "test_name",
            "lastname": "test_lastname",
            "occupation": "test_occupation",
            "email": "test_email@email_address.test"
        }
        return dummy_data

    @task()
    def transform_dummy_data(dummy_data):
        logging.info("Transforming dummy data")
        logging.info(dummy_data)
        transformed_dummy_data = {key: value.capitalize() for key, value in dummy_data.items()}
        return transformed_dummy_data

    @task()
    def load_dummy_data(dummy_data: dict):
        logging.info("Loading data")
        logging.info(f"Amount of loaded data {dummy_data}")

    additional_python_task = PythonOperator(
        task_id='parallel_python_task',
        python_callable=additional_task,
        provide_context=True,
    )

    # 2. Call task to define the ETL dependencies
    extract_result = extract_dummy_data()
    transform_result = transform_dummy_data(extract_result)
    load_result = load_dummy_data(transform_result)

    # 3. Define dummy task for start and end are just a common practice to indicate the start and end of a pipeline
    start_etl = EmptyOperator(task_id='start_etl')
    end_etl = EmptyOperator(task_id='end_etl')

    # 4. Define task work flow
    start_etl >> extract_result >> transform_result >> load_result
    start_etl >> additional_python_task

    [load_result, additional_python_task] >> end_etl


# Instantiate the DAG by calling the decorated function
my_dag = dag_with_decorators()
