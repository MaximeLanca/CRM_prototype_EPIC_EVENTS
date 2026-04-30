from src.cli import cli_command
from src.infrastructure.database import create_tables, drop_tables

cli_command.cli.add_command(cli_command.login)
cli_command.cli.add_command(cli_command.logout)
cli_command.cli.add_command(cli_command.check_token)

cli_command.cli.add_command(cli_command.create_user)
cli_command.cli.add_command(cli_command.update_user_information)
cli_command.cli.add_command(cli_command.delete_user_by_id)
cli_command.cli.add_command(cli_command.get_user_by_id)

cli_command.cli.add_command(cli_command.create_contract)
cli_command.cli.add_command(cli_command.update_contract)
cli_command.cli.add_command(cli_command.delete_contract_by_id)
cli_command.cli.add_command(cli_command.get_contract_by_id)
cli_command.cli.add_command(cli_command.filter_contract)

cli_command.cli.add_command(cli_command.create_event)
cli_command.cli.add_command(cli_command.update_event)
cli_command.cli.add_command(cli_command.filter_event)
cli_command.cli.add_command(cli_command.delete_event)
cli_command.cli.add_command(cli_command.assign_support_contact)

cli_command.cli.add_command(cli_command.create_customer)
cli_command.cli.add_command(cli_command.update_customer)
cli_command.cli.add_command(cli_command.delete_customer)

if __name__ == "__main__":
    #drop_tables()
    #create_tables() 
    cli_command.cli()