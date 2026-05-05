from src.repository.peewee_operation_repository import PeeweeEventRepository
from datetime import datetime
from src.models.peewee_models import EventModel
from src.domain.domain_models import Event
from src.services.authorization_service import require_permission


class EventService:
    def __init__(self, PeeweeEventRepository):
        self.repository = PeeweeEventRepository

    @require_permission("create_event")
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
        event = Event(
            contract=contract,
            date_start=date_start,
            date_end=date_end,
            support_contact=support_contact,
            location=location,
            attendee=attendee,
            note=note,
        )
        return self.repository.create_event(event)

    @require_permission("update_event")
    def update_event(
        self,
        contract_to_change: int,
        date_start_to_change: datetime,
        date_end_to_change: datetime,
        support_contact_to_change: int,
        location_to_change: str,
        attendee_to_change: int,
        note_to_change: str,
    ):
        return self.repository.update_event(
            contract_to_change,
            date_start_to_change,
            date_end_to_change,
            support_contact_to_change,
            location_to_change,
            attendee_to_change,
            note_to_change,
        )

    @require_permission("filter_event")
    def filter_event_by_contact(self, support_contact: int) -> list:
        return self.repository.filter_event_by_contact(support_contact)

    @require_permission("delete_event")
    def delete_event(self, event_id: int):
        return self.repository.delete_event(event_id)

    @require_permission("assign_support_staff")
    def assign_support_contact(self, event_id: int, support_contact: int):
        return self.repository.assign_support_contact(event_id, support_contact)

    def get_event_by_id(self, event_id: int) -> object:
        return self.repository.get_event_by_id(event_id)
