import pytest
from src.tests.conftest import FakeUser


@pytest.fixture(autouse=True)
def setup_db(test_db):
    yield


@pytest.fixture
def use_FakeUser():
    return FakeUser(id__=1, role="sales")


@pytest.fixture
def valid_token(use_FakeUser):
    from src.security.token_service import generate_token

    return generate_token(use_FakeUser)
