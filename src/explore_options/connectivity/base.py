from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class DailyBar:
    symbol: str
    trading_date: date
    open: float
    high: float
    low: float
    close: float
    volume: int


class MarketDataProvider(ABC):
    name: str

    @abstractmethod
    def get_daily_bars(
        self,
        symbol: str,
        start: date | None = None,
        end: date | None = None,
    ) -> list[DailyBar]:
        """Fetch daily OHLCV bars for a symbol."""
