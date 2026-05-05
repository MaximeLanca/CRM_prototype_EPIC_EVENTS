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
    def filter_contract(self, status: str) -> list:
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
    ) -> None:
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
        contract_to_change: int,
        date_start_to_change: datetime,
        date_end_to_change: datetime,
        support_contact_to_change: int,
        location_to_change: str,
        attendee_to_change: int,
        note_to_change: str,
    ):
        pass

    @abstractmethod
    def filter_event_by_contact(self, support_contact: int) -> list:
        pass

    @abstractmethod
    def delete_event(self, event_id: int) -> None:
        pass

    @abstractmethod
    def assign_support_contact(self, event_id: int, support_contact: int) -> object:
        pass

    @abstractmethod
    def get_event_by_id(self, event_id) -> object:
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
