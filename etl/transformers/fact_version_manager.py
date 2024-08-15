from datasketch import MinHash
from rapidfuzz import fuzz
from sklearn.feature_extraction.text import TfidfVectorizer


class FactVersionManager:
    def __init__(
        self, data_repository, num_perm=128, num_buckets=5, threshold=70
    ):
        self.data_repository = data_repository
        self.num_perm = num_perm
        self.num_buckets = num_buckets
        self.threshold = threshold
        self.vectorizer = TfidfVectorizer(stop_words="english")

    def create_lsh_buckets(self, text):
        """
        Create LSH buckets from input text using MinHash and return their
        hashes.
        """
        tfidf_vector = self.vectorizer.fit_transform([text])
        minhash = MinHash(num_perm=self.num_perm)
        for index in tfidf_vector.nonzero()[1]:
            minhash.update(str(index).encode("utf8"))

        bucket_hashes = [
            int.from_bytes(minhash.hashvalues[i].tobytes(), "little")
            for i in range(self.num_buckets)
        ]

        return bucket_hashes

    def get_similar_fact_ids(self, bucket_hashes):
        """
        Retrieve IDs of facts similar to those in the given LSH buckets.
        """

        similar_fact_ids = self.data_repository.find_similar_facts_by_buckets(
            bucket_hashes
        )
        return similar_fact_ids

    def match_and_find_version(self, fact):
        """
        Match the input fact with similar facts and return the ID of the best
        match. Updates the fact with bucket hashes and fact number if a match
        is found.
        """

        current_fact = fact["fact"]
        bucket_hashes = self.create_lsh_buckets(current_fact)
        fact["bucket_hashes"] = bucket_hashes
        candidates = self.get_similar_fact_ids(bucket_hashes)

        if len(candidates) == 0:
            return None

        match_scores = [
            (
                candidate[0],
                candidate[1],
                fuzz.ratio(current_fact, candidate[2]),
            )
            for candidate in candidates
            if fuzz.ratio(current_fact, candidate[2]) > self.threshold
        ]

        if len(match_scores) == 0:
            return None

        top_scorer = max(match_scores, key=lambda x: x[2])
        fact["fact_number"] = top_scorer[1]
        return top_scorer[0]
