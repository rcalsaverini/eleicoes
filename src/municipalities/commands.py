import click
from src.base import MUNICIPALITY, STATE

from src.municipalities.csv_controllers import (
    get_municipalities_for_a_state_from_csv,
    get_municipalities_from_csv,
)

from .tse_controllers import list_municipalities


@click.group()
def municipalities():
    pass


@municipalities.command()
def list():
    dataframe = list_municipalities()
    print(dataframe.to_csv())


@municipalities.command()
@click.argument(
    "path",
    type=click.Path(exists=True, dir_okay=True, writable=True, resolve_path=True),
)
def create_file(path):
    dataframe = list_municipalities()
    dataframe.to_csv(f"{path}/municipalities.csv")


@municipalities.command()
@click.argument(
    "path",
    type=click.Path(exists=True, dir_okay=True, writable=True, resolve_path=True),
)
def test_file(path):
    for municipality in get_municipalities_for_a_state_from_csv(path, STATE.SP):
        print(municipality)
