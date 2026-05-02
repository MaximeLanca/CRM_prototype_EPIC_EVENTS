from src.models.peewee_models import ContractModel, UserModel
from src.domain.domain_models import Contract
from src.infrastructure.database import db
from src.repository.peewee_operation_repository import PeeweeContractRepository


class TestContractRepositoryIntegration:

    def setup_method(self):
        self.contract_repository = PeeweeContractRepository(db)

    def test_create_contract(self):
        user = UserModel.create(name="John", password="1234", role="sales")
        contract = Contract(
            sale_contact=user.id,
            total_amount=1000,
            amount_remaining_paid=500,
            customer_informations="client",
            status="unsigned",
        )
        result = self.contract_repository.create_contract(contract)
        assert result.id__ is not None

    def test_get_contract_by_id(self):
        user = UserModel.create(name="John", password="1234", role="sales")
        contract = ContractModel.create(
            sale_contact=user.id,
            total_amount=2000,
            amount_remaining_paid=1000,
            customer_informations="client",
            status="unsigned",
        )
        result = self.contract_repository.get_contract_by_id(contract.id)
        assert result is not None
        assert result.id__ == contract.id

    def test_delete_contract(self):
        user = UserModel.create(name="John", password="1234", role="sales")
        contract = ContractModel.create(
            sale_contact=user.id,
            total_amount=100,
            amount_remaining_paid=50,
            customer_informations="client",
            status="unsigned",
        )
        self.contract_repository.delete_contract_by_id(contract.id)
        deleted = ContractModel.get_or_none(ContractModel.id == contract.id)
        assert deleted is None
