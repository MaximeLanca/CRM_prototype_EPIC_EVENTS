import pytest
from datetime import datetime
from src.services.customer_service import CustomerService
from src.domain.domain_models import Customer


class FakeCustomerRepository:
    def __init__(self):
        self.customers = []
        self._next_id = 1

    def create_customer(self, customer):
        customer.id__ = self._next_id
        self._next_id += 1
        self.customers.append(customer)
        return customer

    def get_customer_by_id(self, customer_id):
        for customer in self.customers:
            if customer.id__ == customer_id:
                return customer
        return None

    def update_customer(
        self,
        customer_id,
        name=None,
        email=None,
        phone=None,
        company_name=None,
        last_update=None,
        sales_contact=None,
        information=None,
    ):
        customer = self.get_customer_by_id(customer_id)
        if customer:
            if name:
                customer.name = name
            if email:
                customer.email = email

    def delete_customer(self, customer_id):
        customer = self.get_customer_by_id(customer_id)
        if customer:
            self.customers.remove(customer)


class TestCustomerService:

    def setup_method(self):
        self.repository = FakeCustomerRepository()
        self.service = CustomerService(self.repository)

    def test_create_customer_success(self):
        self.service.create_customer(
            "Frank",
            "frank@mail.com",
            "123",
            "Corp",
            None,
            None,
        )
        assert len(self.repository.customers) == 1
        assert self.repository.customers[0].name == "Frank"

    def test_create_customer_has_id(self):
        self.service.create_customer(
            "Frank", "frank@mail.com", "123", "Corp", None, None
        )
        assert self.repository.customers[0].id__ is not None

    def test_get_customer_by_id(self):
        self.service.create_customer(
            "Frank", "frank@mail.com", "123", "Corp", None, None
        )
        customer = self.repository.customers[0]
        result = self.service.get_customer_by_id(customer.id__)
        assert result is not None
        assert result.name == "Frank"

    def test_get_customer_returns_none_if_not_found(self):
        result = self.service.get_customer_by_id(9999)
        assert result is None

    def test_update_customer_name(self):
        self.service.create_customer(
            "Frank", "frank@mail.com", "123", "Corp", None, None
        )
        customer = self.repository.customers[0]
        self.service.update_customer(
            customer.id__, "NewName", None, None, None, None, None, None
        )
        assert self.repository.customers[0].name == "NewName"

    def test_delete_customer(self):
        self.service.create_customer(
            "Frank", "frank@mail.com", "123", "Corp", None, None
        )
        customer = self.repository.customers[0]
        self.service.delete_customer(customer.id__)
        assert len(self.repository.customers) == 0
