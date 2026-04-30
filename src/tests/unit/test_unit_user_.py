import pytest
from src.services.user_service import UserService
from src.domain.domain_models import User
from src.security.token_service import generate_token, save_token, clear_token

class FakeUserRepository:
    def __init__(self):
        self.users = []
        self._next_id = 1

    def create_user(self, user):
        user.id__ = self._next_id
        self._next_id += 1
        self.users.append(user)
        return user

    def get_user_by_id(self, user_id):
        for user in self.users:
            if user.id__ == user_id:
                return user
        return None

    def update_user_information(self, user_id, name_to_change=None, role_to_change=None):
        user = self.get_user_by_id(user_id)
        if user:
            if name_to_change:
                user.name = name_to_change
            if role_to_change:
                user.role = role_to_change

    def delete_user_by_id(self, user_id):
        user = self.get_user_by_id(user_id)
        if user:
            self.users.remove(user)
            return [user.id__, user.name, user.role]
        return None

class TestUserService:

    def setup_method(self):
        self.repository = FakeUserRepository()
        self.service = UserService(self.repository)

    def test_create_user_success(self):
        self.service.create_user("John", "12345", "sales")
        assert len(self.repository.users) == 1
        assert self.repository.users[0].name == "John"
        assert self.repository.users[0].role == "sales"

    def test_create_user_password_is_hashed(self):
        self.service.create_user("John", "12345", "sales")
        assert self.repository.users[0].password != "12345"

    def test_login_returns_token_if_correct(self):
        self.service.create_user("John", "12345", "sales")
        user = self.repository.users[0]
        token = self.service.login(user.id__, "12345")
        assert token is not None

    def test_login_returns_none_if_wrong_password(self):
        self.service.create_user("John", "12345", "sales")
        user = self.repository.users[0]
        token = self.service.login(user.id__, "mauvais_password")
        assert token is None

    def test_login_returns_none_if_user_not_found(self):
        token = self.service.login(9999, "12345")
        assert token is None

    def test_update_user_name(self):
        self.service.create_user("John", "12345", "sales")
        user = self.repository.users[0]
        self.service.update_user_information(user.id__, "NewName", None)
        assert self.repository.users[0].name == "NewName"

    def test_delete_user(self):
        self.service.create_user("John", "12345", "sales")
        user = self.repository.users[0]
        self.service.delete_user_by_id(user.id__)
        assert len(self.repository.users) == 0