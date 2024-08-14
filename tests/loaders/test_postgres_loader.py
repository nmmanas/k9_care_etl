class TestPostgresLoader:
    """
    The `TestPostgresLoader` class contains tests that test the loader class
    PostgresLoader.
    """

    def test_load_data(self, mocker):
        """
        The `test_load_data` function tests the loading of data into a database using
        mocked psycopg2 connections and cursors.
        """
        # Mock the psycopg2.connect method
        mock_conn = mocker.Mock()
        mock_cursor = mocker.Mock()

        mocker.patch("psycopg2.connect", return_value=mock_conn)
        mock_conn.cursor.return_value = mock_cursor

        # Define test data
        test_data = [
            {"fact": "Dogs are loyal.", "created_date": "2024-05-12T08:17:49.657Z"},
            {
                "fact": "Dogs have a sense of time.",
                "created_date": "2024-07-11T22:49:15.819Z",
            },
        ]
        from ...etl.loaders import PostgresLoader

        # Call the function with test data
        PostgresLoader("test_db_uri").load(test_data)

        # Assertions to check if the correct SQL query was executed with expected data
        insert_query = "INSERT INTO facts (fact, created_date) VALUES (%s, %s)"

        # Check that the execute method was called with the correct SQL query and data
        assert mock_cursor.execute.call_count == len(test_data)
        mock_cursor.execute.assert_any_call(
            insert_query, (test_data[0]["fact"], test_data[0]["created_date"])
        )
        mock_cursor.execute.assert_any_call(
            insert_query, (test_data[1]["fact"], test_data[1]["created_date"])
        )

        # Check that commit, close, and cursor close methods were called
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()
