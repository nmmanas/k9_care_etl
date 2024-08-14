import pytest


@pytest.fixture
def data_repository_mock(mocker):
    return mocker.Mock()


@pytest.fixture
def fact_transformer_instance(data_repository_mock):
    from ...etl.transformers import FactTransformer

    return FactTransformer(data_repository=data_repository_mock)
