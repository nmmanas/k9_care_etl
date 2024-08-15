import hashlib

from spellchecker import SpellChecker

from .base_transformer import BaseTransformer
from .fact_version_manager import FactVersionManager


class FactTransformer(BaseTransformer):
    def __init__(self, data_repository):
        self.data_repository = data_repository
        self.version_manager = FactVersionManager(data_repository)

    def transform(self, data):
        """
        Clean and process the input data, returning the transformed result.
        """
        cleaned_data = self.cleanup_data(data)
        processed_data, expired = self.process_data(cleaned_data)
        return processed_data, expired

    def cleanup_data(self, data):
        """
        Clean the data by removing whitespaces, dropping blank entries, and
        deduplicating.
        Returns the cleaned data.
        """
        no_whitespaces = self.clean_whitespaces(data)
        no_blanks = self.drop_blanks(no_whitespaces)
        no_duplicates = self.deduplication(no_blanks)

        return no_duplicates

    def process_data(self, data):
        expired, versioned_data = self.identify_versions(data)
        return versioned_data, expired

    def clean_whitespaces(self, data):
        """
        This function removes extra whitespaces from the "fact" field in each
        dictionary within the input data list.

        :param data: The `clean_whitespaces` function takes a list of
        dictionaries as input, where each dictionary has a key "fact"
        containing a string value. The function then removes extra whitespaces
        from the "fact" values in each dictionary by splitting the string into
        words, joining them back with a single space

        :return: The `clean_whitespaces` function returns the `data` after
        cleaning whitespaces in the "fact" field of each item in the data list.
        """
        for fact in data:
            fact["fact"] = " ".join(fact["fact"].split()).strip()
        return data

    def drop_blanks(self, data):
        """
        This functions iterates through the input list and drops any blank
        facts
        """
        facts = []
        for fact in data:
            if fact["fact"] == "":
                continue
            facts.append(fact)
        return facts

    def correct_typos(self, data):
        """
        The function corrects typos in a list of facts by using a SpellChecker
        to correct words and maintain capitalization.

        :param data: facts dictionary in following format:
            [
                {
                    "fact": "fact 1",
                    "created_date": "<date>"
                }
            ]
        :return: The `correct_typos` method returns the `data` after correcting
        any typos in the "fact" field of each item in the data. The typos are
        corrected using the `SpellChecker` class, and the corrected words are
        stored back in the "fact" field before returning the updated `data`.
        """
        spell = SpellChecker()

        for fact in data:
            corrected_words = []
            for word in fact["fact"].split():
                # Check if the word is capitalized or in uppercase
                if word.isupper():
                    corrected_word = spell.correction(word).upper()
                elif word[0].isupper():
                    corrected_word = spell.correction(word).capitalize()
                else:
                    corrected_word = spell.correction(word)
                corrected_words.append(corrected_word)
            fact["fact"] = " ".join(corrected_words)
        return data

    def deduplication(self, data):
        """
        The `deduplication` function removes duplicate facts from the input
        data based on their MD5 hash values. It takes a list of dictionaries as
        input. Each dictionary in the list is expected to have a key "fact"
        containing a fact string. The method then deduplicates the list based
        on the MD5 hash of the fact.

        :param data: List of dictionaries as input.

        :return: The function `deduplication` returns a list of unique facts
        after removing any duplicates based on the hash value of the fact.
        """
        hash_set = set()
        unique_facts = []
        for fact in data:
            # compute md5 hash for the fact
            hash_ = hashlib.md5(fact["fact"].encode()).hexdigest()

            # check if we saw the fact in this batch and skip if yes
            if hash_ in hash_set:
                continue

            hash_set.add(hash_)

            # check if the fact is present in the data repository
            if self.data_repository.fact_exists(hash_):
                continue

            # store hash of the fact for persisting
            fact["fact_hash"] = hash_

            unique_facts.append(fact)

        return unique_facts

    def identify_versions(self, data):
        """
        Identify and manage versions of facts:
        1. Create LSH buckets for the current fact.
        2. Find similar facts by buckets from the database.
        3. Fuzzy compare against similar facts.
        4. If the matching score exceeds the threshold, identify as a new
           version.
        5. Save the new version to the database and mark the old version as
           expired.
        6. Save LSH buckets in the database.
        """
        expired = []
        for fact in data:
            expired_fact_id = self.version_manager.match_and_find_version(fact)
            if expired_fact_id:
                expired.append(expired_fact_id)
        return expired, data
