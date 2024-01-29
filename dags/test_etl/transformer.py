import logging

import pandas as pd
from airflow.decorators import task
from utils.utility_functions import TextFormatter


@task
def data_transformer(raw_data: list) -> pd.DataFrame:
    text_formatter_1 = TextFormatter(strip_text=True, remove_double_spaces=True, case_type="title_case")
    text_formatter_2 = TextFormatter(strip_text=True, remove_double_spaces=True, case_type="lowercase")

    columns_to_exclude = ["email", "website"]

    logging.debug("- Normalizing json data")
    transformed_data = pd.DataFrame.from_records(raw_data)
    print(transformed_data.to_string())

    logging.debug("- Formatting string-type data")
    column_to_format = list(set(transformed_data.columns) - set(columns_to_exclude))
    transformed_data [column_to_format] = transformed_data[column_to_format].applymap(text_formatter_1.format_object)
    transformed_data [column_to_format] = transformed_data[column_to_format].applymap(text_formatter_2.format_object)

    return transformed_data



