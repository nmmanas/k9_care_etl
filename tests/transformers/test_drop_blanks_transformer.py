class TestDropBlanksTransformer:

    def test_drop_blanks_no_blanks(self, fact_transformer_instance):
        data = [{"fact": "Fact 1"}, {"fact": "Fact 2"}, {"fact": "Fact 3"}]

        result = fact_transformer_instance.drop_blanks(data)

        assert result == data  # No facts should be dropped

    def test_drop_blanks_with_blanks(self, fact_transformer_instance):
        data = [
            {"fact": "Fact 1"},
            {"fact": ""},
            {"fact": "Fact 2"},
            {"fact": ""},
            {"fact": "Fact 3"},
        ]

        expected_result = [{"fact": "Fact 1"}, {"fact": "Fact 2"}, {"fact": "Fact 3"}]

        result = fact_transformer_instance.drop_blanks(data)

        assert result == expected_result  # Only non-blank facts should remain

    def test_drop_blanks_all_blanks(self, fact_transformer_instance):
        data = [{"fact": ""}, {"fact": ""}, {"fact": ""}]

        result = fact_transformer_instance.drop_blanks(data)

        assert (
            result == []
        )  # All facts are blank, so the result should be an empty list

    def test_drop_blanks_empty_list(self, fact_transformer_instance):
        data = []

        result = fact_transformer_instance.drop_blanks(data)

        assert (
            result == []
        )  # The input is an empty list, so the result should also be an empty list

    def test_drop_blanks_mixed_content(self, fact_transformer_instance):
        data = [
            {"fact": ""},
            {"fact": "Fact 1"},
            {"fact": " "},  # A single space is not considered blank
            {"fact": ""},
            {"fact": "\t"},  # A tab is not considered blank
            {"fact": "Fact 2"},
        ]

        expected_result = [
            {"fact": "Fact 1"},
            {"fact": " "},  # A single space should remain
            {"fact": "\t"},  # A tab should remain
            {"fact": "Fact 2"},
        ]

        result = fact_transformer_instance.drop_blanks(data)

        assert (
            result == expected_result
        )  # Only the actual blank facts should be removed
