from __future__ import annotations

from typing import Dict

from explore_options.strategies.base import Strategy
from explore_options.strategies.covered_calls import CoveredCallsStrategy
from explore_options.strategies.echo import EchoStrategy
from explore_options.strategies.long_leaps_short_calls_diagonal import (
    LongLeapsShortCallsDiagonalStrategy,
)
from explore_options.strategies.rolling_options import RollingOptionsStrategy
from explore_options.strategies.reverse import ReverseStrategy

_STRATEGIES: Dict[str, Strategy] = {
    CoveredCallsStrategy.name: CoveredCallsStrategy(),
    EchoStrategy.name: EchoStrategy(),
    LongLeapsShortCallsDiagonalStrategy.name: LongLeapsShortCallsDiagonalStrategy(),
    RollingOptionsStrategy.name: RollingOptionsStrategy(),
    ReverseStrategy.name: ReverseStrategy(),
}


def list_strategies() -> list[Strategy]:
    return sorted(_STRATEGIES.values(), key=lambda strategy: strategy.name)


def get_strategy(name: str) -> Strategy | None:
    return _STRATEGIES.get(name)
