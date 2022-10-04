import click

from .csv_controllers import get_electoral_zones_from_csv

from .tse_controllers import list_electoral_zones


@click.group()
def electoral_zones():
    pass


@electoral_zones.command()
def list():
    dataframe = list_electoral_zones()
    print(dataframe.to_csv())


@electoral_zones.command()
@click.argument(
    "path",
    type=click.Path(exists=True, dir_okay=True, writable=True, resolve_path=True),
)
def create_file(path):
    dataframe = list_electoral_zones()
    dataframe.to_csv(f"{path}/electoral_zones.csv")


@electoral_zones.command()
@click.argument(
    "path",
    type=click.Path(exists=True, dir_okay=True, writable=True, resolve_path=True),
)
def test_file(path):
    for municipality in get_electoral_zones_from_csv(path):
        print(municipality)
