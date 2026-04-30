from src.services.user_service import UserService
from src.repository.peewee_operation_repository import PeeweeUserRepository
from src.infrastructure.database import db
from src.models.peewee_models import UserModel

class TestLoginFunctional:
    def setup_method(self):
        self.repository = PeeweeUserRepository(db)
        self.service = UserService(self.repository)

    def test_user_can_login_after_creation(self):
        self.service.create_user("John", "12345", "sales")
        db_user = UserModel.get(UserModel.name == "John")
        token = self.service.login(db_user.id, "12345")
        assert token is not None

    def test_login_fails_with_wrong_password(self):
        self.service.create_user("John", "12345", "sales")
        db_user = UserModel.get(UserModel.name == "John")
        token = self.service.login(db_user.id, "bad_password")
        assert token is None

    def test_login_fails_with_unknown_user(self):
        token = self.service.login(9999, "12345")
        assert token is None

class TestLogoutFunctional:
    def setup_method(self):
        self.repository = PeeweeUserRepository(db)
        self.service = UserService(self.repository)

    def test_user_can_login_and_logout(self):
        self.service.create_user("Max", "12345", "management")
        db_user = UserModel.get(UserModel.name == "Max")
        token = self.service.login(db_user.id, "12345")
        assert token is not None
        token = self.service.logout()
        assert token is None
 #TODO commande cli à tester