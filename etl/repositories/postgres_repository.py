import psycopg2

from .base_repository import BaseRepository


class PostgresRepository(BaseRepository):
    _connection_pool = None

    def __init__(self, db_uri):
        if PostgresRepository._connection_pool is None:
            PostgresRepository._connection_pool = (
                psycopg2.pool.SimpleConnectionPool(
                    minconn=1, maxconn=10, dsn=db_uri
                )
            )

    @staticmethod
    def _get_connection():
        if PostgresRepository._connection_pool is None:
            raise Exception("Connection pool is not initialized")
        return PostgresRepository._connection_pool.getconn()

    @staticmethod
    def _release_connection(conn):
        PostgresRepository._connection_pool.putconn(conn)

    def fact_exists(self, fact_hash):
        conn = None
        cursor = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            query = "SELECT EXISTS(SELECT 1 FROM facts WHERE fact_hash = %s)"
            cursor.execute(query, (fact_hash,))
            result = cursor.fetchone()
            return result[0]
        except Exception as e:
            print(f"An error occurred: {e}")
            raise
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                self._release_connection(conn)

    def get_last_fact_number(self):
        conn = None
        cursor = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            # Query to get the last used number
            cursor.execute("SELECT MAX(fact_number) FROM facts;")
            last_number = cursor.fetchone()[0]

            return last_number

        except Exception as e:
            print(f"An error occurred: {e}")
            raise
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                self._connection_pool(conn)

    def save_facts_batch(self, facts):
        conn = None
        cursor = None
        if len(facts) == 0:
            return
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            insert_query = """
                INSERT INTO facts
                (fact_number, fact_hash, fact, created_date, is_numeric)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
                """

            last_fact_number = None
            last_fact_number = self.get_last_fact_number()
            if last_fact_number is None:
                last_fact_number = 0
            for item in facts:
                if "fact_number" in item:
                    fact_number = item["fact_number"]
                else:
                    last_fact_number += 1
                    fact_number = last_fact_number
                cursor.execute(
                    insert_query,
                    (
                        fact_number,
                        item["fact_hash"],
                        item["fact"],
                        item["created_date"],
                        item["is_numeric"],
                    ),
                )

                if "bucket_hashes" in item:
                    auto_increment_id = cursor.fetchone()[0]
                    self.save_lsh_buckets_for_fact(
                        auto_increment_id, item["bucket_hashes"], cursor=cursor
                    )
            conn.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            if conn is not None:
                conn.rollback()
            raise
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                self._connection_pool(conn)

    def find_similar_facts_by_buckets(self, bucket_hashes):
        conn = None
        cursor = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            facts = set()
            for bucket_hash in bucket_hashes:
                cursor.execute(
                    """
                    SELECT fact_id, fact_number, facts.fact
                    FROM lsh_buckets
                    JOIN facts
                    ON facts.id = lsh_buckets.fact_id
                        AND facts.is_current = true
                    WHERE bucket_hash = %s
                    """,
                    (bucket_hash,),
                )
                facts.update(
                    [(row[0], row[1], row[2]) for row in cursor.fetchall()]
                )
            return list(facts)
        except Exception as e:
            print(f"An error occurred: {e}")
            if conn is not None:
                conn.rollback()
            raise
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                self._connection_pool(conn)

    def save_lsh_buckets_for_fact(self, fact_id, bucket_hashes, cursor=None):
        """
        Store the LSH bucket hashes for a given fact_id in the lsh_buckets
        table.

        :param fact_id: The ID of the fact in the facts table
        :param bucket_hashes: A list of bucket hashes generated for the fact
        """
        conn = None
        try:
            local_cursor = False
            if cursor is None:
                conn = self._get_connection()
                cursor = conn.cursor()
                local_cursor = True
            for bucket_hash in bucket_hashes:
                cursor.execute(
                    """
                    INSERT INTO lsh_buckets (fact_id, bucket_hash)
                    VALUES (%s, %s)""",
                    (fact_id, bucket_hash),
                )
        except Exception as e:
            print(f"An error occurred: {e}")
            if local_cursor:
                conn.rollback()
            raise
        finally:
            if local_cursor:
                if cursor is not None:
                    cursor.close()
                if conn is not None:
                    self._connection_pool(conn)

    def mark_as_expired(self, data):
        conn = None
        cursor = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            for expired_fact_id in data:
                cursor.execute(
                    """
                    UPDATE facts
                    SET is_current = false, effective_end_date = now()
                    WHERE id = %s;""",
                    (expired_fact_id,),
                )
            conn.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            if conn is not None:
                conn.rollback()
            raise
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                self._connection_pool(conn)
