import logging

import pandas as pd
from airflow.decorators import task
from repository.data_lake import save_dataframe


@task
def data_loader(transformed_data: pd.DataFrame):
    logging.debug("* Saving data in s3 bucket")
    print(transformed_data)
    path = save_dataframe(
        data=transformed_data,
        resource_name="knowledge_transfer",
        resource_group="etl_with_airflow_example",
        stage="ready",
        extension="txt",
    )
    logging.debug(f"* Data loader in path {path}")
