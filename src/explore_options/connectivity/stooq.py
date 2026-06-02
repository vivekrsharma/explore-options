from __future__ import annotations

import csv
from datetime import date

import requests

from explore_options.connectivity.base import DailyBar, MarketDataProvider


class StooqProvider(MarketDataProvider):
    name = "stooq"
    _BASE_URL = "https://stooq.com/q/d/l/"

    def __init__(self, session: requests.Session | None = None) -> None:
        self._session = session or requests.Session()

    def get_daily_bars(
        self,
        symbol: str,
        start: date | None = None,
        end: date | None = None,
    ) -> list[DailyBar]:
        params = {"s": symbol.lower(), "i": "d"}
        response = self._session.get(self._BASE_URL, params=params, timeout=15)
        response.raise_for_status()

        bars = self._parse_csv(symbol=symbol.upper(), csv_text=response.text)

        if start is not None:
            bars = [bar for bar in bars if bar.trading_date >= start]
        if end is not None:
            bars = [bar for bar in bars if bar.trading_date <= end]

        return bars

    @staticmethod
    def _parse_csv(symbol: str, csv_text: str) -> list[DailyBar]:
        reader = csv.DictReader(csv_text.splitlines())
        bars: list[DailyBar] = []

        for row in reader:
            if row.get("Close") in {None, "N/D"}:
                continue
            bars.append(
                DailyBar(
                    symbol=symbol,
                    trading_date=date.fromisoformat(row["Date"]),
                    open=float(row["Open"]),
                    high=float(row["High"]),
                    low=float(row["Low"]),
                    close=float(row["Close"]),
                    volume=int(float(row["Volume"])),
                )
            )

        bars.sort(key=lambda bar: bar.trading_date)
        return bars
