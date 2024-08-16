import pytest


@pytest.fixture
def data_repository_mock(mocker):
    return mocker.Mock()


@pytest.fixture
def version_manager_mock(mocker):
    """
    Fixture to create a mock of the version_manager dependency.
    """
    return mocker.Mock()


@pytest.fixture
def datetime_validator_mock(mocker):
    """
    Fixture to create a mock of the validator dependency.
    """
    return mocker.Mock()


@pytest.fixture
def fact_transformer_instance(
    data_repository_mock, version_manager_mock, datetime_validator_mock
):
    from ...etl.transformers import FactTransformer

    transformer = FactTransformer(data_repository=data_repository_mock)
    transformer.version_manager = version_manager_mock
    transformer.datetime_validator = datetime_validator_mock

    return transformer


@pytest.fixture
def fact_version_manager(data_repository_mock):
    from ...etl.transformers import FactVersionManager

    return FactVersionManager(data_repository_mock)


@pytest.fixture
def date_time_validator():
    """
    Fixture to create an instance of DateTimeValidator
    with default min and max dates.
    """
    from ...etl.transformers import DateTimeValidator

    return DateTimeValidator()
