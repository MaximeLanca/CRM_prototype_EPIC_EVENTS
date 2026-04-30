import pytest
from datetime import datetime
from src.services.event_service import EventService
from src.domain.domain_models import Event
from src.security.token_service import generate_token, save_token

class FakeSales:
    def __init__(self):
        self.id__ = 1
        self.role = "sales"

class FakeEventRepository:
    def __init__(self):
        self.events = []
        self._next_id = 1

    def create_event(self, event):
        event.id__ = self._next_id
        self._next_id += 1
        self.events.append(event)
        return event

    def get_event_by_id(self, event_id):
        for event in self.events:
            if event.id__ == event_id:
                return event
        return None

    def update_event(self, event_id, contract=None, date_start=None, date_end=None,
                     support_contact=None, location=None, attendee=None, note=None):
        event = self.get_event_by_id(event_id)
        if event:
            if location:
                event.location = location
            if note:
                event.note = note
            if attendee:
                event.attendee = attendee

    def delete_event(self, event_id):
        event = self.get_event_by_id(event_id)
        if event:
            self.events.remove(event)

    def filter_event(self, support_contact):
        return [e for e in self.events if e.support_contact == support_contact]

    def assign_support_contact(self, event_id, support_contact):
        event = self.get_event_by_id(event_id)
        if event:
            event.support_contact = support_contact
        return event

class TestEventService:

    def setup_method(self):
        from src.security.token_service import generate_token, save_token
        save_token(generate_token(FakeSales()))
        self.repository = FakeEventRepository()
        self.service = EventService(self.repository)

    def test_create_event_success(self):
        self.service.create_event(1, datetime.now(), datetime.now(), 1, "Paris", 10, "note")
        assert len(self.repository.events) == 1
        assert self.repository.events[0].location == "Paris"

    def test_create_event_has_id(self):
        self.service.create_event(1, datetime.now(), datetime.now(), 1, "Paris", 10, "note")
        assert self.repository.events[0].id__ is not None

    def test_delete_event(self):
        self.service.create_event(1, datetime.now(), datetime.now(), 1, "Paris", 10, "note")
        event = self.repository.events[0]
        self.service.delete_event(event.id__)
        assert len(self.repository.events) == 0

    def test_filter_event_by_support_contact(self):
        self.service.create_event(1, datetime.now(), datetime.now(), 1, "Paris", 10, "note")
        self.service.create_event(1, datetime.now(), datetime.now(), 2, "Lyon", 5, "note")
        result = self.repository.filter_event(1)
        assert len(result) == 1
        assert result[0].support_contact == 1

    def test_assign_support_contact(self):

        class FakeSales:
            id__ = 1
            role = "sales"

        class FakeManagement:
            id__ = 999
            role = "management"
            
        save_token(generate_token(FakeSales()))
        self.service.create_event(1, datetime.now(), datetime.now(), 1, "Paris", 10, "note")
        event = self.repository.events[0]

        save_token(generate_token(FakeManagement()))
        self.service.assign_support_contact(event.id__, 2)
        assert self.repository.events[0].support_contact == 2