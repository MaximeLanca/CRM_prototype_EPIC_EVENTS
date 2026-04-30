from src.repository.operation_repository import ContractRepository, UserRepository, EventRepository, CustomerRepository
from peewee import Database, DoesNotExist
from src.models.peewee_models import ContractModel, UserModel, EventModel, CustomerModel
from src.domain.domain_models import User, Contract, Event, Customer
from datetime import datetime

class PeeweeUserRepository(UserRepository):
    def __init__(self, db: Database):
        self.db = db
    
    def create_user(self, user: User) -> object:
        db_user = UserModel.create(name=user.name, password=user.password, role=user.role)
        user.id__ = db_user.id
        return user
    
    def get_user_by_id(self, user_id: int) -> object:
        try:
            db_user = UserModel.get(UserModel.id == user_id)
            return User(id__=db_user.id, name=db_user.name, password=db_user.password, role=db_user.role)
        except DoesNotExist:
            return None
    
    def update_user_information(self, user_id, name_to_change=None, role_to_change=None):
        db_user = UserModel.get(UserModel.id == user_id)
        if name_to_change is not None:
            db_user.name = name_to_change
        if role_to_change is not None:
            db_user.role = role_to_change
        db_user.save()

    def delete_user_by_id(self, user_id: int) -> list:
        user_db = UserModel.get(UserModel.id == user_id)
        user_informations =[user_db.id , user_db.name, user_db.role]
        user_db.delete_instance()
        return user_informations
        

class PeeweeContractRepository(ContractRepository):
    def __init__(self, db: Database):
        self.db = db

    def create_contract(self, contract:Contract) -> object:
        db_contract = ContractModel.create(sale_contact=contract.sale_contact, total_amount=contract.total_amount, amount_remaining_paid=contract.amount_remaining_paid, customer_informations=contract.customer_informations, status=contract.status)
        return Contract(sale_contact=db_contract.sale_contact, total_amount=db_contract.total_amount,amount_remaining_paid=db_contract.amount_remaining_paid, status=db_contract.status, id__=db_contract.id)
    

    def get_contract_by_id(self, contract_id: int) -> object:
        try:
            db_contract = ContractModel.select().where((ContractModel.id == contract_id)).first()
            db_sale_user = UserModel.select().where((UserModel.id == db_contract.sale_contact)).first()
            print(db_sale_user)
            sale_user = User(id__=db_sale_user.id, name=db_sale_user.name, password=db_sale_user.password, role=db_sale_user.role)
            return Contract(sale_contact=sale_user, total_amount=db_contract.total_amount,amount_remaining_paid=db_contract.amount_remaining_paid, status=db_contract.status, id__=db_contract.id)
        except DoesNotExist:
            return None
        
    def filter_contract(self, status: str) -> list:
        query = ContractModel.select()
        if status == "unsigned":
            query = query.where(ContractModel.status != "signed")
        elif status == "signed":
            query = query.where(ContractModel.status != "unsigned")
        else:
            return []
        return list(query)
        
    def delete_contract_by_id(self, contract_id) -> None:
        try:
            contract = ContractModel.get(ContractModel.id == contract_id)
            contract.delete_instance()
        except DoesNotExist:
            pass

    def update_contract(self, contract_id:int, sale_contact_to_change:int, total_amount_to_change:int, amount_remaining_paid_to_change:int, customer_informations_to_change:str, status_to_change:str):
        db_contract = ContractModel.get(ContractModel.id == contract_id)
        if sale_contact_to_change is not None:
            db_contract.sale_contact = sale_contact_to_change
        if total_amount_to_change is not None:
            db_contract.total_amount = total_amount_to_change
        if amount_remaining_paid_to_change is not None:
            db_contract.amount_remaining_paid = amount_remaining_paid_to_change
        if customer_informations_to_change is not None:
            db_contract.customer_informations = customer_informations_to_change
        if status_to_change is not None:
            db_contract.status = status_to_change
        db_contract.save()

        
class PeeweeEventRepository(EventRepository):
    def __init__(self, db: Database):
        self.db = db

    def create_event(self, event:Event) -> object:
        db_event = EventModel.create(contract=event.contract, 
                                     date_start=event.date_start, 
                                     date_end=event.date_end, 
                                     support_contact=event.support_contact, 
                                     location=event.location, 
                                     attendee=event.attendee, 
                                     note=event.note)
        event.id__ = db_event.id
        return event
    
    def update_event(self, event_id:int, contract_to_change:int, date_start_to_change:datetime, date_end_to_change:datetime, support_contact_to_change:int, location_to_change:str, attendee_to_change:int, note_to_change:str):
        db_event= EventModel.get(EventModel.id == event_id)
        if contract_to_change is not None:
            db_event.contract = contract_to_change
        if date_start_to_change is not None:
            db_event.date_start = date_end_to_change
        if date_end_to_change is not None:
            db_event.date_end = date_end_to_change
        if support_contact_to_change is not None:
            db_event.support_contact = support_contact_to_change
        if location_to_change is not None:
            db_event.location = location_to_change
        if attendee_to_change is not None:
            db_event.note = note_to_change
        db_event.save()

   
    def filter_event(self, support_contact:int) -> list:
        query = EventModel.select()
        query = query.where(EventModel.support_contact == support_contact)
        return list(query)
        
    def delete_event(self, event_id:int) -> None:
        try:
            event = EventModel.get(EventModel.id == event_id)
            event.delete_instance()
        except DoesNotExist:
            pass

    def assign_support_contact(self, event_id:int, support_contact:int) -> object:
        db_user = UserModel.get(UserModel.id == support_contact)
        support_user = User(id__=db_user.id, name=db_user.name, password=db_user.password, role=db_user.role)

        db_event = EventModel.get(EventModel.id == event_id)
        db_event.support_contact = support_contact
        db_event.save()

        db_contract = ContractModel.select().where(ContractModel.id == db_event.contract).first()
        contract = Contract(sale_contact=db_contract.sale_contact, 
                            total_amount=db_contract.total_amount, 
                            amount_remaining_paid=db_contract.amount_remaining_paid, 
                            status=db_contract.status, 
                            created_date=db_contract.created_date, 
                            customer_informations=db_contract.customer_informations,
                            id__=db_contract.id)
        event = Event(contract=contract, 
                      date_start=db_event.date_start,
                      date_end=db_event.date_end, 
                      support_contact=support_user,
                      location=db_event.location, 
                      attendee=db_event.attendee, 
                      note=db_event.note,
                      id__=db_event.id)

        event.support_contact = support_user
        event.contract = contract
        return event

    def get_event_by_id(self, event_id) -> object:
        db_event = EventModel.get(EventModel.id == event_id)
        contract = ContractModel.get(ContractModel.id == db_event.contract)
        support_contact = UserModel.get(UserModel.id == db_event.support_contact)
        return Event(contract = contract, date_start=db_event.date_start, date_end=db_event.date_end, support_contact=support_contact, location=db_event.location, attendee=db_event.attendee, note=db_event.note)
    
class PeeweeCustomerRepository(CustomerRepository):
    def __init__(self, db:Database):
        self.db = db

    def create_customer(self, customer:Customer) -> object:
        customer_db =  CustomerModel.create(name=customer.name,
                                            email=customer.email,
                                            phone=customer.phone,
                                            company_name=customer.company_name,
                                            last_update=customer.last_update,
                                            sales_contact=customer.sales_contact,
                                            information=customer.information)
        customer.id__ = customer_db.id
        return customer

    def update_customer(self, customer_id, name_to_change, email_to_change, phone_to_change, company_name_to_change, last_update, sales_contact_to_change, information_to_change):
        db_customer = CustomerModel.get(CustomerModel.id == customer_id)
        if name_to_change is not None:
            db_customer.name = name_to_change
        if email_to_change is not None:
            db_customer.email = email_to_change
        if phone_to_change is not None:
            db_customer.phone = phone_to_change
        if company_name_to_change is not None:
            db_customer.company_name = company_name_to_change
        if last_update is not None:
            db_customer.last_update = last_update
        if sales_contact_to_change is not None:
            db_customer.sales_contact = sales_contact_to_change
        if information_to_change is not None:
            db_customer.information = information_to_change
        db_customer.save()

    def delete_customer(self, customer_id):
        try:
            customer = CustomerModel.get(CustomerModel.id == customer_id)
            customer.delete_instance()
        except DoesNotExist:
            pass

    def get_customer_by_id(self, customer_id) -> object:
         customer_db = CustomerModel.get(CustomerModel.id == customer_id)
         return Customer(name=customer_db.name,
                         email=customer_db.email,
                         phone=customer_db.phone,
                         company_name=customer_db.company_name,
                         last_update=customer_db.last_update,
                         sales_contact=customer_db.sales_contact,
                         information=customer_db.information,
                         id__=customer_db.id )
