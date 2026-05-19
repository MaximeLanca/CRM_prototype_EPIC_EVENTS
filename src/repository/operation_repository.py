from abc import ABC, abstractmethod
from src.domain.domain_models import User, Contract, Event, Customer
from datetime import datetime


class ContractRepository(ABC):
    @abstractmethod
    def create_contract(self, contract: Contract) -> object:
        pass

    @abstractmethod
    def get_contract_by_id(self, contract_id: int) -> object:
        pass

    @abstractmethod
    def filter_contract(self, status: str, user_id:int, user_role:str) -> list:
        pass

    @abstractmethod
    def delete_contract_by_id(self, contract_id: int) -> None:
        pass

    @abstractmethod
    def update_contract(
        self,
        contract_id: int,
        sale_contact_to_change: int,
        total_amount_to_change: int,
        amount_remaining_paid_to_change: int,
        customer_informations_to_change: str,
        status_to_change: str,
    ) -> object:
        pass
    
    @abstractmethod
    def filter_contract_by_remaining_paid(self, is_paid:bool, user_id, user_role) -> list:
        pass

class UserRepository(ABC):
    @abstractmethod
    def create_user(self, user) -> object:
        pass

    @abstractmethod
    def update_user_information(
        self, user_id: int, name_to_change, role_to_change
    ) -> None:
        pass

    @abstractmethod
    def delete_user_by_id(self, user_id: int) -> list:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> object:
        pass


class EventRepository(ABC):
    @abstractmethod
    def create_event(self, event: Event) -> object:
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def filter_my_events(self, user_id) -> list:
        pass

    @abstractmethod
    def delete_event(self, event_id: int) -> bool:
        pass

    @abstractmethod
    def assign_support_contact(self, event_id: int, support_contact: int) -> object:
        pass

    @abstractmethod
    def get_event_by_id(self, event_id:int) -> object:
        pass

    @abstractmethod
    def filter_event_with_or_without_contact(self, assigned_support_contact:bool) -> list:
        pass


class CustomerRepository(ABC):
    @abstractmethod
    def create_customer(self, customer: Customer) -> object:
        pass

    @abstractmethod
    def update_customer(
        self,
        customer_id: int,
        name_to_change: str,
        email_to_change: str,
        phone_to_change: int,
        company_name_to_change: str,
        last_update,
        sales_contact_to_change: int,
        information_to_change: str,
    ):
        pass

    @abstractmethod
    def delete_customer(self, customer_id: int):
        pass

    @abstractmethod
    def get_customer_by_id(self, customer_id: int) -> object:
        pass
