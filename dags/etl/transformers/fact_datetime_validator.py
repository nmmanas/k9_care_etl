import re
from datetime import datetime

from ..logging_config import LoggerManager

logging = LoggerManager.get_logger(__name__)


class DateTimeValidator:
    def __init__(self, min_date=None, max_date=None):
        logging.info("Initialized DateTimeValidator")
        self.min_date = min_date if min_date else datetime(2000, 1, 1)
        self.max_date = max_date if max_date else datetime(2100, 12, 31)
        self.pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$"

    def validate_format(self, date_string):
        if re.match(self.pattern, date_string):
            return True
        else:
            print(f"Invalid format: {date_string}")
            return False

    def validate_components(self, date_string):
        try:
            parsed_date = datetime.strptime(
                date_string, "%Y-%m-%dT%H:%M:%S.%fZ"
            )

            # Example: Additional check for year range
            if parsed_date.year < 1900 or parsed_date.year > 2100:
                print(f"Year out of range: {parsed_date.year}")
                return False

            return True
        except ValueError as e:
            print(f"Error parsing date-time components: {e}")
            return False

    def validate_timezone(self, date_string):
        if date_string.endswith("Z"):
            return True
        else:
            print(f"Timezone indicator missing or incorrect: {date_string}")
            return False

    def validate_range(self, date_string):
        try:
            parsed_date = datetime.strptime(
                date_string, "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            if parsed_date < self.min_date or parsed_date > self.max_date:
                print(f"Date out of valid range: {parsed_date}")
                return False
            return True
        except ValueError as e:
            print(f"Error checking date range: {e}")
            return False

    def validate(self, date_string):
        """
        Perform all validations on the date string.
        Returns the parsed date if valid, otherwise None.
        """
        if (
            self.validate_format(date_string)
            and self.validate_components(date_string)
            and self.validate_timezone(date_string)
            and self.validate_range(date_string)
        ):
            return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            print(f"Validation failed for: {date_string}")
            return None
