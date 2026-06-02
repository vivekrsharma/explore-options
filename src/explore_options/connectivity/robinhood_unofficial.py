from __future__ import annotations

from datetime import date

from explore_options.connectivity.base import DailyBar, MarketDataProvider


class RobinhoodUnofficialProvider(MarketDataProvider):
    name = "robinhood-unofficial"

    def get_daily_bars(
        self,
        symbol: str,
        start: date | None = None,
        end: date | None = None,
    ) -> list[DailyBar]:
        raise RuntimeError(
            "Robinhood does not provide an official public market data API for this use case. "
            "Use a supported provider (for example Stooq, Polygon, Alpaca, or other official APIs)."
        )
