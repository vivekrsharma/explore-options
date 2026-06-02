from __future__ import annotations

from explore_options.strategies.covered_calls import CoveredCallsStrategy
from explore_options.strategies.registry import get_strategy


def test_covered_calls_strategy_with_symbol() -> None:
    strategy = CoveredCallsStrategy()

    output = strategy.execute("SNOW")

    assert "Strategy: Covered Calls (SNOW)" in output
    assert "Buy or hold 100 shares of stock." in output
    assert "Sell 1 OTM call against every 100 shares." in output


def test_covered_calls_strategy_default_symbol() -> None:
    strategy = CoveredCallsStrategy()

    output = strategy.execute("")

    assert "Strategy: Covered Calls (UNDERLYING)" in output


def test_registry_returns_covered_calls_strategy() -> None:
    strategy = get_strategy("covered-calls")

    assert strategy is not None
    assert strategy.name == "covered-calls"