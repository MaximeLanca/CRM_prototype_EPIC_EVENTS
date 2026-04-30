import pytest

@pytest.fixture(autouse=True)
def setup_db(test_db): 
    yield


# TODO Creer les tests pour contract et event