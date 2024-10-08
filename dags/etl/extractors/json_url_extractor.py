import time

import requests

from ..exceptions import MalformedJsonError
from ..logging_config import LoggerManager
from .base_extractor import BaseExtractor

logging = LoggerManager.get_logger(__name__)


class JSONURLExtractor(BaseExtractor):
    def __init__(self, url):
        logging.info("Initialize extractor")
        self.url = url

    @LoggerManager.log_execution
    def get_resource(self):
        """
        The function `get_resource` makes a GET request to a specified URL with
        retries and exponential backoff in case of connection errors or
        timeouts.

        :return: The `get_resource` method is returning the response object
        obtained from the `requests.get` call if the request is successful and
        the response status code is not an error. If there are connection
        errors or timeouts during the request, the method will retry the
        request up to 3 times with an exponential backoff strategy. If all
        retries fail, an error message is logged, and the original exception is
        raised
        """
        retries = 3
        for attempt in range(retries):
            try:
                logging.info(f"Attempt {attempt+1}/{retries}")
                logging.info(f"Connecting to: {self.url}")
                response = requests.get(self.url, timeout=5)
                response.raise_for_status()
                return response
            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
            ) as e:
                if attempt < retries - 1:
                    sleep_time = 2**attempt
                    logging.error(f"Failed to reach resource at {self.url}")
                    logging.error(f"Trying after: {sleep_time}s")
                    time.sleep(sleep_time)  # Exponential backoff
                else:
                    logging.error(
                        f"Failed to reach resource at {self.url}: {e}"
                    )
                    raise e  # Raise the exception after final retry

    @LoggerManager.log_execution
    def extract(self):
        """
        The function `extract_data` retrieves JSON data from a resource,
        handling errors related to file type and JSON parsing.
        :return: The `extract_data` function is attempting to extract and parse
        JSON data from a resource. If successful, it will return the parsed
        JSON data. If there are errors such as an invalid file type or
        malformed JSON, it will log an error message and raise the
        corresponding custom exception (`InvalidFileTypeError` or
        `MalformedJsonError`).
        """
        try:
            response = self.get_resource()

            # Attempt to parse JSON content
            try:
                logging.info("Attempt to parse json")
                return response.json()
            except ValueError as e:
                logging.error("The JSON file is malformed")
                raise MalformedJsonError("The JSON file is malformed") from e

        except MalformedJsonError as e:
            logging.error(f"Error extracting data: {e}")
            raise
