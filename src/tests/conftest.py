import pytest
from src.infrastructure.database import db
from src.security.token_service import generate_token, save_token, clear_token
from src.models.peewee_models import UserModel, ContractModel, EventModel, CustomerModel

MODELS = [EventModel, ContractModel, CustomerModel, UserModel]

class FakeAdmin:
    def __init__(self):
        self.id__ = 999
        self.role = 'management'

class FakeUser:
    def __init__(self, id__, role):
        self.id__ = id__
        self.role = role

@pytest.fixture(autouse=True)
def setup_token():
    clear_token()
    save_token(generate_token(FakeAdmin()))
    yield
    clear_token()

@pytest.fixture
def test_db():
    db.init("database_epic_events_test", user='maxime', host='localhost', port=5432)
    db.connect(reuse_if_open=True)
    db.drop_tables(MODELS, safe=True)
    db.create_tables(MODELS, safe=True)
    yield db
    db.drop_tables(MODELS, safe=True)
    db.close()