from src.repository.peewee_operation_repository import PeeweeEventRepository
from src.infrastructure.database import db
from src.services.event_service import EventService
from datetime import datetime


class EventController:
    def __init__(self):
        self.repository = PeeweeEventRepository(db)
        self.service = EventService(self.repository)

    def create_event(
        self,
        contract: int,
        date_start: datetime,
        date_end: datetime,
        support_contact: int,
        location: str,
        attendee: int,
        note: str,
    ) -> object:
        return self.service.create_event(
            contract, date_start, date_end, support_contact, location, attendee, note
        )

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
        return self.service.update_event(
            event_id,
            new_contract,
            new_date_start,
            new_date_end,
            new_support_contact,
            new_location,
            new_attendee,
            new_note,
        )

    def filter_my_events(self):
        return self.service.filter_my_events()

    def delete_event(self, event_id: int) -> bool:
        return self.service.delete_event(event_id)

    def assign_support_contact(self, event_id: int, support_contact: int):
        return self.service.assign_support_contact(event_id, support_contact)

    def get_event_by_id(self, event_id:int) -> object:
        return self.service.get_event_by_id(event_id)
    
    def filter_event_with_or_without_contact(self,assigned_support_contact:bool) -> list:
        return self.service.filter_event_with_or_without_contact(assigned_support_contact)
