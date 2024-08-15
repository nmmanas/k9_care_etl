import pytest


@pytest.fixture
def data_repository_mock(mocker):
    return mocker.Mock()


@pytest.fixture
def fact_transformer_instance(data_repository_mock):
    from ...etl.transformers import FactTransformer

    return FactTransformer(data_repository=data_repository_mock)


@pytest.fixture
def fact_version_manager(data_repository_mock):
    from ...etl.transformers import FactVersionManager

    return FactVersionManager(data_repository_mock)
