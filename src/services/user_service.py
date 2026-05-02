from src.domain.domain_models import User
from src.security.token_service import generate_token, save_token, clear_token
from src.repository.peewee_operation_repository import PeeweeUserRepository
from src.security.password_service import verify_password, hash_password
from src.services.session_service import SessionService
from src.services.authorization_service import require_permission


class UserService:
    def __init__(self, PeeweeUserRepository):
        self.repository = PeeweeUserRepository
        self.user_session = SessionService()

    def login(self, user_id: int, password: str):
        user = self.get_user_by_id(user_id)
        if not user:
            print("User don't exist.")
            return None
        if not verify_password(user.password, password):
            print("Password is invalid.")
            return None
        token = generate_token(user)
        save_token(token)
        return token

    def logout(self):
        clear_token()

    @require_permission("create_employee")
    def create_user(self, name: str, password: str, role: str) -> object:
        hashed = hash_password(password)
        user = User(name=name, password=hashed, role=role)
        return self.repository.create_user(user)

    def get_user_by_id(self, user_id: int) -> object:
        return self.repository.get_user_by_id(user_id)

    @require_permission("delete_employee")
    def delete_user_by_id(self, user_id: int) -> list:
        return self.repository.delete_user_by_id(user_id)

    @require_permission("update_employee")
    def update_user_information(self, user_id, name_to_change, role_to_change):
        return self.repository.update_user_information(
            user_id, name_to_change, role_to_change
        )
