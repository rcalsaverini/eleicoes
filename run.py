import click
from src.electoral_zones.commands import electoral_zones
from src.municipalities.commands import municipalities
from src.presidential_election.votes.commands import presidential_votes


@click.group()
def main():
    pass


main.add_command(electoral_zones, "electoral-zones")
main.add_command(municipalities, "municipalities")
main.add_command(presidential_votes, "presidential_votes")

main()
