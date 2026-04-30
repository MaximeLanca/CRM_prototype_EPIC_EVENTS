from src.repository.peewee_operation_repository import PeeweeCustomerRepository
from src.domain.domain_models import Customer
from src.services.authorization_service import require_permission

class CustomerService:
    def __init__ (self,PeeweeCustomerRepository):
        self.repository = PeeweeCustomerRepository

    @require_permission("create_customer")
    def create_customer(self, name:str, email:str, phone:int, company_name:str, last_update:str, sales_contact:int, information:str) -> object:
        customer = Customer(name=name, email=email, phone=phone, company_name=company_name, last_update=last_update, sales_contact=sales_contact, information=information)
        return self.repository.create_customer(customer)
    
    @require_permission("update_customer")
    def update_customer(self, customer_id:int, name_to_change:str, email_to_change:str, phone_to_change:int, company_name_to_change:str, last_update:str, sales_contact_to_change:int, information_to_change:str):
        return  self.repository.update_customer(customer_id, name_to_change, email_to_change, phone_to_change, company_name_to_change, last_update, sales_contact_to_change, information_to_change)
    
    @require_permission("delete_customer")
    def delete_customer(self, customer_id:int):
        return self.repository.delete_customer(customer_id)
    
    def get_customer_by_id(self, customer_id:int):
        return self.repository.get_customer_by_id(customer_id)