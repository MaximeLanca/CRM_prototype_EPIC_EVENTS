import pytest
from src.services.authorization_service import has_permissions
from src.security.token_service import generate_token, save_token, clear_token


class FakeManagement:
    def __init__(self):
        self.id__ = 1
        self.role = "management"


class FakeSales:
    def __init__(self):
        self.id__ = 2
        self.role = "sales"


class FakeSupport:
    def __init__(self):
        self.id__ = 3
        self.role = "support"


class TestPermissions:

    def test_management_can_create_employee(self):
        save_token(generate_token(FakeManagement()))
        assert has_permissions("create_employee") == True

    def test_sales_cannot_create_employee(self):
        save_token(generate_token(FakeSales()))
        assert has_permissions("create_employee") == False

    def test_sales_can_create_event(self):
        save_token(generate_token(FakeSales()))
        assert has_permissions("create_event") == True

    def test_support_can_update_event(self):
        save_token(generate_token(FakeSupport()))
        assert has_permissions("update_event") == True

    def test_support_cannot_create_employee(self):
        save_token(generate_token(FakeSupport()))
        assert has_permissions("create_employee") == False

    def test_management_can_delete_employee(self):
        save_token(generate_token(FakeManagement()))
        assert has_permissions("delete_employee") == True

    def teardown_method(self):
        clear_token()
