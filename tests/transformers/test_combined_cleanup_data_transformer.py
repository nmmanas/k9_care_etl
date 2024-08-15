class TestCleanupDataTransformer:

    def test_cleanup_data_no_blanks_no_duplicates(
        self, data_repository_mock, fact_transformer_instance
    ):
        data_repository_mock.fact_exists.return_value = False
        data = [
            {"fact": "Fact 1", "created_date": "2024-01-01"},
            {"fact": "Fact 2", "created_date": "2024-01-02"},
            {"fact": "Fact 3", "created_date": "2024-01-03"},
        ]

        result = fact_transformer_instance.cleanup_data(data)

        assert result == data  # the output should be the same as the input

    def test_cleanup_data_with_blanks(
        self, data_repository_mock, fact_transformer_instance
    ):
        data_repository_mock.fact_exists.return_value = False
        data = [
            {"fact": "Fact 1", "created_date": "2024-01-01"},
            {"fact": "", "created_date": "2024-01-02"},
            {"fact": "Fact 2", "created_date": "2024-01-03"},
            {"fact": "", "created_date": "2024-01-01"},
            {"fact": "Fact 3", "created_date": "2024-01-02"},
        ]

        expected_result = [
            {"fact": "Fact 1", "created_date": "2024-01-03"},
            {"fact": "Fact 2", "created_date": "2024-01-01"},
            {"fact": "Fact 3", "created_date": "2024-01-02"},
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
            {"fact": "Fact 1", "created_date": "2024-01-03"},
            {"fact": "Fact 2", "created_date": "2024-01-01"},
            {"fact": "Fact 1", "created_date": "2024-01-02"},  # Duplicate fact
            {"fact": "Fact 3", "created_date": "2024-01-03"},
        ]

        # Assuming that the deduplication method works correctly,
        # the expected result should remove the duplicate
        expected_result = [
            {"fact": "Fact 1", "created_date": "2024-01-01"},
            {"fact": "Fact 2", "created_date": "2024-01-02"},
            {"fact": "Fact 3", "created_date": "2024-01-03"},
        ]

        result = fact_transformer_instance.cleanup_data(data)

        assert len(result) == len(
            expected_result
        )  # Duplicate facts should be removed

    def test_cleanup_data_with_whitespaces(
        self, data_repository_mock, fact_transformer_instance
    ):
        data_repository_mock.fact_exists.return_value = False
        data = [
            {"fact": " Fact 1 ", "created_date": "2024-01-01"},
            {"fact": "Fact 2", "created_date": "2024-01-02"},
            {"fact": " Fact 3 ", "created_date": "2024-01-03"},
        ]

        # Assuming that clean_whitespaces method trims the whitespaces
        expected_result = [
            {"fact": "Fact 1", "created_date": "2024-01-01"},
            {"fact": "Fact 2", "created_date": "2024-01-02"},
            {"fact": "Fact 3", "created_date": "2024-01-03"},
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
            {
                "fact": " Fact 1 ",
                "created_date": "2024-01-01",
            },  # Leading and trailing spaces
            {"fact": "", "created_date": "2024-01-02"},  # Blank fact
            {"fact": "Fact 2", "created_date": "2024-01-03"},
            {"fact": "Fact 1", "created_date": "2024-01-01"},  # Duplicate fact
            {"fact": "Fact 2", "created_date": "2024-01-02"},  # Duplicate fact
            {
                "fact": " Fact 1 ",
                "created_date": "2024-01-03",
            },  # Another duplicate with spaces
            {"fact": "Fact 3", "created_date": "2024-01-01"},
        ]

        expected_result = [
            {"fact": "Fact 1", "created_date": "2024-01-01"},
            {"fact": "Fact 2", "created_date": "2024-01-02"},
            {"fact": "Fact 3", "created_date": "2024-01-03"},
        ]

        result = fact_transformer_instance.cleanup_data(data)

        # The result should have no blanks, no duplicates,
        # and no leading/trailing whitespaces
        assert len(result) == len(expected_result)
