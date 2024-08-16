import hashlib
import re

from ..logging_config import LoggerManager
from .base_transformer import BaseTransformer
from .constants import hyphenated_numbers_pattern, number_words
from .fact_datetime_validator import DateTimeValidator
from .fact_version_manager import FactVersionManager

logging = LoggerManager.get_logger(__name__)


class FactTransformer(BaseTransformer):
    def __init__(self, data_repository, required_keys=None):
        logging.info("Initialize Transformer")
        self.data_repository = data_repository
        self.version_manager = FactVersionManager(data_repository)
        self.datetime_validator = DateTimeValidator()
        if required_keys is None:
            required_keys = ["fact", "created_date"]
        self.required_keys = required_keys

    @LoggerManager.log_execution
    def transform(self, data):
        """
        Clean and process the input data, returning the transformed result.
        """
        cleaned_data = self.cleanup_data(data)
        processed_data, expired = self.process_data(cleaned_data)
        return processed_data, expired

    @LoggerManager.log_execution
    def cleanup_data(self, data):
        """
        Clean the data by removing whitespaces, dropping blank entries, and
        deduplicating.
        Returns the cleaned data.
        """
        keys_validated = self.validate_keys(data)
        date_validated = self.validate_datetime(keys_validated)
        self.sort_facts_by_created_date(date_validated)
        no_whitespaces = self.clean_whitespaces(date_validated)
        no_blanks = self.drop_blanks(no_whitespaces)
        no_duplicates = self.deduplication(no_blanks)

        return no_duplicates

    @LoggerManager.log_execution
    def sort_facts_by_created_date(self, data):
        data.sort(key=lambda x: x["created_date"])

    @LoggerManager.log_execution
    def process_data(self, data):
        versioned_data, expired = self.identify_versions(data)
        categorized_data = self.categorize_numeric_facts(versioned_data)
        return categorized_data, expired

    @LoggerManager.log_execution
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

    @LoggerManager.log_execution
    def drop_blanks(self, data):
        """
        This functions iterates through the input list and drops any blank
        facts
        """
        facts = []
        for fact in data:
            if fact["fact"] == "":
                logging.info(f"blank 'fact' found in record: {fact}")
                continue
            facts.append(fact)
        return facts

    @LoggerManager.log_execution
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
                logging.info(
                    f"hash already found in the batch: {fact['fact']}"
                )
                continue

            hash_set.add(hash_)

            # check if the fact is present in the data repository
            if self.data_repository.fact_exists(hash_):
                (f"hash already found in the data store: {fact['fact']}")
                continue

            # store hash of the fact for persisting
            fact["fact_hash"] = hash_

            unique_facts.append(fact)

        return unique_facts

    @LoggerManager.log_execution
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
                logging.info(f"fact_id {expired_fact_id} is set to expire")
                expired.append(expired_fact_id)
        return data, expired

    def contains_number(self, text):
        # Check for digits
        if re.search(r"\d", text):
            return True

        # Check for hyphenated number words
        if re.search(hyphenated_numbers_pattern, text, re.IGNORECASE):
            return True

        # Check for exact number words
        words = set(re.findall(r"\b\w+\b", text.lower()))
        if words & number_words:
            return True

        return False

    @LoggerManager.log_execution
    def categorize_numeric_facts(self, data):
        for fact in data:
            if "fact" in fact:
                if self.contains_number(fact["fact"]):
                    fact["is_numeric"] = True
                else:
                    fact["is_numeric"] = False
                logging.info(f"{fact['fact']} is numeric {fact['is_numeric']}")
        return data

    @LoggerManager.log_execution
    def validate_datetime(self, data):
        validated_data = []
        for record in data:
            date_string = record.get("created_date")

            if not date_string:
                logging.info(f"'created_date' is missing in record: {record}")
                continue

            validated_date = self.datetime_validator.validate(date_string)
            if validated_date:
                record["parsed_date"] = validated_date
                validated_data.append(record)
            else:
                logging.info(f"Invalid record: {record}")

        return validated_data

    @LoggerManager.log_execution
    def validate_keys(self, data):
        validated_data = []
        for record in data:
            if all(key in record for key in self.required_keys):
                validated_data.append(record)
            else:
                logging.info(f"Record dropped: {record}")
        return validated_data
