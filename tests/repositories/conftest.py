import pytest


@pytest.fixture
def db_uri():
    return "postgresql://user:password@localhost:5432/testdb"


@pytest.fixture
def postgres_repository(db_uri):
    from ...etl.repositories import PostgresRepository

    return PostgresRepository(db_uri=db_uri)


@pytest.fixture
def db_connect_mock(mocker):
    # Mocking psycopg2.connect
    return mocker.patch("psycopg2.connect")
