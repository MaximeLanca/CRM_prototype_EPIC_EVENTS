import peewee
import uuid
from src.infrastructure.database import db
import datetime


class BaseModel(peewee.Model):
    class Meta:
        database = db


class UserModel(BaseModel):
    class Meta:
        table_name = "users"

    name = peewee.CharField()
    password = peewee.CharField()
    role = peewee.CharField(
        constraints=[peewee.Check("role IN ('sales','support','management')")]
    )


class ContractModel(BaseModel):
    class Meta:
        table_name = "contract"

    total_amount = peewee.IntegerField()
    amount_remaining_paid = peewee.IntegerField()
    created_date = peewee.DateTimeField(default=datetime.datetime.now)
    status = peewee.CharField()
    customer_informations = peewee.CharField()
    sale_contact = peewee.ForeignKeyField(UserModel, backref="contracts", null=True)


class CustomerModel(BaseModel):
    class Meta:
        table_name = "customer"

    name = peewee.CharField()
    email = peewee.CharField()
    phone = peewee.CharField(max_length=20)
    company_name = peewee.CharField()
    creation_date = peewee.DateTimeField(default=datetime.datetime.now)
    last_update = peewee.DateTimeField(null=True)
    sale_contact = peewee.ForeignKeyField(UserModel, backref="customers", null=True)
    information = peewee.CharField(null=True)


# https://mermaid.js.org/


class EventModel(BaseModel):
    class Meta:
        table_name = "event"

    contract = peewee.ForeignKeyField(
        ContractModel, backref="event", on_delete="CASCADE"
    )
    date_start = peewee.DateField()
    date_end = peewee.DateField()
    support_contact = peewee.ForeignKeyField(UserModel, backref="customers", null=True)
    location = peewee.CharField(null=True)
    attendee = peewee.IntegerField(null=True)
    note = peewee.TextField(null=True)
