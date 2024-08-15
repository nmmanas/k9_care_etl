import pytest
from psycopg2 import OperationalError


class TestPostgresRepository:
    def test_fact_exists_true(self, db_connect_mock, postgres_repository):
        """
        The function `test_fact_exists_true` tests the existence of a fact in a
        PostgreSQL database using mocking in Python.

        :param mocker: Mocker is a library in Python that allows to easily mock
        dependencies in tests.
        :param postgres_repository: The `postgres_repository` parameter is a
        mock instance of PostgresRepository class.
        """

        mock_cursor = db_connect_mock["mock_cursor"]

        mock_cursor.fetchone.return_value = (True,)

        fact_hash = "somehashvalue"
        result = postgres_repository.fact_exists(fact_hash)

        mock_cursor.execute.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "SELECT EXISTS(SELECT 1 FROM facts WHERE fact_hash = %s)",
            (fact_hash,),
        )
        assert result is True

    def test_fact_exists_false(self, db_connect_mock, postgres_repository):
        """
        The function tests if a fact exists in a PostgreSQL database using
        mocking.

        :param mocker: Mocker is a library in Python that allows to easily
        mock dependencies in tests.
        :param postgres_repository: The `postgres_repository` parameter is a
        mock instance of PostgresRepository class.
        """
        mock_cursor = db_connect_mock["mock_cursor"]
        mock_cursor.fetchone.return_value = (False,)

        fact_hash = "somehashvalue"
        result = postgres_repository.fact_exists(fact_hash)

        mock_cursor.execute.assert_called_once_with(
            "SELECT EXISTS(SELECT 1 FROM facts WHERE fact_hash = %s)",
            (fact_hash,),
        )
        assert result is False

    def test_fact_exists_db_error(self, db_connect_mock, postgres_repository):
        """
        The function tests that a database error is raised when checking if a
        fact exists in a PostgreSQL repository.

        :param mocker: Mocker is a library in Python that allows to easily mock
        dependencies in tests.
        :param postgres_repository: The `postgres_repository` parameter is a
        mock instance of PostgresRepository class.
        """
        db_connect_mock[
            "connection_pool_mock"
        ].return_value.getconn.side_effect = OperationalError

        with pytest.raises(OperationalError):
            postgres_repository.fact_exists("somehashvalue")

        db_connect_mock[
            "connection_pool_mock"
        ].return_value.getconn.assert_called_once()
        db_connect_mock[
            "connection_pool_mock"
        ].return_value.putconn.assert_not_called()

    def test_save_facts_batch(self, db_connect_mock, postgres_repository):
        """
        The `test_save_facts_batch` function tests the batch saving of facts to
        a PostgreSQL  repository using mocked objects.

        :param mocker: Mocker is a library in Python that allows to easily mock
        dependencies in tests.
        :param postgres_repository: The `postgres_repository` parameter is a
        mock instance of PostgresRepository class.
        """
        mock_cursor = db_connect_mock["mock_cursor"]

        mock_cursor.fetchone.return_value = [1]
        facts = [
            {
                "fact_hash": "hash1",
                "fact": "Fact 1",
                "created_date": "2024-08-14",
                "is_numeric": True,
            },
            {
                "fact_hash": "hash2",
                "fact": "Fact 2",
                "created_date": "2024-08-14",
                "is_numeric": True,
            },
        ]

        postgres_repository.save_facts_batch(facts)

        # need to check +1 for since get_last_fact_number, calls it
        assert mock_cursor.execute.call_count == len(facts) + 1
        db_connect_mock["mock_conn"].commit.assert_called_once()

    def test_save_facts_batch_empty(
        self, db_connect_mock, postgres_repository
    ):
        """
        The function `test_save_facts_batch_empty` tests the behavior of saving
        an empty batch of facts using a PostgreSQL repository.

        :param mocker: Mocker is a library in Python that allows to easily mock
        dependencies in tests.
        :param postgres_repository: The `postgres_repository` parameter is a
        mock instance of PostgresRepository class.
        """
        facts = []

        postgres_repository.save_facts_batch(facts)

        db_connect_mock["mock_conn"].commit.assert_not_called()

    def test_save_facts_batch_db_error(
        self, db_connect_mock, postgres_repository
    ):
        """
        The function tests that a database error is raised when uploading facts
        to a db using a PostgreSQL repository.

        :param mocker: Mocker is a library in Python that allows to easily mock
        dependencies in tests.
        :param postgres_repository: The `postgres_repository` parameter is a
        mock instance of PostgresRepository class.
        """
        db_connect_mock[
            "connection_pool_mock"
        ].return_value.getconn.side_effect = OperationalError

        facts = [
            {
                "fact_hash": "hash1",
                "fact": "Fact 1",
                "created_date": "2024-08-14",
            },
        ]

        with pytest.raises(OperationalError):
            postgres_repository.save_facts_batch(facts)

        db_connect_mock[
            "connection_pool_mock"
        ].return_value.getconn.assert_called_once()
        db_connect_mock[
            "connection_pool_mock"
        ].return_value.putconn.assert_not_called()

    def test_get_connection_uninitialized_pool(self, postgres_repository):
        """
        Test if exception is raised when connection pool is not initialized.
        """

        from ...etl.repositories import PostgresRepository

        # Force uninitialize the pool
        PostgresRepository._connection_pool = None
        with pytest.raises(
            Exception, match="Connection pool is not initialized"
        ):
            postgres_repository._get_connection()

    def test_fact_exists_exception_handling(
        self, db_connect_mock, postgres_repository
    ):
        """Test that an exception is handled in fact_exists method."""
        db_connect_mock["mock_cursor"].execute.side_effect = OperationalError(
            "DB Error"
        )
        with pytest.raises(OperationalError):
            postgres_repository.fact_exists("some_hash")

    def test_get_last_fact_number_empty_table(
        self, db_connect_mock, postgres_repository
    ):
        """Test get_last_fact_number when the facts table is empty."""
        db_connect_mock["mock_cursor"].fetchone.return_value = [None]
        last_number = postgres_repository.get_last_fact_number()
        assert last_number is None
