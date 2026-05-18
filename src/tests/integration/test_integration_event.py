from src.models.peewee_models import EventModel, UserModel, ContractModel
from src.domain.domain_models import Event
from src.infrastructure.database import db
from src.repository.peewee_operation_repository import PeeweeEventRepository
from datetime import datetime


class TestEventRepositoryIntegration:

    def setup_method(self):
        self.event_repository = PeeweeEventRepository(db)

    def test_create_event(self):
        user = UserModel.create(name="Support", password="1234", role="support")
        contract = ContractModel.create(
            sale_contact=user.id,
            total_amount=1000,
            amount_remaining_paid=500,
            customer_informations="client",
            status="signed",
        )
        event = Event(
            contract=contract.id,
            date_start=datetime.now(),
            date_end=datetime.now(),
            support_contact=user.id,
            location="Paris",
            attendee=10,
            note="test",
        )
        result = self.event_repository.create_event(event)
        assert result.id is not None

    def test_delete_event(self):
        user = UserModel.create(name="Support", password="1234", role="support")
        contract = ContractModel.create(
            sale_contact=user.id,
            total_amount=1000,
            amount_remaining_paid=500,
            customer_informations="client",
            status="unsigned",
        )
        event = EventModel.create(
            contract=contract.id,
            date_start=datetime.now(),
            date_end=datetime.now(),
            support_contact=user.id,
            location="Paris",
            attendee=10,
            note="test",
        )
        self.event_repository.delete_event(event.id)
        deleted = EventModel.get_or_none(EventModel.id == event.id)
        assert deleted is None
