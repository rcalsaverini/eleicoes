from pathlib import Path
from typing import Iterable
import pandas as pd  # type:ignore


from src.base import MUNICIPALITY, STATE


def get_municipalities_from_csv(csv_data: Path) -> Iterable[MUNICIPALITY]:
    dataframe = pd.read_csv(csv_data)
    for row in dataframe.itertuples():
        yield MUNICIPALITY(STATE.parse(row.estado), row.municipio, row.codigo_municipio)


def get_municipalities_for_a_state_from_csv(
    csv_data: Path, state: STATE
) -> Iterable[MUNICIPALITY]:
    dataframe = pd.read_csv(csv_data)
    for row in dataframe.loc[dataframe.estado == state.name].itertuples():
        yield MUNICIPALITY(STATE.parse(row.estado), row.municipio, row.codigo_municipio)
