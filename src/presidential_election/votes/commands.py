import click
import tqdm
import pandas as pd

from src.base import MUNICIPALITY, STATE
from src.municipalities.csv_controllers import (
    get_municipalities_for_a_state_from_csv,
    get_municipalities_from_csv,
)
from src.presidential_election.votes.csv_controllers import (
    get_all_presidential_votes,
    get_votes_dataframe,
)
from .tse_controllers import get_all_electoral_zones_for_municipality


@click.group()
def presidential_votes():
    pass


@presidential_votes.command()
@click.argument(
    "municipality_path",
    type=click.Path(
        exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True
    ),
)
@click.argument(
    "output_path",
    type=click.Path(
        exists=True, file_okay=False, dir_okay=True, writable=True, resolve_path=True
    ),
)
def to_file(municipality_path, output_path):
    votes = None
    for state in tqdm.tqdm(STATE):
        municipalities = get_municipalities_for_a_state_from_csv(
            municipality_path, state
        )
        if votes is None:
            votes = get_votes_dataframe(municipalities)
        else:
            votes = pd.concat([votes, get_votes_dataframe(municipalities)])
    votes.to_csv(f"{output_path}/presidential.csv", index=None)
    
