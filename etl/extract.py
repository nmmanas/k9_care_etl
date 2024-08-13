import logging
import time

import requests

from .config import Config
from .exceptions import InvalidFileTypeError, MalformedJsonError


def get_resource():
    """
    The function `get_resource` attempts to retrieve a resource from a specified URL
    with retries and exponential backoff in case of connection errors or timeouts.
    :return: The `get_resource` function is returning the response object obtained from
    making a GET request to the resource URL specified in the `Config.resource_url`.
    """
    url = Config.resource_url
    retries = 3
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            if attempt < retries - 1:
                time.sleep(2**attempt)  # Exponential backoff
            else:
                logging.error(f"Failed to reach resource at {url}: {e}")
                raise e  # Raise the exception after final retry


def extract_data():
    """
    The function `extract_data` retrieves JSON data from a resource, handling errors
    related to file type and JSON parsing.
    :return: The `extract_data` function is attempting to extract and parse JSON data
    from a resource. If successful, it will return the parsed JSON data. If there are
    errors such as an invalid file type or malformed JSON, it will log an error message
    and raise the corresponding custom exception (`InvalidFileTypeError` or
    `MalformedJsonError`).
    """
    try:
        response = get_resource()

        # Check if the response is JSON
        if response.headers.get("Content-Type") != "application/json":
            raise InvalidFileTypeError("Expected JSON, received a different file type")

        # Attempt to parse JSON content
        try:
            return response.json()
        except ValueError as e:
            raise MalformedJsonError("The JSON file is malformed") from e

    except (InvalidFileTypeError, MalformedJsonError) as e:
        logging.error(f"Error extracting data: {e}")
        raise
