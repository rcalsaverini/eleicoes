from ..base import ELECTION_TYPE
from .tse import iter_electoral_zones
import pandas as pd  # type: ignore


def list_electoral_zones() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "codigo_zona_eleitoral": int(zone.code),
            "zona_eleitoral": zone.code,
            "estado": zone.municipality.state.name,
            "municipio": zone.municipality.name,
            "codigo_municipio": zone.municipality.code,
        }
        for zone in iter_electoral_zones(2022, ELECTION_TYPE.FEDERAL)
    ).set_index("zona_eleitoral")


def list_municipalities():
    return (
        pd.DataFrame(
            {
                "estado": zone.municipality.state.name,
                "municipio": zone.municipality.name,
                "codigo_municipio": zone.municipality.code,
            }
            for zone in iter_electoral_zones(2022, ELECTION_TYPE.FEDERAL)
        )
        .drop_duplicates()
        .reset_index(drop=True)
        .set_index("codigo_municipio")
    )
