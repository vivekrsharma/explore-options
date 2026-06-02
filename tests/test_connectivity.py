from __future__ import annotations

from datetime import date
from datetime import datetime

import pytest

from explore_options.connectivity.robinhood_unofficial import RobinhoodUnofficialProvider
from explore_options.connectivity.cboe_options import OptionCallQuote, OptionChainSnapshot
from explore_options.connectivity.diagonal_snapshot import create_diagonal_snapshot_report
from explore_options.connectivity.stooq import StooqProvider


class _FakeResponse:
    def __init__(self, text: str) -> None:
        self.text = text

    def raise_for_status(self) -> None:
        return None


class _FakeSession:
    def __init__(self, text: str) -> None:
        self._text = text

    def get(self, url: str, params: dict[str, str], timeout: int) -> _FakeResponse:
        assert params["s"] == "aapl"
        assert params["i"] == "d"
        assert timeout == 15
        return _FakeResponse(self._text)


def test_stooq_provider_parses_and_filters() -> None:
    csv_text = "\n".join(
        [
            "Date,Open,High,Low,Close,Volume",
            "2026-05-28,100,110,99,108,1000000",
            "2026-05-29,108,112,107,111,1200000",
            "2026-05-30,111,113,109,N/D,0",
        ]
    )
    provider = StooqProvider(session=_FakeSession(csv_text))

    bars = provider.get_daily_bars(
        "AAPL",
        start=date(2026, 5, 29),
        end=date(2026, 5, 30),
    )

    assert len(bars) == 1
    assert bars[0].symbol == "AAPL"
    assert bars[0].trading_date == date(2026, 5, 29)
    assert bars[0].close == 111.0


def test_robinhood_unofficial_provider_raises() -> None:
    provider = RobinhoodUnofficialProvider()
    with pytest.raises(RuntimeError):
        provider.get_daily_bars("AAPL")


class _FakeCboeProvider:
    def get_option_chain(self, symbol: str) -> OptionChainSnapshot:
        assert symbol == "SNOW"
        return OptionChainSnapshot(
            symbol="SNOW",
            spot=276.75,
            timestamp=str(datetime(2026, 6, 2, 1, 32, 42)),
            calls=[
                OptionCallQuote(
                    contract="SNOW280121C00230000",
                    expiry=date(2028, 1, 21),
                    strike=230.0,
                    bid=115.2,
                    ask=122.0,
                    delta=0.7687,
                    open_interest=3938,
                    volume=28,
                ),
                OptionCallQuote(
                    contract="SNOW280121C00370000",
                    expiry=date(2028, 1, 21),
                    strike=370.0,
                    bid=60.0,
                    ask=70.0,
                    delta=0.45,
                    open_interest=1200,
                    volume=20,
                ),
                OptionCallQuote(
                    contract="SNOW260717C00320000",
                    expiry=date(2026, 7, 17),
                    strike=320.0,
                    bid=13.55,
                    ask=14.45,
                    delta=0.3453,
                    open_interest=298,
                    volume=473,
                ),
                OptionCallQuote(
                    contract="SNOW260717C00270000",
                    expiry=date(2026, 7, 17),
                    strike=270.0,
                    bid=22.0,
                    ask=24.0,
                    delta=0.55,
                    open_interest=500,
                    volume=300,
                ),
            ],
        )


def test_create_diagonal_snapshot_report_filters_candidates() -> None:
    report = create_diagonal_snapshot_report(
        symbol="SNOW",
        long_expiry=date(2028, 1, 21),
        short_expiry=date(2026, 7, 17),
        provider=_FakeCboeProvider(),
    )

    assert "SNOW280121C00230000" in report
    assert "SNOW280121C00370000" not in report
    assert "SNOW260717C00320000" in report
    assert "SNOW260717C00270000" not in report
