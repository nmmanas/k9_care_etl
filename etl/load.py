import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def load_data(data):
    """
    The `load_data` function inserts data into a PostgreSQL database table named
    `facts`.

    :param data: data to be loaded
    eg:
    [
        {"fact": "Dogs are loyal.", "created_date": "2024-05-12T08:17:49.657Z"},
        {
            "fact": "Dogs have a sense of time.",
            "created_date": "2024-07-11T22:49:15.819Z",
        },
    ]
    """
    DB_URI = os.getenv("DB_URI")
    conn = psycopg2.connect(DB_URI)
    cursor = conn.cursor()

    insert_query = "INSERT INTO facts (fact, created_date) VALUES (%s, %s)"

    for item in data:
        cursor.execute(insert_query, (item["fact"], item["created_date"]))

    conn.commit()
    cursor.close()
    conn.close()
