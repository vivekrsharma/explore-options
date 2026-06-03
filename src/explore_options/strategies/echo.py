from __future__ import annotations

from explore_options.strategies.base import Strategy, StrategyInput, StrategyOutput


class EchoStrategy(Strategy):
    name = "echo"
    description = "Return input unchanged"

    def execute(self, input_data: StrategyInput) -> StrategyOutput:
        return StrategyOutput(headline="Echo", plain_text=input_data.text_input)
