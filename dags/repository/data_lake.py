from datetime import datetime
from io import StringIO, BytesIO
from typing import Literal, Optional

import boto3
import pandas as pd
from airflow.models import Variable

AWS_CREDENTIALS = {
    "aws_access_key_id": Variable.get("AWS_ACCESS_KEY_ID"),
    "aws_secret_access_key": Variable.get("AWS_SECRET_ACCESS_KEY"),
    "region_name": Variable.get("AWS_DEFAULT_REGION")
}
S3_BUCKET = "knowledge-transfer-data"


def _get_s3_client():
    return boto3.client(service_name="s3", **AWS_CREDENTIALS)


def _get_file_base_name(*args):
    return "_".join([value for value in args if value is not None])


def _format_date(day: Optional[str] = None, month: Optional[str] = None, year: Optional[str] = None):
    year = year if year else datetime.today().strftime("%Y")
    month = month if month else datetime.today().strftime("%m")
    return "_".join([x for x in [day, month, year] if x])


def save_dataframe(  # noqa - All these arguments are requiered according to the naming convention.
        data: pd.DataFrame,
        resource_group: str,
        resource_name: str,
        stage: Literal["ready", "curated", "raw"],
        description: Optional[str] = None,
        extension: Literal["parquet", "txt"] = "parquet",
        year: Optional[str] = None,
        month: Optional[str] = None,
        day: Optional[str] = None,
) -> str:
    folder_name = f"{resource_group}/{resource_name}/{stage}"
    file_name = f"{_get_file_base_name(resource_name, stage, description, _format_date(day, month, year))}.{extension}"

    if extension == "parquet":
        _buffer = BytesIO()
        data.to_parquet(_buffer, engine="pyarrow")
    else:
        _buffer = StringIO()
        data.to_csv(_buffer, index=False, sep="\t")

    client = _get_s3_client()
    client.put_object(Body=_buffer.getvalue(), Bucket=S3_BUCKET, Key=f"{folder_name}/{file_name}")
    return f"{folder_name}/{file_name}"
