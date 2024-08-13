class TestExtract:
    """
    The `TestExtract` class contains unit tests for the `get_resource` and
    `extract_data` functions.
    """

    def test_get_resource(self, mocker):
        """
        The function `test_get_resource` tests the `get_resource` function by mocking a
        response and asserting its status code.

        :param mocker: The `mocker` parameter in the `test_get_resource` function is
        used for creating mock objects and patching functions during testing. In this
        specific test case, `mocker` is used to create a mock response object for the
        `requests.get` function and set its status code to 200.
        """
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mocker.patch("requests.get", return_value=mock_response)

        from ..etl.extract import get_resource

        response = get_resource()

        assert response == mock_response
        assert response.status_code == 200

    def test_extract_data(self, mocker):
        """
        The function `test_extract_data` is a unit test that mocks a JSON response and
        tests the extraction of data using the `extract_data` function.

        :param mocker: The `mocker` parameter in the `test_extract_data` method is used
        for mocking objects and functions in your test cases. In this specific test
        case, `mocker` is being used to create a mock response object that simulates the
        behavior of a real HTTP response object.
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

        from ..etl.extract import extract_data

        data = extract_data()

        assert data == mock_json_data
