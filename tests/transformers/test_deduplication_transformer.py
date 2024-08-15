import hashlib


class TestDeduplicationTransformer:
    def test_deduplication_empty_list(self, fact_transformer_instance):
        """
        This function tests the deduplication method on an empty list.

        :param fact_transformer_instance: FactTransformer class instance
        """
        data = []
        result = fact_transformer_instance.deduplication(data)
        assert result == []

    def test_deduplication_no_duplicates(
        self, fact_transformer_instance, data_repository_mock
    ):
        """
        This function tests the deduplication method of a fact transformer
        instance when there are no duplicates in the data.

        :param fact_transformer_instance: FactTransformer class instance
        :param data_repository_mock: The `data_repository_mock` is a mock
        object that simulates the behavior of a data repository. In this test
        case, it is being used to mock the  `fact_exists` method to return
        `False`, indicating that no facts exist in the repository.
        """
        data = [{"fact": "Fact 1"}, {"fact": "Fact 2"}, {"fact": "Fact 3"}]

        # Mock fact_exists to return False, meaning no facts exist in the
        # repository
        data_repository_mock.fact_exists.return_value = False

        result = fact_transformer_instance.deduplication(data)

        assert len(result) == len(data)
        for fact in result:
            assert "fact_hash" in fact

    def test_deduplication_with_duplicates(
        self, fact_transformer_instance, data_repository_mock
    ):
        """
        This function tests the deduplication functionality of a fact
        transformer instance by providing a list of facts with duplicates and
        verifying that only unique facts are returned.

        :param fact_transformer_instance: FactTransformer class instance
        :param data_repository_mock: The `data_repository_mock` is a mock
        object that simulates the behavior of a data repository in the test
        environment. In this specific test case, it uses the `fact_exists`
        method of the `data_repository_mock` to check if a fact already exists
        in the repository before deduplicating
        """
        data = [
            {"fact": "Fact 1"},
            {"fact": "Fact 2"},
            {"fact": "Fact 1"},  # Duplicate fact
        ]

        # Mock fact_exists to return False, meaning no facts exist in the
        # repository
        data_repository_mock.fact_exists.return_value = False

        result = fact_transformer_instance.deduplication(data)

        assert len(result) == 2  # Expecting only two unique facts

    def test_deduplication_with_existing_facts(
        self, fact_transformer_instance, data_repository_mock
    ):
        """
        This function tests deduplication functionality by checking for
        existing facts in a data repository and removing duplicates.

        :param fact_transformer_instance: FactTransformer class instance
        :param data_repository_mock: This is a mock object that simulates the
        behavior of a data repository. In this specific test case, it used to
        setting up a side effect for the `fact_exists` method of this mock
        object to return `True` only for "Fact 2
        """
        data = [{"fact": "Fact 1"}, {"fact": "Fact 2"}, {"fact": "Fact 3"}]

        # Mock fact_exists to return True for "Fact 2", meaning it already
        # exists in the repository
        def fact_exists_side_effect(hash_value):
            fact_2_hash = hashlib.md5("Fact 2".encode()).hexdigest()
            return hash_value == fact_2_hash

        data_repository_mock.fact_exists.side_effect = fact_exists_side_effect

        result = fact_transformer_instance.deduplication(data)

        assert (
            len(result) == 2
        )  # Expecting only "Fact 1" and "Fact 3" in the result
        assert all(fact["fact"] != "Fact 2" for fact in result)

    def test_deduplication_all_facts_exist(
        self, fact_transformer_instance, data_repository_mock
    ):
        """
        This function tests the deduplication method with the scenario where
        all facts already exist in the data repository.

        :param fact_transformer_instance: FactTransformer class instance
        :param data_repository_mock: This is a mock object that simulates the
        behavior of a data repository in the test environment. In this specific
        test case, the `fact_exists` method of the `data_repository_mock` is
        being mocked to always return `True` for any fact provided to it.
        """
        data = [{"fact": "Fact 1"}, {"fact": "Fact 2"}, {"fact": "Fact 3"}]

        # Mock fact_exists to return True for all facts
        data_repository_mock.fact_exists.return_value = True

        result = fact_transformer_instance.deduplication(data)

        assert (
            len(result) == 0
        )  # Expecting no facts in the result as all exist in the repository
