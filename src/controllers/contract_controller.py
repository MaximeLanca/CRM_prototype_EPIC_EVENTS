from src.services.contract_service import ContractService
from src.repository.peewee_operation_repository import PeeweeContractRepository
from src.infrastructure.database import db
from src.models.peewee_models import UserModel

class ContractController:
    def __init__(self):
        self.repository = PeeweeContractRepository(db)
        self.service = ContractService(self.repository)

    def create_contract(self, sale_contract:int, total_amount:int, amount_remaining_paid:int, customer_informations:str, status:str) -> object:
        return self.service.create_contract(sale_contract, total_amount, amount_remaining_paid, customer_informations, status) 
    
    def update_contract(self,id__:int, sale_contact_to_change:int, total_amount_to_change:int, amount_remaining_paid_to_change:int, customer_informations_to_change:str, status_to_change:str):
        return self.service.update_contract(id__,sale_contact_to_change,total_amount_to_change,amount_remaining_paid_to_change,customer_informations_to_change,status_to_change)

    def delete_contract_by_id(self, id__:int):
        return self.service.delete_contract_by_id(id__)
    
    def get_contract_by_id(self, id__:int) -> object:
        return self.service.get_contract_by_id(id__)
    
    def filter_contract(self, status:str) -> list:
        return self.service.filter_contract(status)