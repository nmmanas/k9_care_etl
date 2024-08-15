class TestFactsLoader:
    """
    The `TestPostgresLoader` class contains tests that test the loader class
    PostgresLoader.
    """

    def test_load_data(self, mocker):
        """
        The `test_load_data` function tests the loading of data into a database
        using mocked psycopg2 connections and cursors.
        """

        # Define test data
        test_data = [
            {
                "fact": "Dogs are loyal.",
                "created_date": "2024-05-12T08:17:49.657Z",
            },
            {
                "fact": "Dogs have a sense of time.",
                "created_date": "2024-07-11T22:49:15.819Z",
            },
        ]
        # Mock the psycopg2.connect method
        data_repository = mocker.Mock()
        from ...etl.loaders import FactsLoader

        # Call the function with test data
        FactsLoader(data_repository).load(test_data, [])
        data_repository.save_facts_batch.assert_called_once()
