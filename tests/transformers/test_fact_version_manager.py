import pytest


class TestFactVersionManager:
    def test_create_lsh_buckets_empty_input(self, fact_version_manager):
        """
        Test that create_lsh_buckets raises a ValueError when given an empty
        input string.
        """
        with pytest.raises(
            ValueError
        ):  # TfidfVectorizer might raise a ValueError for empty input
            fact_version_manager.create_lsh_buckets("")

    def test_create_lsh_buckets_single_word(self, fact_version_manager):
        """
        Test that create_lsh_buckets returns the correct number of bucket
        hashes for a single word input. Ensures all returned bucket hashes are
        integers.
        """
        bucket_hashes = fact_version_manager.create_lsh_buckets("word")
        assert len(bucket_hashes) == fact_version_manager.num_buckets
        assert all(isinstance(bh, int) for bh in bucket_hashes)

    def test_create_lsh_buckets_multiple_words(self, fact_version_manager):
        """
        Test that create_lsh_buckets returns the correct number of bucket
        hashes for a multiple words input. Ensures all returned bucket hashes
        are integers.
        """
        bucket_hashes = fact_version_manager.create_lsh_buckets(
            "multiple words input"
        )
        assert len(bucket_hashes) == fact_version_manager.num_buckets
        assert all(isinstance(bh, int) for bh in bucket_hashes)

    def test_get_similar_fact_ids_no_similar_facts(
        self, fact_version_manager, data_repository_mock
    ):
        """
        Test that get_similar_fact_ids returns an empty list when no similar
        facts are found.
        """
        data_repository_mock.find_similar_facts_by_buckets.return_value = []
        similar_fact_ids = fact_version_manager.get_similar_fact_ids([12345])

        assert similar_fact_ids == []

    def test_match_and_find_version_no_similar_facts(
        self, fact_version_manager, data_repository_mock
    ):
        """
        Test that match_and_find_version returns None and does not set
        fact_number when no similar facts are found.
        """
        fact = {"fact": "This is a test fact"}
        data_repository_mock.find_similar_facts_by_buckets.return_value = []

        result = fact_version_manager.match_and_find_version(fact)

        assert result is None
        assert (
            "fact_number" not in fact
        )  # Should not set fact_number if no similar facts

    def test_match_and_find_version_identical_fact(
        self, fact_version_manager, data_repository_mock
    ):
        """
        Test that match_and_find_version returns the ID of an identical fact
        and sets the fact_number.
        """
        fact = {"fact": "This is a test fact"}
        mock_candidates = {
            (1, 101, "This is a test fact"),
        }

        data_repository_mock.find_similar_facts_by_buckets.return_value = (
            mock_candidates
        )

        result = fact_version_manager.match_and_find_version(fact)

        assert result == 1  # Should return the ID of the identical fact
        assert fact["fact_number"] == 101

    def test_match_and_find_version_near_threshold(
        self, fact_version_manager, data_repository_mock
    ):
        """
        Test that match_and_find_version returns the ID of the most similar
        fact if its similarity score is above the threshold.
        """
        fact = {"fact": "This is a test fact"}
        mock_candidates = {
            (1, 101, "This is a test facts"),
            (2, 102, "This is another fact"),
        }

        data_repository_mock.find_similar_facts_by_buckets.return_value = (
            mock_candidates
        )

        result = fact_version_manager.match_and_find_version(fact)

        # It should return the ID of the most similar fact,
        # if it's above the threshold
        assert result is not None
        assert fact["fact_number"] in {101, 102}

    def test_match_and_find_version_below_threshold(
        self, fact_version_manager, data_repository_mock
    ):
        """
        Test that match_and_find_version returns None when no similar fact
        meets the threshold for similarity.
        """
        fact = {"fact": "This is a unique fact"}
        mock_candidates = {
            (1, 101, "This is a very common fact"),
        }

        data_repository_mock.find_similar_facts_by_buckets.return_value = (
            mock_candidates
        )

        result = fact_version_manager.match_and_find_version(fact)

        # Should return None because no match meets the threshold
        assert result is None
