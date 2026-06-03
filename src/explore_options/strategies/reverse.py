from __future__ import annotations

from explore_options.strategies.base import Strategy, StrategyInput, StrategyOutput


class ReverseStrategy(Strategy):
    name = "reverse"
    description = "Reverse input text"

    def execute(self, input_data: StrategyInput) -> StrategyOutput:
        return StrategyOutput(headline="Reverse", plain_text=input_data.text_input[::-1])
