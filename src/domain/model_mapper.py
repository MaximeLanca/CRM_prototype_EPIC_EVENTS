from src.domain.domain_models import User, Contract, Event, Customer
from src.models.peewee_models import UserModel, ContractModel, EventModel, CustomerModel

def to_user(db_user: UserModel) -> User:
    if db_user == None:
        return None
    return User(
        id__=db_user.id,
        name=db_user.name,
        password=db_user.password,
        role=db_user.role
    )

def to_contract(db_contract: ContractModel, sale_contact=None) -> Contract:
    return Contract(
        id__=db_contract.id,
        sale_contact=sale_contact,
        total_amount=db_contract.total_amount,
        amount_remaining_paid=db_contract.amount_remaining_paid,
        status=db_contract.status,
        created_date=db_contract.created_date,
        customer_informations=db_contract.customer_informations
    )

def to_event(db_event: EventModel, contract=None, support_contact=None ) -> Event:
    return Event(
        id__=db_event.id,
        contract=contract,
        date_start=db_event.date_start,
        date_end=db_event.date_end,
        support_contact=support_contact,
        location=db_event.location,
        attendee=db_event.attendee,
        note=db_event.note
    )

def to_customer(db_customer: CustomerModel, sale_contact) -> Customer:
    return Customer(
        id__=db_customer.id,
        name=db_customer.name,
        email=db_customer.email,
        phone=db_customer.phone,
        company_name=db_customer.company_name,
        last_update=db_customer.last_update,
        sale_contact=sale_contact,
        information=db_customer.information
    )