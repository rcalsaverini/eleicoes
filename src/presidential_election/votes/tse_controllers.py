from typing import Dict
from src.base import ELECTORAL_ZONE, MUNICIPALITY, VOTE_COUNT
from .tse import iter_presidential_votes
import pandas as pd  # type: ignore


def get_all_electoral_zones_for_municipality(municipality: MUNICIPALITY):
    return pd.DataFrame(
        get_row(vote_count)
        for vote_count in iter_presidential_votes(2022, municipality)
        if isinstance(vote_count.aggregate, ELECTORAL_ZONE)
    )


def get_row(vote_count: VOTE_COUNT):
    row = {
        "zona_eleitoral": vote_count.aggregate.code,
        "brancos": vote_count.blank,
        "nulos": vote_count.anulled,
        "abstencao": vote_count.abstention,
    }
    for candidate, candidate_votes in vote_count.candidates.items():
        row[f"votos_{candidate.party.value}"] = candidate_votes
    return row