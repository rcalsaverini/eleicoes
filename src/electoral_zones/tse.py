from dataclasses import dataclass
from typing import Iterable
from ..base import ELECTION_TYPE, STATE, MUNICIPALITY, ELECTORAL_ZONE
from src.request_utils import TSE_Request


BASE_URL: str = "https://resultados.tse.jus.br/oficial/ele{year}/{election_code}/config/mun-e{election_code:06d}-cm.json"

STATE_INFO_FIELD = "abr"
MUNICIPALITY_INFO_FIELD = "mu"
ELECTORAL_ZONE_FIELD = "z"


@dataclass()
class ElectoralZonesRequest(TSE_Request):
    year: int
    election_type: ELECTION_TYPE

    def build_url(self) -> str:
        return BASE_URL.format(year=self.year, election_code=self.election_type.value)


def iter_parsed_electoral_zones(raw_api_data) -> Iterable[ELECTORAL_ZONE]:
    yield from (
        ELECTORAL_ZONE(
            MUNICIPALITY(
                STATE.parse(state_info["cd"]),
                municipality_info["nm"],
                municipality_info["cd"],
            ),
            electoral_zone,
        )
        for state_info in raw_api_data[STATE_INFO_FIELD]
        for municipality_info in state_info[MUNICIPALITY_INFO_FIELD]
        for electoral_zone in municipality_info[ELECTORAL_ZONE_FIELD]
    )


def iter_electoral_zones(
    year: int, election_type: ELECTION_TYPE
) -> Iterable[ELECTORAL_ZONE]:
    raw_data = ElectoralZonesRequest(year, election_type).fetch()
    yield from iter_parsed_electoral_zones(raw_data)
