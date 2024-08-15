import pytest
from psycopg2 import OperationalError


class TestFindSimilarFacts:
    def test_find_similar_facts_no_buckets(
        self, db_connect_mock, postgres_repository
    ):
        """
        Test case where no bucket hashes are provided
        """
        mock_cursor = db_connect_mock["mock_cursor"]
        mock_cursor.fetchall.return_value = []

        result = postgres_repository.find_similar_facts_by_buckets([])

        assert (
            result == []
        )  # Should return an empty list when no buckets are provided

    def test_find_similar_facts_single_bucket(
        self, db_connect_mock, postgres_repository
    ):
        """
        Test case with a single bucket hash
        """
        mock_cursor = db_connect_mock["mock_cursor"]
        mock_cursor.fetchall.return_value = [(1, 101, "Fact 1")]

        result = postgres_repository.find_similar_facts_by_buckets(["hash1"])

        assert result == [
            (1, 101, "Fact 1")
        ]  # Should return the fact associated with the bucket hash

    def test_find_similar_facts_multiple_buckets(
        self, db_connect_mock, postgres_repository
    ):
        """
        Test case with multiple bucket hashes
        """
        mock_cursor = db_connect_mock["mock_cursor"]
        mock_cursor.fetchall.side_effect = [
            [(1, 101, "Fact 1")],
            [(2, 102, "Fact 2"), (3, 103, "Fact 3")],
        ]

        result = postgres_repository.find_similar_facts_by_buckets(
            ["hash1", "hash2"]
        )

        expected_result = [
            (1, 101, "Fact 1"),
            (2, 102, "Fact 2"),
            (3, 103, "Fact 3"),
        ]
        assert sorted(result) == sorted(
            expected_result
        )  # Should return facts associated with both bucket hashes

    def test_find_similar_facts_duplicate_entries(
        self, db_connect_mock, postgres_repository
    ):
        """
        Test case with duplicate entries across bucket hashes
        """
        mock_cursor = db_connect_mock["mock_cursor"]
        mock_cursor.fetchall.side_effect = [
            [(1, 101, "Fact 1")],
            [(1, 101, "Fact 1"), (2, 102, "Fact 2")],
        ]

        result = postgres_repository.find_similar_facts_by_buckets(
            ["hash1", "hash2"]
        )

        expected_result = [(1, 101, "Fact 1"), (2, 102, "Fact 2")]
        assert sorted(result) == sorted(
            expected_result
        )  # Should deduplicate the facts

    def test_find_similar_facts_db_error(
        self, db_connect_mock, postgres_repository
    ):
        """
        Test case where the database connection fails
        """
        # Mock the getconn() method to raise an OperationalError
        db_connect_mock[
            "connection_pool_mock"
        ].return_value.getconn.side_effect = OperationalError

        with pytest.raises(OperationalError):
            postgres_repository.find_similar_facts_by_buckets(["hash1"])

        # Ensure getconn was called
        db_connect_mock[
            "connection_pool_mock"
        ].return_value.getconn.assert_called_once()

        # Ensure putconn was not called since connection was never successfully
        # retrieved
        db_connect_mock[
            "connection_pool_mock"
        ].return_value.putconn.assert_not_called()
