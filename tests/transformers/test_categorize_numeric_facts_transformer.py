import pytest


class TestCategorizeNumericFacts:
    """
    Test suite for the categorize_numeric_facts method.
    """

    @pytest.fixture
    def fact_transformer_instance(self, mocker, data_repository_mock):
        """
        Fixture to create an instance of the class containing the categorize_numeric_facts method.
        """

        from ...etl.transformers import FactTransformer

        instance = FactTransformer(data_repository=data_repository_mock)

        # Mock the contains_number method
        mocker.patch.object(instance, "contains_number", autospec=True)
        return instance

    def test_categorize_numeric_facts_all_numeric(
        self, fact_transformer_instance
    ):
        """
        Test categorize_numeric_facts where all facts contain numbers.
        """
        fact_transformer_instance.contains_number.return_value = True

        data = [{"fact": "Fact 1"}, {"fact": "There are twenty apples."}]

        result = fact_transformer_instance.categorize_numeric_facts(data)

        assert all(fact["is_numeric"] is True for fact in result)

    def test_categorize_numeric_facts_all_non_numeric(
        self, fact_transformer_instance
    ):
        """
        Test categorize_numeric_facts where no facts contain numbers.
        """
        fact_transformer_instance.contains_number.return_value = False

        data = [
            {"fact": "This is a fact."},
            {"fact": "Another non-numeric fact."},
        ]

        result = fact_transformer_instance.categorize_numeric_facts(data)

        assert all(fact["is_numeric"] is False for fact in result)

    def test_categorize_numeric_facts_mixed(self, fact_transformer_instance):
        """
        Test categorize_numeric_facts with a mix of numeric and non-numeric facts.
        """
        data = [
            {"fact": "Fact 1"},
            {"fact": "This is not numeric."},
            {"fact": "There are twenty apples."},
            {"fact": "Just some words."},
        ]

        # Mock contains_number to return True for specific facts
        fact_transformer_instance.contains_number.side_effect = [
            True,
            False,
            True,
            False,
        ]

        result = fact_transformer_instance.categorize_numeric_facts(data)

        assert result[0]["is_numeric"] is True
        assert result[1]["is_numeric"] is False
        assert result[2]["is_numeric"] is True
        assert result[3]["is_numeric"] is False

    def test_categorize_numeric_facts_empty_list(
        self, fact_transformer_instance
    ):
        """
        Test categorize_numeric_facts with an empty list.
        It should return an empty list.
        """
        data = []

        result = fact_transformer_instance.categorize_numeric_facts(data)

        assert result == []

    def test_categorize_numeric_facts_no_fact_key(
        self, fact_transformer_instance
    ):
        """
        Test categorize_numeric_facts with items missing the 'fact' key.
        It should handle them without raising an error.
        """
        data = [
            {"text": "This entry has no fact key."},
            {"fact": "This is numeric 100."},
        ]

        # Mock contains_number to return True only for valid facts
        fact_transformer_instance.contains_number.side_effect = lambda x: (
            "100" in x if isinstance(x, str) else False
        )

        result = fact_transformer_instance.categorize_numeric_facts(data)
        assert (
            result[0].get("is_numeric") is None
        )  # No 'fact' key, so no categorization
        assert result[1]["is_numeric"] is True
