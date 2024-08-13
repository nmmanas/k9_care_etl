class InvalidFileTypeError(Exception):
    """Raised when the expected JSON file is not a JSON file."""

    pass


class MalformedJsonError(Exception):
    """Raised when the JSON file is malformed and cannot be parsed."""

    pass
