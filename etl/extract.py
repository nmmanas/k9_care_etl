import requests

from .config import Config


def get_resource():
    """
    The function `get_resource` retrieves a resource from a specified URL with a timeout
    of 5 seconds.
    :return: The function `get_resource()` is returning the response object obtained by
    making a GET request to the resource URL specified in the `Config` object.
    """
    url = Config.resource_url
    response = requests.get(url, timeout=5)
    return response


def extract_data():
    """
    The function `extract_data` retrieves a resource and returns its JSON data.
    :return: The function `extract_data()` is returning the JSON data obtained from the
    `get_resource()` function.
    """
    data = get_resource()
    return data.json()
