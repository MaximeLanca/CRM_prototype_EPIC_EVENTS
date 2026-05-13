import click
from src.controllers.user_controller import UserController
from src.controllers.session_controller import SessionController
from src.controllers.contract_controller import ContractController
from src.controllers.event_controller import EventController
from src.controllers.customer_controller import CustomerController
from src.infrastructure.database import db
from src.services.session_service import SessionService

user_controller = UserController()
session_controller = SessionController()
contract_controller = ContractController()
event_controller = EventController()
customer_controller = CustomerController()


@click.group()
def cli():
    db.connect(reuse_if_open=True)


@click.command()
@click.option("--user_id", required=True, type=int)
@click.option("--password", required=True)
def login(user_id, password):
    result = user_controller.login(user_id, password)
    if result is None:
        pass
    else:
        _, user = result
        click.echo(f"Welcome {user.name}.")


@click.command()
def logout():
    user_controller.logout()
    click.echo("You are logged out.")


@click.command()
@click.option("--name", type=str, required=True)
@click.option("--password", type=str, required=True)
@click.option(
    "--role",
    type=click.Choice(["management", "sales", "support"], case_sensitive=False),
    required=True,
)
def create_user(name, password, role):
    user = user_controller.create_user(name, password, role)
    click.echo("The user:")
    click.echo(f"User ID: {user.id__}")
    click.echo(f"Name: {user.name}")
    click.echo(f"Role: {user.role}")
    click.echo("has been created successfully")


@click.command()
def check_token():
    payload, error = session_controller.get_payload()
    if error:
        click.echo(error)
        return
    click.echo(f"User ID: {payload['sub']}")
    click.echo(f"Department: {payload['role']}")


@click.command()
@click.option("--user_id", type=int, required=True)
def get_user_by_id(user_id):
    user = user_controller.get_user_by_id(user_id)
    click.echo(
        f"ID number: {user.id__}\n"
        f"Name: {user.name}\n"
        f"Role: {user.role}"
    )


@click.command()
@click.option("--user_id", type=int, required=True)
def delete_user_by_id(user_id):
    user = user_controller.delete_user_by_id(user_id)
    click.echo(
        "Employee: "
        f"ID number: {user[0]}\n"
        f"Name: {user[1]}\n"
        f"Role: {user[2]}\n"
        "... is deleted."
    )


@click.command()
@click.option("--user_id", type=int, required=True)
@click.option("--new_name", type=str, required=False)
@click.option("--new_role", type=str, required=False)
def update_user_information(user_id, new_name, new_role):
    user_controller.update_user_information(user_id, new_name, new_role)
    print("User informations udpated.")


@cli.command()
@click.option("--sale_contact", type=int, required=True)
@click.option("--total_amount", type=int, required=True)
@click.option("--amount_remaining_paid", type=int, required=False)
@click.option("--customer_informations", type=str, required=False)
@click.option(
    "--status",
    type=click.Choice(["signed", "unsigned"], case_sensitive=False),
    required=True,
)
def create_contract(
    sale_contact, total_amount, amount_remaining_paid, customer_informations, status
):
    contract = contract_controller.create_contract(
        sale_contact, total_amount, amount_remaining_paid, customer_informations, status
    )
    click.echo(f"The contract N°{contract.id__} is created.")


@cli.command()
@click.option("--contract_id", type=str, required=True)
@click.option("--new_sale_contact", type=int, required=False)
@click.option("--new_total_amount", type=int, required=False)
@click.option("--new_amount_remaining_paid", type=int, required=False)
@click.option("--new_customer_informations", type=str, required=False)
@click.option(
    "--new_status",
    type=click.Choice(["signed", "unsigned"], case_sensitive=False),
    required=False,
)
def update_contract(
    contract_id,
    new_sale_contact,
    new_total_amount,
    new_amount_remaining_paid,
    new_customer_informations,
    new_status,
):
    contract = contract_controller.update_contract(
        contract_id,
        new_sale_contact,
        new_total_amount,
        new_amount_remaining_paid,
        new_customer_informations,
        new_status,
    )
    if contract is None:
        click.echo("You aren't autorized to modify this contract. You aren't the owner")
    else:
        click.echo(f"The contract ID N°{contract_id} is updated.")


@cli.command()
@click.option("--contract_id", type=str, required=True)
def delete_contract_by_id(contract_id):
    contract_controller.delete_contract_by_id(contract_id)
    click.echo(f"The contract N°{contract_id} is deleted.")


@cli.command()
@click.option("--contract_id", type=int, required=True)
def get_contract_by_id(contract_id):
    contract = contract_controller.get_contract_by_id(contract_id)
    click.echo(
        f"Contract N°:{contract.id__}\n"
        f"Sale contact: {contract.sale_contact.name} & ID number: {contract.sale_contact.id__}\n"
        f"Total amount: {contract.total_amount}\n"
        f"Amount remaining paid : {contract.amount_remaining_paid}\n"
        f"Status: {contract.status}"
    )


@cli.command()
@click.option("--status", type=str, required=True)
def filter_contract(status):
    contract_list = contract_controller.filter_contract(status)
    for contract in contract_list:
        click.echo(f"Contracts N°: {contract.id}")

@cli.command()
@click.option("--is_paid", type=bool, required=True)
def filter_contract_by_remaining_paid(is_paid):
    contracts = contract_controller.filter_contract_by_remaining_paid(is_paid)
    for contract in contracts:
        click.echo(
        f"Contract N°:{contract.id__}\n"
        f"Sale contact: {contract.sale_contact.name} & ID number: {contract.sale_contact.id__}\n"
        f"Total amount: {contract.total_amount}\n"
        f"Amount remaining paid : {contract.amount_remaining_paid}\n"
        f"Status: {contract.status}"
        "\n"
    )

@cli.command()
@click.option("--contract", type=int, required=True)
@click.option("--date_start", type=click.DateTime(formats=["%Y-%m-%d"]), required=True)
@click.option("--date_end", type=click.DateTime(formats=["%Y-%m-%d"]), required=True)
@click.option("--support_contact", type=int, required=False)
@click.option("--location", type=str, required=False)
@click.option("--attendee", type=int, required=False)
@click.option("--note", type=str, required=False)
def create_event(
    contract, date_start, date_end, support_contact, location, attendee, note
):
    db_event = event_controller.create_event(
        contract, date_start, date_end, support_contact, location, attendee, note
    )
    if db_event:
        click.echo(f"The event N° {db_event} id created.")
    else: 
        click.echo(f"The event didn't has been create because the contract ID N°{contract} didn't has been signed. ")

@click.command()
@click.option("--event_id", type=str, required=True)
@click.option("--new_contract", type=int, required=False)
@click.option(
    "--new_date_start", type=click.DateTime(formats=["%Y-%m-%d"]), required=False
)
@click.option(
    "--new_date_end", type=click.DateTime(formats=["%Y-%m-%d"]), required=False
)
@click.option("--new_support_contact", type=int, required=False)
@click.option("--new_location", type=str, required=False)
@click.option("--new_attendee", type=int, required=False)
@click.option("--new_note", type=str, required=False)
def update_event(
    event_id,
    new_contract,
    new_date_start,
    new_date_end,
    new_support_contact,
    new_location,
    new_attendee,
    new_note,
):
    event_controller.update_event(
        event_id,
        new_contract,
        new_date_start,
        new_date_end,
        new_support_contact,
        new_location,
        new_attendee,
        new_note,
    )
    click.echo(f"The event N°{event_id} is updated.")


@click.command()
def filter_my_events():
    events_list = event_controller.filter_my_events()
    if events_list == []:
        click.echo("You don't have any associated events.")
    for event in events_list:
        click.echo(
            f"Event N°{event.id__},\n"
            f"Contract N°{event.contract.id__} with status : {event.contract.status},\n"
            f"Date Start: {event.date_start},\n"
            f"Date End: {event.date_end},\n"
            f"Support Contact: ID N°{event.support_contact.id__},\n"
            f"Location: {event.location},\n"
            f"Attendee: {event.attendee},\n"
            f"Note: {event.note}"
            "\n"
        )

@click.command()
@click.option("--event_id", type=int, required=True)
def delete_event(event_id):
    result = event_controller.delete_event(event_id)
    if result is None:
        return
    click.echo(f"Event N°{event_id} is deleted.")


@click.command()
@click.option("--event_id", type=int, required=True)
@click.option("--support_contact", type=int, required=True)
def assign_support_contact(event_id, support_contact):
    event = event_controller.assign_support_contact(event_id, support_contact)
    click.echo(
        f"User ID n°{support_contact} / Name: {event.support_contact.name} has been assigned to the event N°{event.id__}."
    )


@cli.command()
@click.option("--event_id", type=int, required=True)
def get_event_by_id(event_id):
    event = event_controller.get_event_by_id(event_id)
    click.echo(
        f"Event N°{event.id__},\n"
        f"Contract N°{event.contract.id__} with status : {event.contract.status},\n"
        f"Date Start: {event.date_start},\n"
        f"Date End: {event.date_end},\n"
        f"Support Contact: ID N°{event.support_contact.id__} / Name : {event.support_contact.name},\n"
        f"Location: {event.location},\n"
        f"Attendee: {event.attendee},\n"
        f"Note: {event.note}"
    )

@cli.command()
@click.option("--assigned_support_contact",type=bool, required=True)
def filter_event_by_assigned_contact(assigned_support_contact):
    events_list = event_controller.filter_event_with_or_without_contact(assigned_support_contact)
    for event in events_list:
        click.echo(
        f"Event N°{event.id__},\n"
        f"Contract N°{event.contract.id__} with status : {event.contract.status},\n"
        f"Date Start: {event.date_start},\n"
        f"Date End: {event.date_end},\n"
        f"Support Contact: ID N°{event.support_contact.id__} / Name : {event.support_contact.name},\n"
        f"Location: {event.location},\n"
        f"Attendee: {event.attendee},\n"
        f"Note: {event.note}"
        "\n"
        )


@click.command()
@click.option("--name", type=str, required=True)
@click.option("--email", type=str, required=True)
@click.option("--phone", type=str, required=True)
@click.option("--company_name", type=str, required=True)
@click.option("--last_update", type=str, required=False)
@click.option("--information", type=str, required=False)
def create_customer(
    name, email, phone, company_name, last_update, information
):
    customer = customer_controller.create_customer(
        name, email, phone, company_name, last_update, information
    )
    click.echo()
    click.echo(
        f"The customer ID N°{customer.id__} has been created.\n"
        f"Name {customer.name},\n"
        f"Phone: {customer.phone},\n"
        f"email: {customer.email}\n"
    )


@click.command()
@click.option("--customer_id", type=str, required=True)
@click.option("--new_name", type=str, required=False)
@click.option("--new_email", type=str, required=False)
@click.option("--new_phone", type=str, required=False)
@click.option("--new_company_name", type=str, required=False)
@click.option("--last_update", type=str, required=False)
@click.option("--new_sales_contact", type=int, required=False)
@click.option("--new_information", type=str, required=False)
def update_customer(
    customer_id,
    new_name,
    new_email,
    new_phone,
    new_company_name,
    last_update,
    new_sales_contact,
    new_information,
):
    customer_controller.update_customer(
        customer_id,
        new_name,
        new_email,
        new_phone,
        new_company_name,
        last_update,
        new_sales_contact,
        new_information,
    )
    click.echo("The customer has been updated.")


@click.command()
@click.option("--customer_id", type=int, required=True)
def delete_customer(customer_id):
    customer_controller.delete_customer(customer_id)
    click.echo("The customer has been deleted.")


@click.command()
@click.option("--customer_id", type=int, required=True)
def get_customer_by_id(customer_id):
    customer = customer_controller.get_customer_by_id(customer_id)
    click.echo(
        f"Customer ID n°{customer.id__},\n"
        f"Name : {customer.name},\n"
        f"Email : {customer.email},\n"
        f"Phone : {customer.phone}\n,"
        f"Company name : {customer.company_name},\n"
        f"Last update : {customer.last_update},\n"
        f"Sale contact : {customer.sales_contact.id__}"
        f"Information : {customer.information}"
    )
