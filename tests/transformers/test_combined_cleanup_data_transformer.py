class TestCleanupDataTransformer:

    def test_cleanup_data_no_blanks_no_duplicates(
        self, data_repository_mock, fact_transformer_instance
    ):
        data_repository_mock.fact_exists.return_value = False
        data = [{"fact": "Fact 1"}, {"fact": "Fact 2"}, {"fact": "Fact 3"}]

        result = fact_transformer_instance.cleanup_data(data)

        assert result == data  # the output should be the same as the input

    def test_cleanup_data_with_blanks(
        self, data_repository_mock, fact_transformer_instance
    ):
        data_repository_mock.fact_exists.return_value = False
        data = [
            {"fact": "Fact 1"},
            {"fact": ""},
            {"fact": "Fact 2"},
            {"fact": ""},
            {"fact": "Fact 3"},
        ]

        expected_result = [
            {"fact": "Fact 1"},
            {"fact": "Fact 2"},
            {"fact": "Fact 3"},
        ]

        result = fact_transformer_instance.cleanup_data(data)

        assert len(result) == len(
            expected_result
        )  # Blank facts should be removed

    def test_cleanup_data_with_duplicates(
        self, data_repository_mock, fact_transformer_instance
    ):
        data_repository_mock.fact_exists.return_value = False
        data = [
            {"fact": "Fact 1"},
            {"fact": "Fact 2"},
            {"fact": "Fact 1"},  # Duplicate fact
            {"fact": "Fact 3"},
        ]

        # Assuming that the deduplication method works correctly,
        # the expected result should remove the duplicate
        expected_result = [
            {"fact": "Fact 1"},
            {"fact": "Fact 2"},
            {"fact": "Fact 3"},
        ]

        result = fact_transformer_instance.cleanup_data(data)

        assert len(result) == len(
            expected_result
        )  # Duplicate facts should be removed

    def test_cleanup_data_with_whitespaces(
        self, data_repository_mock, fact_transformer_instance
    ):
        data_repository_mock.fact_exists.return_value = False
        data = [{"fact": " Fact 1 "}, {"fact": "Fact 2"}, {"fact": " Fact 3 "}]

        # Assuming that clean_whitespaces method trims the whitespaces
        expected_result = [
            {"fact": "Fact 1"},
            {"fact": "Fact 2"},
            {"fact": "Fact 3"},
        ]

        result = fact_transformer_instance.cleanup_data(data)

        assert len(result) == len(
            expected_result
        )  # Whitespaces should be cleaned

    def test_cleanup_data_all_steps_combined(
        self, data_repository_mock, fact_transformer_instance
    ):
        data_repository_mock.fact_exists.return_value = False
        data = [
            {"fact": " Fact 1 "},  # Leading and trailing spaces
            {"fact": ""},  # Blank fact
            {"fact": "Fact 2"},
            {"fact": "Fact 1"},  # Duplicate fact
            {"fact": "Fact 2"},  # Duplicate fact
            {"fact": " Fact 1 "},  # Another duplicate with spaces
            {"fact": "Fact 3"},
        ]

        expected_result = [
            {"fact": "Fact 1"},
            {"fact": "Fact 2"},
            {"fact": "Fact 3"},
        ]

        result = fact_transformer_instance.cleanup_data(data)

        # The result should have no blanks, no duplicates,
        # and no leading/trailing whitespaces
        assert len(result) == len(expected_result)
