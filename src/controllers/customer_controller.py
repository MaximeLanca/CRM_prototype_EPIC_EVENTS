from src.infrastructure.database import db
from src.repository.peewee_operation_repository import PeeweeCustomerRepository
from src.services.customer_service import CustomerService

class CustomerController:
    def __init__(self):
        self.repository = PeeweeCustomerRepository(db)
        self.service = CustomerService(self.repository)

    def create_customer(self, name:str, email:str, phone:int, company_name:str, last_update:str, sales_contact:int, information:str) -> object:
        return self.service.create_customer(name, email, phone, company_name, last_update, sales_contact, information)
    
    def update_customer(self, customer_id:int, name_to_change:str, email_to_change:str, phone_to_change:int, company_name_to_change:str, last_update, sales_contact_to_change:int, information_to_change:str):
        return self.service.update_customer(customer_id, name_to_change, email_to_change, phone_to_change, company_name_to_change, last_update, sales_contact_to_change, information_to_change)
    
    def delete_customer(self, customer_id:int):
        return self.service.delete_customer(customer_id)
    
    def get_customer_by_id(self,customer_id:int) -> object:
        return self.service.get_customer_by_id(customer_id)