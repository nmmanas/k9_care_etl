class TestValidateKeys:
    """
    Test suite for the validate_keys method.
    """

    def test_validate_keys_all_valid(self, fact_transformer_instance):
        """
        Test validate_keys with all records containing the required keys.
        """
        data = [
            {"fact": "Fact 1", "created_date": "2024-08-14"},
            {"fact": "Fact 2", "created_date": "2024-08-15"},
        ]

        result = fact_transformer_instance.validate_keys(data)

        assert (
            result == data
        )  # All records are valid, so the result should be the same as input

    def test_validate_keys_some_missing_keys(self, fact_transformer_instance):
        """
        Test validate_keys with some records missing one or more required keys.
        """
        data = [
            {"fact": "Fact 1", "created_date": "2024-08-14"},
            {"fact": "Fact 2"},  # Missing 'created_date'
            {"created_date": "2024-08-16"},  # Missing 'fact'
        ]

        result = fact_transformer_instance.validate_keys(data)

        expected_result = [{"fact": "Fact 1", "created_date": "2024-08-14"}]
        assert (
            result == expected_result
        )  # Only the record with all required keys should be included

    def test_validate_keys_all_missing_keys(self, fact_transformer_instance):
        """
        Test validate_keys with all records missing one or more required keys.
        """
        data = [
            {"fact": "Fact 1"},  # Missing 'created_date'
            {"created_date": "2024-08-15"},  # Missing 'fact'
        ]

        result = fact_transformer_instance.validate_keys(data)

        assert (
            result == []
        )  # No records should be included, as all are missing required keys

    def test_validate_keys_empty_data(self, fact_transformer_instance):
        """
        Test validate_keys with an empty list.
        """
        data = []

        result = fact_transformer_instance.validate_keys(data)

        assert result == []  # Should return an empty list

    def test_validate_keys_additional_keys(self, fact_transformer_instance):
        """
        Test validate_keys with records that have additional keys beyond the
        required ones.
        """
        data = [
            {
                "fact": "Fact 1",
                "created_date": "2024-08-14",
                "extra_key": "extra_value",
            },
            {
                "fact": "Fact 2",
                "created_date": "2024-08-15",
                "extra_key": "extra_value",
            },
        ]

        result = fact_transformer_instance.validate_keys(data)

        assert (
            result == data
        )  # All records are valid, even with additional keys

    def test_validate_keys_different_required_keys(
        self, fact_transformer_instance
    ):
        """
        Test validate_keys with a different set of required keys.
        """
        fact_transformer_instance.required_keys = ["fact", "id"]

        data = [
            {"fact": "Fact 1", "id": 1, "created_date": "2024-08-14"},
            {"fact": "Fact 2", "created_date": "2024-08-15"},  # Missing 'id'
        ]

        result = fact_transformer_instance.validate_keys(data)

        expected_result = [
            {"fact": "Fact 1", "id": 1, "created_date": "2024-08-14"}
        ]
        assert (
            result == expected_result
        )  # Only the record with all required keys should be included
