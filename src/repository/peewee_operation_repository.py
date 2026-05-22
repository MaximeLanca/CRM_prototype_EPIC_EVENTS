from src.repository.operation_repository import (
    ContractRepository,
    UserRepository,
    EventRepository,
    CustomerRepository,
)
import sentry_sdk
from datetime import datetime
from peewee import Database, DoesNotExist
from src.models.peewee_models import ContractModel, UserModel, EventModel, CustomerModel
from src.domain.domain_models import User, Contract, Event, Customer
from datetime import datetime
from src.domain.model_mapper import (
    to_contract,
    to_customer,
    to_event,
    to_user,
    to_customer,
)


class PeeweeUserRepository(UserRepository):
    def __init__(self, db: Database):
        self.db = db

    def create_user(self, user: User) -> object:
        db_user = UserModel.create(
            name=user.name, password=user.password, role=user.role
        )
        user.id__ = db_user.id
        now = datetime.now()
        sentry_sdk.capture_message(
            f"The user [ID N° {user.id__}, Name: {user.name}] has been created at {now.strftime("%d/%m/%Y %H:%M:%S")}",
            level="info",
        )
        return user

    def get_user_by_id(self, user_id: int) -> object:
        try:
            db_user = UserModel.get(UserModel.id == user_id)
            return to_user(db_user)

        except DoesNotExist:
            return None

    def update_user_information(
        self, user_id, name_to_change=None, role_to_change=None
    ):
        db_user = UserModel.select().where(UserModel.id == user_id).first()
        if name_to_change is not None:
            db_user.name = name_to_change
        if role_to_change is not None:
            db_user.role = role_to_change
        if name_to_change is None and role_to_change is None:
            return
        else:
            now = datetime.now()
            sentry_sdk.capture_message(
                f"The user's information [ID N° {db_user.id}, Name: {db_user.name}] has been updated at {now.strftime("%d/%m/%Y %H:%M:%S")}",
                level="info",
            )
            db_user.save()

    def delete_user_by_id(self, user_id: int) -> list:
        user_db = UserModel.select().where(UserModel.id == user_id).first()
        user_informations = [user_db.id, user_db.name, user_db.role]
        user_db.delete_instance()
        return user_informations


class PeeweeContractRepository(ContractRepository):
    def __init__(self, db: Database):
        self.db = db

    def create_contract(self, contract: Contract) -> object:
        db_contract = ContractModel.create(
            sale_contact=contract.sale_contact,
            total_amount=contract.total_amount,
            amount_remaining_paid=contract.amount_remaining_paid,
            customer_informations=contract.customer_informations,
            status=contract.status,
        )

        contract = to_contract(db_contract)

        if contract.status == "signed":
            now = datetime.now()
            sentry_sdk.capture_message(
                f"The contract ID N° {contract.id__} has been signed at {now.strftime("%d/%m/%Y %H:%M:%S")}",
                level="info",
            )

        return contract

    def get_contract_by_id(self, contract_id: int) -> object:
        db_contract = (
            ContractModel.select().where((ContractModel.id == contract_id)).first()
        )
        db_sale_user = (
            UserModel.select().where(UserModel.id == db_contract.sale_contact).first()
        )
        sale_user = to_user(db_sale_user)

        return to_contract(db_contract, sale_user)

    def filter_contract(self, status: str, user_id: int, user_role: str) -> list:
        if status not in ["signed", "unsigned"]:
            return []
        status_filter = ContractModel.status != (
            "unsigned" if status == "signed" else "signed"
        )

        query = ContractModel.select().where(status_filter)

        if user_role != "management":
            query = query.where(ContractModel.sale_contact == user.id)

        return list(query)

    def filter_contract_by_remaining_paid(
        self, is_paid: bool, user_id: int, user_role: str
    ) -> list:
        paid_filter = (
            ContractModel.amount_remaining_paid == 0
            if is_paid
            else ContractModel.amount_remaining_paid != 0
        )

        query = ContractModel.select().where(paid_filter)

        if user_role != "management":
            query = query.where(ContractModel.sale_contact == user_id)

        contracts = []
        for db_contract in query:
            contract = to_contract(db_contract)
            db_sale_contact = (
                UserModel.select()
                .where(UserModel.id == db_contract.sale_contact_id)
                .first()
            )
            contract.sale_contact = to_user(db_sale_contact)
            contracts.append(contract)
        return contracts

    def delete_contract_by_id(self, contract_id) -> None:
        try:
            contract = ContractModel.get(ContractModel.id == contract_id)
            contract.delete_instance()
        except DoesNotExist:
            pass

    def update_contract(
        self,
        contract_id: int,
        sale_contact_to_change: int,
        total_amount_to_change: int,
        amount_remaining_paid_to_change: int,
        customer_informations_to_change: str,
        status_to_change: str,
    ) -> object:
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
            if status_to_change == "signed":
                now = datetime.now()
                sentry_sdk.capture_message(
                    f"Contract N°{contract_id} has been signed at {now.strftime('%d/%m/%Y %H:%M:%S')}",
                    level="info",
                )
        db_contract.save()

        contract = to_contract(db_contract)

        return contract


class PeeweeEventRepository(EventRepository):
    def __init__(self, db: Database):
        self.db = db

    def create_event(self, event: Event) -> object:
        db_contract = (
            ContractModel.select().where(ContractModel.id == event.contract).first()
        )
        if db_contract.status == "unsigned":
            return None
        else:
            db_event = EventModel.create(
                contract=event.contract,
                date_start=event.date_start,
                date_end=event.date_end,
                support_contact=event.support_contact,
                location=event.location,
                attendee=event.attendee,
                note=event.note,
            )
            return db_event

    def update_event(
        self,
        event_id: int,
        new_contract: int,
        new_date_start: datetime,
        new_date_end: datetime,
        new_support_contact: int,
        new_location: str,
        new_attendee: int,
        new_note: str,
    ):
        db_event = EventModel.get(EventModel.id == event_id)
        if new_contract is not None:
            db_event.contract = new_contract
        if new_date_start is not None:
            db_event.date_start = new_date_start
        if new_date_end is not None:
            db_event.date_end = new_date_end
        if new_support_contact is not None:
            db_event.support_contact = new_support_contact
        if new_location is not None:
            db_event.location = new_location
        if new_attendee is not None:
            db_event.note = new_attendee
        if new_note is not None:
            db_event.note = new_note
        db_event.save()

    def filter_my_events(self, user_id: int) -> list:
        query = EventModel.select().where(EventModel.support_contact == user_id)
        events = []
        for db_event in query:

            db_contract = (
                ContractModel.select()
                .where(ContractModel.id == db_event.contract_id)
                .first()
            )

            contract = to_contract(db_contract)

            db_user = (
                UserModel.select()
                .where(UserModel.id == db_event.support_contact_id)
                .first()
            )
            user_contact = to_user(db_user)

            event = to_event(db_event, contract, user_contact)
            events.append(event)

        return events

    def filter_event_with_or_without_contact(
        self, assigned_support_contact: bool
    ) -> list:
        if assigned_support_contact is False:
            query = EventModel.select().where(EventModel.support_contact_id == None)
        else:
            query = EventModel.select().where(EventModel.support_contact_id != None)

        events = []

        for db_event in query:
            db_contract = (
                ContractModel.select()
                .where(ContractModel.id == db_event.contract_id)
                .first()
            )
            db_sale_contact_contract = (
                UserModel.select()
                .where(UserModel.id == db_contract.sale_contact_id)
                .first()
            )
            sale_contact_contract = to_user(db_sale_contact_contract)
            contract = to_contract(db_contract, sale_contact_contract)

            db_support_contact = (
                UserModel.select()
                .where(UserModel.id == db_event.support_contact_id)
                .first()
            )
            support_contact = to_user(db_support_contact)
            event = to_event(db_event, contract, support_contact)
            events.append(event)

        return events

    def delete_event(self, event_id: int) -> bool:
        try:
            event = EventModel.select().where(EventModel.id == event_id).first()
            event.delete_instance()
            return True
        except DoesNotExist:
            pass

    def assign_support_contact(self, event_id: int, support_contact: int) -> object:
        db_event = EventModel.select().where(EventModel.id == event_id).first()
        db_event.support_contact = support_contact
        db_event.save()

        db_support_user_event = (
            UserModel.select().where(UserModel.id == support_contact).first()
        )
        user_support_contact_event = to_user(db_support_user_event)

        db_contract = (
            ContractModel.select().where(ContractModel.id == db_event.contract).first()
        )
        db_sale_contact_contract = (
            UserModel.select().where(UserModel.id == db_contract.sale_contact).first()
        )

        sale_contact_contract = to_user(db_sale_contact_contract)
        contract = to_contract(db_contract, sale_contact_contract)

        db_event = EventModel.select().where(EventModel.id == event_id).first()

        event = to_event(db_event, contract, user_support_contact_event)
        return event

    def get_event_by_id(self, event_id) -> object:
        db_event = EventModel.select().where(EventModel.id == event_id).first()

        db_contract = (
            ContractModel.select().where(ContractModel.id == db_event.contract).first()
        )
        db_sale_contact = (
            UserModel.select().where(UserModel.id == db_contract.sale_contact).first()
        )

        sale_contact = to_user(db_sale_contact)
        contract = to_contract(db_contract, sale_contact)

        db_support_contact = (
            UserModel.select().where(UserModel.id == db_event.support_contact).first()
        )
        support_contact = to_user(db_support_contact)
        print(f"DEBUG: {support_contact}")

        return to_event(db_event, contract, support_contact)


class PeeweeCustomerRepository(CustomerRepository):
    def __init__(self, db: Database):
        self.db = db

    def create_customer(self, customer: Customer) -> object:
        customer_db = CustomerModel.create(
            name=customer.name,
            email=customer.email,
            phone=customer.phone,
            company_name=customer.company_name,
            last_update=customer.last_update,
            sale_contact=customer.sale_contact,
            information=customer.information,
        )
        customer.id__ = customer_db.id
        return customer

    def update_customer(
        self,
        customer_id,
        name_to_change,
        email_to_change,
        phone_to_change,
        company_name_to_change,
        last_update,
        sales_contact_to_change,
        information_to_change,
    ):
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
        customer_db = (
            CustomerModel.select().where(CustomerModel.id == customer_id).first()
        )

        db_sale_contact = (
            UserModel.select()
            .where(UserModel.id == customer_db.sale_contact_id)
            .first()
        )
        sale_contact = to_user(db_sale_contact)
        print(f"DEBUG: {sale_contact}")
        return to_customer(customer_db, sale_contact)
