from src.repository.peewee_operation_repository import PeeweeUserRepository
from src.infrastructure.database import db
from src.services.user_service import UserService


class UserController:
    def __init__(self):
        self.repository = PeeweeUserRepository(db)
        self.service = UserService(self.repository)

    def create_user(self, name: str, password: str, role: str) -> object:
        return self.service.create_user(name, password, role)

    def login(self, user_id: int, password: str) -> tuple [str, object]:
        return self.service.login(user_id, password)

    def logout(self):
        return self.service.logout()

    def get_user_by_id(self, user_id: int) -> object:
        return self.service.get_user_by_id(user_id)

    def delete_user_by_id(self, user_id: int) -> list:
        return self.service.delete_user_by_id(user_id)

    def update_user_information(
        self, user_id: int, name_to_change: str, role_to_change: str
    ):
        return self.service.update_user_information(
            user_id, name_to_change, role_to_change
        )
