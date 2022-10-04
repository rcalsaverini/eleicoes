import json
from multiprocessing.sharedctypes import Value
import traceback
from typing import Any, Protocol
from urllib.error import HTTPError

import requests


def make_request(url):
    req = requests.get(url)
    try:
        req.raise_for_status()
    except HTTPError as e:
        traceback.print_exception(e)
        raise ValueError(f"Failed to get data from {url}")
    return req


def load_json(raw_data):
    try:
        return json.loads(raw_data)
    except Exception as e:
        traceback.print_exception(e)
        raise ValueError(f"Failed to parse json output. Received: {raw_data}.")


class TSE_Request(Protocol):
    def build_url(self) -> str:
        raise NotImplementedError()

    def fetch(self) -> dict[str, Any]:
        url = self.build_url()
        req = make_request(url)
        return load_json(req.content)


class TSEError(ValueError):
    pass
