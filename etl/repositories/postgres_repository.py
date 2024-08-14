import psycopg2

from .base_repository import BaseRepository


class PostgresRepository(BaseRepository):
    def __init__(self, db_uri):
        self.db_uri = db_uri

    def fact_exists(self, fact_hash):
        conn = psycopg2.connect(self.db_uri)
        cursor = conn.cursor()
        query = "SELECT EXISTS(SELECT 1 FROM facts WHERE fact_hash = %s)"
        cursor.execute(query, (fact_hash,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0]

    def save_facts_batch(self, facts):
        if len(facts) == 0:
            return
        conn = psycopg2.connect(self.db_uri)
        cursor = conn.cursor()
        insert_query = (
            "INSERT INTO facts (fact_hash, fact, created_date) VALUES (%s, %s, %s)"
        )

        for item in facts:
            cursor.execute(
                insert_query,
                (item["fact_hash"], item["fact"], item["created_date"]),
            )
        conn.commit()
        cursor.close()
        conn.close()
