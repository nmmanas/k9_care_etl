from datetime import datetime


class TestDateTimeValidator:
    """
    Test suite for the DateTimeValidator class.
    """

    def test_validate_format_valid(self, date_time_validator):
        """
        Test validate_format with a valid date-time string.
        """
        valid_date_string = "2024-08-14T12:34:56.789Z"
        assert date_time_validator.validate_format(valid_date_string) is True

    def test_validate_format_invalid(self, date_time_validator):
        """
        Test validate_format with an invalid date-time string.
        """
        invalid_date_string = "2024-08-14 12:34:56"
        assert (
            date_time_validator.validate_format(invalid_date_string) is False
        )

    def test_validate_components_valid(self, date_time_validator):
        """
        Test validate_components with a valid date-time string.
        """
        valid_date_string = "2024-08-14T12:34:56.789Z"
        assert (
            date_time_validator.validate_components(valid_date_string) is True
        )

    def test_validate_components_invalid(self, date_time_validator):
        """
        Test validate_components with an invalid date-time string
        (e.g., invalid date).
        """
        invalid_date_string = "2024-02-30T12:34:56.789Z"  # Invalid date
        assert (
            date_time_validator.validate_components(invalid_date_string)
            is False
        )

    def test_validate_timezone_valid(self, date_time_validator):
        """
        Test validate_timezone with a valid timezone indicator.
        """
        valid_date_string = "2024-08-14T12:34:56.789Z"
        assert date_time_validator.validate_timezone(valid_date_string) is True

    def test_validate_timezone_invalid(self, date_time_validator):
        """
        Test validate_timezone with an invalid timezone indicator.
        """
        invalid_date_string = "2024-08-14T12:34:56.789+01:00"
        assert (
            date_time_validator.validate_timezone(invalid_date_string) is False
        )

    def test_validate_range_within_bounds(self, date_time_validator):
        """
        Test validate_range with a date-time string within the valid range.
        """
        valid_date_string = "2024-08-14T12:34:56.789Z"
        assert date_time_validator.validate_range(valid_date_string) is True

    def test_validate_range_out_of_bounds(self, date_time_validator):
        """
        Test validate_range with a date-time string outside the valid range.
        """
        out_of_bounds_date_string = "1899-12-31T23:59:59.999Z"
        assert (
            date_time_validator.validate_range(out_of_bounds_date_string)
            is False
        )

    def test_validate_all_valid(self, date_time_validator):
        """
        Test the full validate method with a valid date-time string.
        """
        valid_date_string = "2024-08-14T12:34:56.789Z"
        parsed_date = date_time_validator.validate(valid_date_string)
        assert parsed_date == datetime(2024, 8, 14, 12, 34, 56, 789000)

    def test_validate_all_invalid_format(self, date_time_validator):
        """
        Test the full validate method with an invalid format.
        """
        invalid_date_string = "2024-08-14 12:34:56"
        assert date_time_validator.validate(invalid_date_string) is None

    def test_validate_all_out_of_range(self, date_time_validator):
        """
        Test the full validate method with a date-time string
        outside the valid range.
        """
        out_of_bounds_date_string = "1899-12-31T23:59:59.999Z"
        assert date_time_validator.validate(out_of_bounds_date_string) is None
