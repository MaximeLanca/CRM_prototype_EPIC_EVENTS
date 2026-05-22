import pytest
from src.tests.conftest import FakeUser


@pytest.fixture(autouse=True)
def setup_db(test_db):
    yield


@pytest.fixture(autouse=True)
def use_fake_user():
    return FakeUser(id__=1, role="sales")
