import logging

import requests
from airflow.decorators import task
from airflow.models import Variable

ENDPOINT = Variable.get("etl_test_endpoint")


class InvalidRequestException(Exception):
    """Custom exception for invalid HTTP requests."""

    def __init__(self, message="Invalid HTTP request"):
        self.message = message
        super().__init__(self.message)


@task
def data_extractor() -> list:
    """
    get data from the url provided in variable etl_test_endpoint. This variable must be defined in airflow UI
    :return: extracted data from the url
    :raise raise InvalidRequestException:
    """
    try:
        logging.info(f"Extracting data from {ENDPOINT}")
        response = requests.get(ENDPOINT)
        response.raise_for_status()  # Check if the request was successful (status code 2xx)
        return response.json()

    except requests.exceptions.HTTPError as e:
        raise InvalidRequestException(f"HTTP Error: {e}")

    except requests.exceptions.RequestException as e:
        raise InvalidRequestException(f"Request Error: {e}")
