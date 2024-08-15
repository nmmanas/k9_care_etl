import pytest


@pytest.fixture
def db_uri():
    return "postgresql://user:password@localhost:5432/testdb"


@pytest.fixture
def postgres_repository(db_uri):
    # Mock the SimpleConnectionPool for the duration of this fixture
    from ...etl.repositories import PostgresRepository

    # Reset the connection pool before each test to avoid shared state issues
    PostgresRepository._connection_pool = None

    return PostgresRepository(db_uri=db_uri)


@pytest.fixture(autouse=True)
def db_connect_mock(mocker):
    # Mock the SimpleConnectionPool
    connection_pool_mock = mocker.patch(
        "psycopg2.pool.SimpleConnectionPool", autouse=True
    )

    # Create a mock connection object
    mock_conn = mocker.MagicMock()

    # Mock the getconn method to return the mock connection
    connection_pool_mock.return_value.getconn.return_value = mock_conn

    # Mock the putconn method to simply return None when called
    connection_pool_mock.return_value.putconn = mocker.MagicMock()

    # Mock the cursor on the mock connection
    mock_cursor = mocker.MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    return {
        "connection_pool_mock": connection_pool_mock,
        "mock_conn": mock_conn,
        "mock_cursor": mock_cursor,
    }
