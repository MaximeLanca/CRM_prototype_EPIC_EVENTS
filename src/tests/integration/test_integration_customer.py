from datetime import datetime
from src.models.peewee_models import CustomerModel
from src.domain.domain_models import Customer
from src.infrastructure.database import db
from src.repository.peewee_operation_repository import PeeweeCustomerRepository

class TestCustomerRepositoryIntegration:

    def setup_method(self):
        self.repository = PeeweeCustomerRepository(db)

    def test_create_customer(self):
        customer = Customer(
            name="Client",
            email="test@mail.com",
            phone="123",
            company_name="Corp",
            last_update=datetime.now(),
            sales_contact=None,
            information="info"
        )
        self.repository.create_customer(customer)
        assert CustomerModel.select().count() == 1

    def test_update_customer(self):
        customer = CustomerModel.create(
            name="Client",
            email="test@mail.com",
            phone="123",
            company_name="Corp",
            last_update=datetime.now(),
            information="info"
        )
        self.repository.update_customer(
            customer.id, "NewName", None, None, None, None, None, None
        )
        updated = CustomerModel.get_by_id(customer.id)
        assert updated.name == "NewName"

    def test_delete_customer(self):
        customer = CustomerModel.create(
            name="Client",
            email="test@mail.com",
            phone="123",
            company_name="Corp",
            last_update=datetime.now(),
            information="info"
        )
        self.repository.delete_customer(customer.id)
        assert CustomerModel.select().count() == 0