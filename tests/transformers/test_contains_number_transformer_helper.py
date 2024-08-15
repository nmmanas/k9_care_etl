class TestContainsNumberHelper:
    """
    Test suite for the contains_number method.
    """

    def test_contains_number_with_digit(self, fact_transformer_instance):
        """
        Test contains_number with a string containing numeric digits.
        """
        text = "This string contains the number 42."
        assert fact_transformer_instance.contains_number(text) is True

    def test_contains_number_with_number_word(self, fact_transformer_instance):
        """
        Test contains_number with a string containing a number word.
        """
        text = "This string contains the word 'forty-two'."
        assert fact_transformer_instance.contains_number(text) is True

    def test_contains_number_with_mixed_case_number_word(
        self, fact_transformer_instance
    ):
        """
        Test contains_number with a string containing a mixed case number word.
        """
        text = "This string contains the word 'Forty-Two'."
        assert fact_transformer_instance.contains_number(text) is True

    def test_contains_number_without_any_numbers(
        self, fact_transformer_instance
    ):
        """
        Test contains_number with a string that contains no numeric digits or
        number words.
        """
        text = "This string contains no numbers."
        assert fact_transformer_instance.contains_number(text) is False

    def test_contains_number_with_multiple_number_words(
        self, fact_transformer_instance
    ):
        """
        Test contains_number with a string containing multiple number words.
        """
        text = "The string contains three hundred and forty-two items."
        assert fact_transformer_instance.contains_number(text) is True

    def test_contains_number_with_large_number_word(
        self, fact_transformer_instance
    ):
        """
        Test contains_number with a string containing a large number word.
        """
        text = "The string mentions a billion."
        assert fact_transformer_instance.contains_number(text) is True

    def test_contains_number_with_hyphenated_number_word(
        self, fact_transformer_instance
    ):
        """
        Test contains_number with a string containing a hyphenated number word.
        """
        text = "The string mentions twenty-one."
        assert fact_transformer_instance.contains_number(text) is True

    def test_contains_number_with_edge_case_words(
        self, fact_transformer_instance
    ):
        """
        Test contains_number with edge case words that look similar to number
        words but aren't.
        """
        text = "The word 'tent' should not be mistaken for a number."
        assert fact_transformer_instance.contains_number(text) is False

    def test_contains_number_with_empty_string(
        self, fact_transformer_instance
    ):
        """
        Test contains_number with an empty string.
        """
        text = ""
        assert fact_transformer_instance.contains_number(text) is False

    def test_contains_number_with_non_numeric_symbols(
        self, fact_transformer_instance
    ):
        """
        Test contains_number with a string containing symbols but no numeric
        content.
        """
        text = "The price is $$$."
        assert fact_transformer_instance.contains_number(text) is False
