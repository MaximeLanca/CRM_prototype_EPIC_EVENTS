from src.domain.domain_models import Contract
from src.repository.peewee_operation_repository import PeeweeContractRepository
from src.services.authorization_service import require_permission
from src.models.peewee_models import UserModel
from src.services.session_service import SessionService


class ContractService:
    def __init__(self, PeeweeContractRepository):
        self.repository = PeeweeContractRepository

    @require_permission("create_contract")
    def create_contract(
        self,
        sale_contact: int,
        total_amount: int,
        amount_remaining_paid: int,
        customer_informations: str,
        status: str,
    ) -> object:
        contract = Contract(
            sale_contact=sale_contact,
            total_amount=total_amount,
            amount_remaining_paid=amount_remaining_paid,
            customer_informations=customer_informations,
            status=status,
        )
        return self.repository.create_contract(contract)

    @require_permission("update_contract")
    def update_contract(
        self,
        id__: int,
        sale_contact_to_change: int,
        total_amount_to_change: int,
        amount_remaining_paid_to_change: int,
        customer_informations_to_change: str,
        status_to_change: str,
    ):
        session = SessionService()
        payload, _ = session.get_payload()
        sale_contact_id = int(payload["sub"]) if payload else None 

        contract = self.get_contract_by_id(id__)
        if sale_contact_id != contract.sale_contact:
            return None
        return self.repository.update_contract(
            id__,
            sale_contact_to_change,
            total_amount_to_change,
            amount_remaining_paid_to_change,
            customer_informations_to_change,
            status_to_change,
        )

    @require_permission("delete_contract")
    def delete_contract_by_id(self, id__):
        return self.repository.delete_contract_by_id(id__)

    def get_contract_by_id(self, id__: int) -> Contract:
        return self.repository.get_contract_by_id(id__)

    @require_permission("sort_contract")
    def filter_contract(self, status: str) -> list:
        return self.repository.filter_contract(status)
