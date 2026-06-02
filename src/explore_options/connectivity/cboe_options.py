from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
import json
from pathlib import Path
import re

import requests


@dataclass(frozen=True)
class OptionCallQuote:
    contract: str
    expiry: date
    strike: float
    bid: float
    ask: float
    delta: float | None
    open_interest: float
    volume: float


@dataclass(frozen=True)
class OptionChainSnapshot:
    symbol: str
    spot: float
    timestamp: str
    calls: list[OptionCallQuote]


class CboeDelayedOptionsProvider:
    _BASE_URL = "https://cdn.cboe.com/api/global/delayed_quotes/options"

    def __init__(self, session: requests.Session | None = None) -> None:
        self._session = session or requests.Session()

    def get_option_chain(self, symbol: str) -> OptionChainSnapshot:
        upper_symbol = symbol.upper()
        url = f"{self._BASE_URL}/{upper_symbol}.json"
        response = self._session.get(url, timeout=20)
        response.raise_for_status()
        payload = response.json()

        return parse_cboe_option_chain_payload(payload=payload, symbol=upper_symbol)


class JsonOptionChainProvider:
    """Load a previously saved Cboe-style option-chain JSON for backdated analysis."""

    def __init__(self, file_path: str) -> None:
        self._file_path = Path(file_path)

    def get_option_chain(self, symbol: str) -> OptionChainSnapshot:
        raw = self._file_path.read_text(encoding="utf-8")
        payload = json.loads(raw)
        return parse_cboe_option_chain_payload(payload=payload, symbol=symbol.upper())


def parse_cboe_option_chain_payload(payload: dict, symbol: str) -> OptionChainSnapshot:
    data = payload["data"]
    spot = float(data["current_price"])
    timestamp = str(payload["timestamp"])

    pattern = re.compile(rf"^{symbol}(\d{{6}})([CP])(\d{{8}})$")
    calls: list[OptionCallQuote] = []

    for row in data["options"]:
        contract = str(row["option"])
        match = pattern.match(contract)
        if not match:
            continue
        if match.group(2) != "C":
            continue

        expiry = datetime.strptime(match.group(1), "%y%m%d").date()
        strike = int(match.group(3)) / 1000.0
        calls.append(
            OptionCallQuote(
                contract=contract,
                expiry=expiry,
                strike=strike,
                bid=float(row.get("bid") or 0),
                ask=float(row.get("ask") or 0),
                delta=(float(row["delta"]) if row.get("delta") is not None else None),
                open_interest=float(row.get("open_interest") or 0),
                volume=float(row.get("volume") or 0),
            )
        )

    return OptionChainSnapshot(
        symbol=symbol,
        spot=spot,
        timestamp=timestamp,
        calls=calls,
    )
