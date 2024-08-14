import psycopg2

from .base_loader import BaseLoader


class PostgresLoader(BaseLoader):
    def __init__(self, db_uri):
        self.db_uri = db_uri

    def load(self, data):
        """
        The `load` function inserts data into a PostgreSQL database table named `facts`
        using psycopg2.

        :param data: The method takes a parameter `data`, which is expected to be a list
        of dictionaries where each dictionary represents a row to be inserted into the
        `facts` table
        """
        conn = psycopg2.connect(self.db_uri)
        cursor = conn.cursor()

        insert_query = "INSERT INTO facts (fact, created_date) VALUES (%s, %s)"

        for item in data:
            cursor.execute(insert_query, (item["fact"], item["created_date"]))

        conn.commit()
        cursor.close()
        conn.close()
