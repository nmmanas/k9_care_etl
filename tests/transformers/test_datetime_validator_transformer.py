from datetime import datetime


class TestValidateAndTransformData:
    """
    Test suite for the validate_datetime method.
    """

    def test_validate_datetime_all_valid(
        self, fact_transformer_instance, datetime_validator_mock
    ):
        """
        Test validate_datetime with all valid date strings.
        """
        data = [
            {"id": 1, "created_date": "2024-08-14T12:34:56.789Z"},
            {"id": 2, "created_date": "2024-08-15T12:34:56.789Z"},
        ]

        datetime_validator_mock.validate.side_effect = [
            datetime(2024, 8, 14, 12, 34, 56, 789000),
            datetime(2024, 8, 15, 12, 34, 56, 789000),
        ]

        result = fact_transformer_instance.validate_datetime(data)

        assert len(result) == 2
        assert result[0]["parsed_date"] == datetime(
            2024, 8, 14, 12, 34, 56, 789000
        )
        assert result[1]["parsed_date"] == datetime(
            2024, 8, 15, 12, 34, 56, 789000
        )

    def test_validate_datetime_missing_date(
        self, fact_transformer_instance, datetime_validator_mock
    ):
        """
        Test validate_datetime with a record missing the
        created_date.
        """
        data = [
            {"id": 1, "created_date": "2024-08-14T12:34:56.789Z"},
            {"id": 2},  # Missing created_date
        ]

        datetime_validator_mock.validate.return_value = datetime(
            2024, 8, 14, 12, 34, 56, 789000
        )

        result = fact_transformer_instance.validate_datetime(data)

        assert len(result) == 1
        assert result[0]["id"] == 1
        assert "parsed_date" in result[0]
        assert result[0]["parsed_date"] == datetime(
            2024, 8, 14, 12, 34, 56, 789000
        )

    def test_validate_datetime_invalid_date(
        self, fact_transformer_instance, datetime_validator_mock
    ):
        """
        Test validate_datetime with a record that has an invalid date
        format.
        """
        data = [
            {"id": 1, "created_date": "2024-08-14T12:34:56.789Z"},
            {"id": 2, "created_date": "invalid-date-format"},
        ]

        datetime_validator_mock.validate.side_effect = [
            datetime(2024, 8, 14, 12, 34, 56, 789000),
            None,  # Invalid date format
        ]

        result = fact_transformer_instance.validate_datetime(data)

        assert len(result) == 1
        assert result[0]["id"] == 1
        assert "parsed_date" in result[0]
        assert result[0]["parsed_date"] == datetime(
            2024, 8, 14, 12, 34, 56, 789000
        )

    def test_validate_datetime_all_invalid(
        self, fact_transformer_instance, datetime_validator_mock
    ):
        """
        Test validate_datetime where all records have invalid date
        formats.
        """
        data = [
            {"id": 1, "created_date": "invalid-date-format"},
            {"id": 2, "created_date": "another-invalid-date"},
        ]

        datetime_validator_mock.validate.return_value = (
            None  # All dates are invalid
        )

        result = fact_transformer_instance.validate_datetime(data)

        assert len(result) == 0  # No valid records should be returned

    def test_validate_datetime_empty_data(
        self, fact_transformer_instance, datetime_validator_mock
    ):
        """
        Test validate_datetime with an empty list.
        """
        data = []

        result = fact_transformer_instance.validate_datetime(data)

        assert result == []  # Should return an empty list
