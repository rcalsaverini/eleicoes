from dataclasses import dataclass
from pprint import pprint
import traceback
from src.base import (
    CANDIDATE,
    ELECTION_TYPE,
    ELECTORAL_ZONE,
    MUNICIPALITY,
    POLITICAL_PARTY,
    POLITICAL_POSITION,
    VOTE_COUNT,
)
from src.request_utils import TSE_Request, TSEError
from typing import Dict, Iterable, List, TypedDict

BASE_URL: str = "https://resultados.tse.jus.br/oficial/ele{year}/{election_code}/dados/{state_code}/{state_code}{municipality_code:05d}-c0001-e{election_code:06d}-v.json"


@dataclass()
class PresidentialVotesRequest(TSE_Request):
    year: int
    municipality: MUNICIPALITY

    def build_url(self) -> str:
        return BASE_URL.format(
            year=self.year,
            election_code=ELECTION_TYPE.FEDERAL.value,
            state_code=self.municipality.state.name.lower(),
            municipality_code=self.municipality.code,
        )


class CandidateResult(TypedDict):
    n: str  # candidate number
    vap: str  # number of votes


class VoteResult(TypedDict):
    vv: str  # valid votes
    vb: str  # blank votes
    vn: str  # anulled votes
    tv: str  # total votes
    a: str  # abstentions votes
    c: str  # attendance
    e: str  # number of electors
    tpabr: str  # type of aggregate
    cdabr: str  # aggregate code
    cand: List[CandidateResult]


def iter_parsed_votes(raw_api_data, municipality: MUNICIPALITY) -> Iterable[VOTE_COUNT]:
    yield from (
        parse_vote_count(result, municipality) for result in raw_api_data["abr"]
    )


def validate_counts(
    candidates: Dict[CANDIDATE, int],
    valid_votes: int,
    blank_votes: int,
    anulled_votes: int,
    total_votes: int,
    abstension: int,
    attendance: int,
    total_ellectors: int,
) -> None:

    if valid_votes + blank_votes + anulled_votes != total_votes:
        msg = (
            f"Valid votes, blank votes and anulled votes should sum to total votes. Found:"
            f"valid_votes={valid_votes}, blank_votes={blank_votes}, anulled_votes={anulled_votes} "
            f"(sum={valid_votes + blank_votes + anulled_votes}), "
            f"while total_votes={total_votes}"
        )

        raise TSEError(msg)
    if total_votes + abstension != total_ellectors:
        msg = (
            f"Total votes and abstensions should sum to total ellectors. Found:"
            f"total_votes={total_votes}, abstension={abstension} "
            f"(sum={total_votes + abstension}), "
            f"while total_ellectors={total_ellectors}"
        )
        raise TSEError(msg)
    if attendance + abstension != total_ellectors:
        msg = (
            f"Attendance and abstensions should sum to total ellectors. Found:"
            f"total_votes={attendance}, abstension={abstension} "
            f"(sum={attendance + abstension}), "
            f"while total_ellectors={total_ellectors}"
        )
        raise TSEError(msg)

    if sum(candidates.values()) != valid_votes:
        msg = (
            f"The sum of the votes of all candidates must equal the valid votes. Found:"
            f"{candidates} (sum={sum(candidates.values())}), "
            f"while valid_votes={valid_votes}"
        )
        raise TSEError(msg)


def parse_candidates(candidates: List[CandidateResult]) -> Dict[CANDIDATE, int]:
    return {
        CANDIDATE(
            POLITICAL_PARTY(int(cr["n"])), None, POLITICAL_POSITION.PRESIDENT
        ): int(cr["vap"])
        for cr in candidates
    }


def parse_aggregate(
    result: VoteResult, municipality: MUNICIPALITY
) -> MUNICIPALITY | ELECTORAL_ZONE:
    if result["tpabr"] == "MU":
        return municipality
    elif result["tpabr"] == "ZONA":
        return ELECTORAL_ZONE(municipality, code=result["cdabr"])
    else:
        raise TSEError("Aggregate is neither municipality nor electoral zone")


def parse_vote_count(result: VoteResult, municipality: MUNICIPALITY) -> VOTE_COUNT:
    try:
        aggregate = parse_aggregate(result, municipality)
        candidates = parse_candidates(result["cand"])
        valid_votes = int(result["vv"])
        blank_votes = int(result["vb"])
        anulled_votes = int(result["vn"])
        total_votes = int(result["tv"])
        abstension = int(result["a"])
        attendance = int(result["c"])
        total_ellectors = int(result["e"])
        validate_counts(
            candidates,
            valid_votes,
            blank_votes,
            anulled_votes,
            total_votes,
            abstension,
            attendance,
            total_ellectors,
        )
    except TSEError as e:
        print("Found error during parsing.")
        traceback.print_exception(e)
        print("Object received:")
        pprint(result)

    return VOTE_COUNT(
        aggregate, valid_votes, blank_votes, anulled_votes, abstension, candidates
    )


def iter_presidential_votes(
    year: int, municipality: MUNICIPALITY
) -> Iterable[VOTE_COUNT]:
    raw_data = PresidentialVotesRequest(year, municipality).fetch()
    yield from iter_parsed_votes(raw_data, municipality)
