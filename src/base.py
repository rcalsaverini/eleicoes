from enum import Enum, auto
from dataclasses import dataclass
from typing import Dict


class ELECTION_TYPE(Enum):
    STATE = 546
    FEDERAL = 544


class POLITICAL_POSITION(Enum):
    PRESIDENT = auto()
    GOVERNOR = auto()
    SENATOR = auto()
    FEDERAL_REP = auto()
    STATE_REP = auto()


class STATE(Enum):
    AC = auto()
    AL = auto()
    AP = auto()
    AM = auto()
    BA = auto()
    CE = auto()
    DF = auto()
    ES = auto()
    GO = auto()
    MA = auto()
    MT = auto()
    MS = auto()
    MG = auto()
    PA = auto()
    PB = auto()
    PR = auto()
    PE = auto()
    PI = auto()
    RJ = auto()
    RN = auto()
    RS = auto()
    RO = auto()
    RR = auto()
    SC = auto()
    SP = auto()
    SE = auto()
    TO = auto()
    ZZ = auto()

    @classmethod
    def parse(cls, state_code: str):
        return cls.__members__[state_code]

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name


@dataclass(eq=True, frozen=True)
class MUNICIPALITY:
    state: STATE
    name: str
    code: str


@dataclass(eq=True, frozen=True)
class ELECTORAL_ZONE:
    municipality: MUNICIPALITY
    code: str


class POLITICAL_PARTY(Enum):
    MDB = 15
    PT = 13
    PSDB = 45
    PP = 11
    PDT = 12
    UNIÃO = 44
    PTB = 14
    PL = 22
    PSB = 40
    REPUBLICANOS = 10
    CIDADANIA = 23
    PSC = 20
    PODE = 19
    PCdoB = 65
    PSD = 55
    PV = 43
    PATRIOTA = 51
    SOLIEDARIEDADE = 77
    PSOL = 50
    AVANTE = 70
    PMN = 33
    AGIR = 36
    DC = 27
    PRTB = 28
    PROS = 90
    PMB = 35
    REDE = 18
    NOVO = 30
    PSTU = 16
    PCB = 21
    PCO = 29
    UP = 80


@dataclass(eq=True, frozen=True)
class CANDIDATE:
    party: POLITICAL_PARTY
    name: str | None
    position: POLITICAL_POSITION


@dataclass(eq=True, frozen=True)
class VOTE_COUNT:
    aggregate: MUNICIPALITY | ELECTORAL_ZONE
    valid: int
    blank: int
    anulled: int
    abstention: int
    candidates: Dict[CANDIDATE, int]
