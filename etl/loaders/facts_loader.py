from .base_loader import BaseLoader


class FactsLoader(BaseLoader):
    def __init__(self, data_repository):
        self.data_repository = data_repository

    def load(self, data):
        """
        The `load` function inserts data into a PostgreSQL database table named `facts`
        using psycopg2.

        :param data: The method takes a parameter `data`, which is expected to be a list
        of dictionaries where each dictionary represents a row to be inserted into the
        `facts` table
        """
        self.data_repository.save_facts_batch(data)
