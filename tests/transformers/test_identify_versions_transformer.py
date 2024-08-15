class TestIdentifyVersionsTransformer:
    """
    Test suite for the identify_versions method in IdentifyVersionsTransformer class.
    """

    def test_identify_versions_empty_data(self, fact_transformer_instance):
        """
        Test identify_versions with an empty data list.
        It should return empty lists for both expired and data.
        """
        result_expired, result_data = fact_transformer_instance.identify_versions([])

        assert result_expired == []
        assert result_data == []

    def test_identify_versions_no_matches(
        self, fact_transformer_instance, version_manager_mock
    ):
        """
        Test identify_versions where no facts match existing versions.
        It should return a list of None values in expired.
        """
        version_manager_mock.match_and_find_version.return_value = None

        data = [{"fact": "Fact 1"}, {"fact": "Fact 2"}]

        result_expired, result_data = fact_transformer_instance.identify_versions(data)

        assert result_expired == [None, None]
        assert result_data == data

    def test_identify_versions_with_matches(
        self, fact_transformer_instance, version_manager_mock
    ):
        """
        Test identify_versions where some facts match existing versions.
        It should return a list of expired fact IDs where matches are found.
        """
        version_manager_mock.match_and_find_version.side_effect = [123, None, 456]

        data = [{"fact": "Fact 1"}, {"fact": "Fact 2"}, {"fact": "Fact 3"}]

        result_expired, result_data = fact_transformer_instance.identify_versions(data)

        assert result_expired == [123, None, 456]
        assert result_data == data

    def test_identify_versions_mixed_results(
        self, fact_transformer_instance, version_manager_mock
    ):
        """
        Test identify_versions with a mix of matching and non-matching facts.
        The result should correctly reflect expired fact IDs and None for unmatched
        ones.
        """
        version_manager_mock.match_and_find_version.side_effect = [None, 101, None, 202]

        data = [
            {"fact": "Fact A"},
            {"fact": "Fact B"},
            {"fact": "Fact C"},
            {"fact": "Fact D"},
        ]

        result_expired, result_data = fact_transformer_instance.identify_versions(data)

        assert result_expired == [None, 101, None, 202]
        assert result_data == data

    def test_identify_versions_all_match(
        self, fact_transformer_instance, version_manager_mock
    ):
        """
        Test identify_versions where all facts match existing versions.
        It should return a list of expired fact IDs.
        """
        version_manager_mock.match_and_find_version.side_effect = [111, 222, 333]

        data = [{"fact": "Fact X"}, {"fact": "Fact Y"}, {"fact": "Fact Z"}]

        result_expired, result_data = fact_transformer_instance.identify_versions(data)

        assert result_expired == [111, 222, 333]
        assert result_data == data
