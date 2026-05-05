import attrs
from datetime import datetime
from typing import Optional


@attrs.define
class User:
    name: str
    password: str
    role: str
    id__: Optional[int] = None


@attrs.define
class Contract:
    sale_contact: object
    total_amount: int
    amount_remaining_paid: int
    status: str
    created_date: datetime = attrs.field(factory=datetime.now)
    customer_informations: Optional[str] = None
    id__: Optional[int] = None


@attrs.define
class Event:
    contract: object
    date_start: datetime
    date_end: datetime
    location: str
    attendee: int
    note: str
    support_contact: Optional[object] = None
    id__: Optional[int] = None


@attrs.define
class Customer:
    name: str
    email: str
    phone: int
    company_name: str
    last_update: str
    information: str
    sale_contact: Optional[int] = None
    creation_date: datetime = attrs.field(factory=datetime.now)
    id__: Optional[int] = None
