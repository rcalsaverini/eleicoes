from pathlib import Path
from typing import Iterable
import pandas as pd  # type:ignore


from src.base import MUNICIPALITY, STATE, ELECTORAL_ZONE


def get_electoral_zones_from_csv(csv_data: Path) -> Iterable[ELECTORAL_ZONE]:
    dataframe = pd.read_csv(csv_data)
    for row in dataframe.itertuples():

        yield ELECTORAL_ZONE(
            MUNICIPALITY(
                STATE.parse(row.estado),
                row.municipio,
                row.codigo_municipio
            ), 
            row.codigo_zona_eleitoral
        )
