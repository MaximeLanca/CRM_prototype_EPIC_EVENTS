from src.models.peewee_models import UserModel
from src.infrastructure.database import db
from src.repository.peewee_operation_repository import PeeweeUserRepository
from src.domain.domain_models import User


class TestUserRepositoryIntegration:

    def setup_method(self):
        self.repository = PeeweeUserRepository(db)

    def test_create_user_in_db(self):
        user = User(name="John", password="hashed_pwd", role="sales")
        self.repository.create_user(user)

        db_user = UserModel.get(UserModel.name == "John")
        assert db_user.name == "John"
        assert db_user.role == "sales"

    def test_get_user_by_id(self):
        user_created = UserModel.create(
            name="John", password="hashed_pwd", role="sales"
        )
        user = self.repository.get_user_by_id(user_created.id)
        assert user.name == "John"
