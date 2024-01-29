import logging

import pandas as pd
from airflow.decorators import task
from repository.data_lake import save_dataframe_in_s3_bucket


@task
def data_loader(transformed_data: pd.DataFrame) -> None:
    """
    This function saves the transformed data in S3 bucket
    :param transformed_data: pandas dataframe containing the transformed data
    :return: None
    """
    logging.info("* Saving data in s3 bucket")

    path = save_dataframe_in_s3_bucket(
        data=transformed_data,
        resource_name="knowledge_transfer",
        resource_group="etl_with_airflow_example",
        stage="ready",
        extension="txt",
    )
    logging.info(f"* Data loader in path {path}")
