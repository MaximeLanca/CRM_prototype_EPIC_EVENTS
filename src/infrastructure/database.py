import os
from dotenv import load_dotenv
from peewee import PostgresqlDatabase
from peewee_migrate import Router


load_dotenv()

db = PostgresqlDatabase (
    os.getenv('DATABASE'), 
    user = os.getenv('USER'), 
    password = os.getenv('PASSWORD'), 
    host = os.getenv('HOST'), 
    port = int(os.getenv('PORT',5432)),
    options='-c search_path=public'
)

def migrates_database() :
    router = Router(db)
    router.run()

def create_tables():
    from src.models.peewee_models import UserModel, ContractModel, EventModel, CustomerModel
    db.create_tables([UserModel, ContractModel, EventModel, CustomerModel])

def drop_tables():
    from src.models.peewee_models import UserModel, ContractModel, EventModel, CustomerModel
    db.drop_tables([UserModel, ContractModel, EventModel, CustomerModel], cascade=True)