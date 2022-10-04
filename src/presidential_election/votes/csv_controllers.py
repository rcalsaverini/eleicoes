from pathlib import Path
from typing import Iterable
import pandas as pd  # type:ignore


from src.base import MUNICIPALITY, STATE, ELECTORAL_ZONE, VOTE_COUNT
from src.presidential_election.votes.tse import iter_presidential_votes


def get_all_presidential_votes(
    municipalities: Iterable[MUNICIPALITY],
) -> Iterable[VOTE_COUNT]:
    for municipality in municipalities:
        for vote_count in iter_presidential_votes(2022, municipality):
            yield vote_count


def get_votes_dataframe(municipalities: Iterable[MUNICIPALITY]) -> pd.DataFrame:
    return pd.DataFrame(
        (
            get_row(vote_count)
            for vote_count in get_all_presidential_votes(municipalities)
            if isinstance(vote_count.aggregate, ELECTORAL_ZONE)
        )
    )


def get_row(vote_count: VOTE_COUNT):
    if isinstance(vote_count.aggregate, ELECTORAL_ZONE):
        row = {
            "zona_eleitoral": vote_count.aggregate.code,
            "municipio": vote_count.aggregate.municipality.name,
            "estado": vote_count.aggregate.municipality.state.name,
            "brancos": vote_count.blank,
            "nulos": vote_count.anulled,
            "abstencao": vote_count.abstention,
        }
        for candidate, candidate_votes in vote_count.candidates.items():
            row[f"votos_{candidate.party.value}"] = candidate_votes
        return row