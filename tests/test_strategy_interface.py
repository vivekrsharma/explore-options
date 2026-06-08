from __future__ import annotations

from explore_options.strategies.base import StrategyInput, StrategyOutput
from explore_options.strategies.covered_calls import CoveredCallsStrategy
from explore_options.strategies.echo import EchoStrategy
from explore_options.strategies.rolling_options import RollingOptionsStrategy
from explore_options.strategies.reverse import ReverseStrategy


def test_strategy_output_render_plain_text() -> None:
    output = StrategyOutput(headline="ignored", plain_text="hello")

    assert output.render_text() == "hello"


def test_echo_strategy_uses_structured_input() -> None:
    strategy = EchoStrategy()

    rendered = strategy.execute(StrategyInput(text_input="abc")).render_text()

    assert rendered == "abc"


def test_reverse_strategy_uses_structured_input() -> None:
    strategy = ReverseStrategy()

    rendered = strategy.execute(StrategyInput(text_input="abcd")).render_text()

    assert rendered == "dcba"


def test_covered_calls_strategy_output_sections() -> None:
    strategy = CoveredCallsStrategy()

    rendered = strategy.execute(StrategyInput(symbol="SNOW")).render_text()

    assert "Strategy: Covered Calls (SNOW)" in rendered
    assert "Structure:" in rendered
    assert "Objective:" in rendered


def test_rolling_options_strategy_output_sections() -> None:
    strategy = RollingOptionsStrategy()

    rendered = strategy.execute(StrategyInput(symbol="MSFT")).render_text()

    assert "Strategy: Rolling Options (MSFT)" in rendered
    assert "Structure:" in rendered
    assert "Objective:" in rendered
