import pytest
from src.services.contract_service import ContractService
from src.domain.domain_models import Contract


class FakeContractRepository:
    def __init__(self):
        self.contracts = []
        self._next_id = 1

    def create_contract(self, contract):
        contract.id__ = self._next_id
        self._next_id += 1
        self.contracts.append(contract)
        return contract

    def get_contract_by_id(self, contract_id):
        for contract in self.contracts:
            if contract.id__ == contract_id:
                return contract
        return None

    def update_contract(
        self,
        contract_id,
        sale_contact=None,
        total_amount=None,
        amount_remaining_paid=None,
        customer_informations=None,
        status=None,
    ):
        contract = self.get_contract_by_id(contract_id)
        if contract:
            if sale_contact:
                contract.sale_contact = sale_contact
            if total_amount:
                contract.total_amount = total_amount
            if amount_remaining_paid:
                contract.amount_remaining_paid = amount_remaining_paid
            if status:
                contract.status = status

    def delete_contract_by_id(self, contract_id):
        contract = self.get_contract_by_id(contract_id)
        if contract:
            self.contracts.remove(contract)

    def filter_contract(self, status):
        return [c for c in self.contracts if c.status == status]


class TestContractService:

    def setup_method(self):
        self.repository = FakeContractRepository()
        self.service = ContractService(self.repository)

    def test_create_contract_success(self):
        self.service.create_contract(1, 1000, 500, "client", "unsigned")
        assert len(self.repository.contracts) == 1
        assert self.repository.contracts[0].total_amount == 1000

    def test_create_contract_has_id(self):
        self.service.create_contract(1, 1000, 500, "client", "unsigned")
        assert self.repository.contracts[0].id__ is not None

    def test_get_contract_by_id(self):
        self.service.create_contract(1, 1000, 500, "client", "unsigned")
        contract = self.repository.contracts[0]
        result = self.service.get_contract_by_id(contract.id__)
        assert result is not None
        assert result.total_amount == 1000

    def test_get_contract_returns_none_if_not_found(self):
        result = self.service.get_contract_by_id(9999)
        assert result is None

    def test_delete_contract(self):
        self.service.create_contract(1, 1000, 500, "client", "unsigned")
        contract = self.repository.contracts[0]
        self.service.delete_contract_by_id(contract.id__)
        assert len(self.repository.contracts) == 0

    def test_filter_signed_contracts(self):
        self.service.create_contract(1, 1000, 500, "client", "signed")
        self.service.create_contract(1, 2000, 1000, "client", "unsigned")
        result = self.repository.filter_contract("signed")
        assert len(result) == 1
        assert result[0].status == "signed"

    def test_filter_unsigned_contracts(self):
        self.service.create_contract(1, 1000, 500, "client", "signed")
        self.service.create_contract(1, 2000, 1000, "client", "unsigned")
        result = self.repository.filter_contract("unsigned")
        assert len(result) == 1
        assert result[0].status == "unsigned"
