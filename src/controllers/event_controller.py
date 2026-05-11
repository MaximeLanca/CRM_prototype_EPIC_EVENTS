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
        contract_to_change: int,
        date_start_to_change: datetime,
        date_end_to_change: datetime,
        support_contact_to_change: int,
        location_to_change: str,
        attendee_to_change: int,
        note_to_change: str,
    ):
        return self.service.update_event(
            event_id,
            contract_to_change,
            date_start_to_change,
            date_end_to_change,
            support_contact_to_change,
            location_to_change,
            attendee_to_change,
            note_to_change,
        )

    def filter_my_events(self):
        return self.service.filter_my_events()

    def delete_event(self, event_id: int):
        return self.service.delete_event(event_id)

    def assign_support_contact(self, event_id: int, support_contact: int):
        return self.service.assign_support_contact(event_id, support_contact)

    def get_event_by_id(self, event_id:int) -> object:
        return self.service.get_event_by_id(event_id)
    
    def filter_event_with_or_without_contact(self,assigned_support_contact:bool) -> list:
        return self.service.filter_event_with_or_without_contact(assigned_support_contact)
