import pytest
import requests

from ...dags.etl.exceptions import MalformedJsonError


class TestJSONURLExtractor:
    """
    The `TestJSONURLExtractor` class contains unit tests for testing the
    `get_resource` and `extract_data` functions from
    etl.extractors.JSONURLExtractor, mocking responses and testing various
    scenarios such as tatus codes, network errors, and JSON data extraction.
    """

    def test_get_resource(self, mocker):
        """
        The function `test_get_resource` tests the `get_resource` function by
        mocking a response and asserting its status code.

        :param mocker: The `mocker` parameter in the `test_get_resource`
        function is used for creating mock objects and patching functions
        during testing. In this specific test case, `mocker` is used to create
        a mock response object for the `requests.get` function and set its
        status code to 200.
        """
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mocker.patch("requests.get", return_value=mock_response)

        from ...dags.etl.extractors import JSONURLExtractor

        response = JSONURLExtractor("www.example.com").get_resource()

        assert response == mock_response
        assert response.status_code == 200

    def test_get_resource_status_code(self, mocker):
        """
        The function `test_get_resource_status_code` tests the status code
        returned by the `get_resource` function.

        :param mocker: The `mocker` parameter in the test function is used for
        creating mock objects and patching functions or methods during testing.
        In the provided test case, `mocker` is used to create a mock response
        object with a status codeof 404 and patch the `requests.get` function
        to return this mocked response object.
        """
        mock_response = mocker.Mock()
        mock_response.status_code = 404
        mocker.patch("requests.get", return_value=mock_response)

        from ...dags.etl.extractors import JSONURLExtractor

        response = JSONURLExtractor("www.example.com").get_resource()

        assert response.status_code == 404

    def test_get_resource_network_down(self, mocker):
        """
        The function `test_get_resource_network_down` tests the behavior of the
        `get_resource` function when a `ConnectionError` with the message
        "Network is down" is raised.

        :param mocker: The `mocker` parameter in the
        `test_get_resource_network_down` function is used as a fixture provided
        by the `pytest-mock` library. It allowsyou to easily mock objects and
        functions for testing purposes. In this specific test case, `mocker`
        is used to patch the `requests.get` function.
        """
        mocker.patch(
            "requests.get",
            side_effect=requests.exceptions.ConnectionError("Network is down"),
        )

        from ...dags.etl.extractors import JSONURLExtractor

        # Assert that the ConnectionError is raised
        with pytest.raises(
            requests.exceptions.ConnectionError, match="Network is down"
        ):
            JSONURLExtractor("www.example.com").get_resource()

    def test_get_resource_missing_resource(self, mocker):
        """
        The function `test_get_resource_missing_resource` tests the behavior
        of the `get_resource` function when a resource is missing.

        :param mocker: The `mocker` parameter in the test function is used for
        creatingmock objects and patching functions during testing. In this
        specific test case, `mocker` is being used to create a mock response
        object with a status code of 404 and patch the `requests.get` function
        to return this mock response object.
        """
        mock_response = mocker.Mock()
        mock_response.status_code = 404
        mocker.patch("requests.get", return_value=mock_response)

        from ...dags.etl.extractors import JSONURLExtractor

        response = JSONURLExtractor("www.example.com").get_resource()

        assert response.status_code == 404

    def test_extract_data(self, mocker):
        """
        The function `test_extract_data` is a unit test that mocks a JSON
        response and tests the extraction of data using the `extract_data`
        function.

        :param mocker: The `mocker` parameter in the `test_extract_data` method
        is used for mocking objects and functions in your test cases. In this
        specific test case, `mocker` is being used to create a mock response
        object that simulates the behavior of a real HTTP response object.
        """
        mock_json_data = [
            {
                "fact": "A great fact about dogs!",
                "created_date": "2023-10-02T02:22:00.272Z",
            }
        ]
        mock_response = mocker.Mock()
        mock_response.json.return_value = mock_json_data
        mocker.patch("requests.get", return_value=mock_response)

        from ...dags.etl.extractors import JSONURLExtractor

        data = JSONURLExtractor("www.example.com").extract()

        assert data == mock_json_data

    def test_extract_data_invalid_file_type(self, mocker):
        """
        The function `test_extract_data_invalid_file_type` tests the
        `extract_data`function by mocking a response with an invalid file type
        error.

        :param mocker: `mocker` is a pytest-mock object that allows you to
        create mock objects for testing purposes. In the provided test case,
        `mocker` is used to create a mock response object and patch the
        `requests.get` function to return this mock response.
        """
        mock_response = mocker.Mock()
        mock_response.json.side_effect = MalformedJsonError(
            "The JSON file is malformed"
        )
        mocker.patch("requests.get", return_value=mock_response)

        from ...dags.etl.extractors import JSONURLExtractor

        # Assert that the MalformedJsonError is raised
        with pytest.raises(
            MalformedJsonError, match="The JSON file is malformed"
        ):
            JSONURLExtractor("www.example.com").extract()

    def test_extract_data_malformed_json(self, mocker):
        """
        The function `test_extract_data_malformed_json` tests the extraction
        of data from a malformed JSON response by mocking the response object.

        :param mocker: The `mocker` parameter in the test function is used for
        mocking objects and functions in Python tests. In this specific test
        case, `mocker` is being used to create a mock response object for
        simulating a scenario where the JSON data is malformed.
        """
        # Mock the response object to simulate a malformed JSON
        mock_response = mocker.Mock()
        mock_response.json.side_effect = ValueError("Malformed JSON")
        mocker.patch("requests.get", return_value=mock_response)

        from ...dags.etl.extractors import JSONURLExtractor

        # Assert that the MalformedJsonError is raised
        with pytest.raises(
            MalformedJsonError, match="The JSON file is malformed"
        ):
            JSONURLExtractor("www.example.com").extract()
