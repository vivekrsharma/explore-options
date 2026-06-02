from __future__ import annotations

from explore_options.strategies.base import Strategy


class EchoStrategy(Strategy):
    name = "echo"
    description = "Return input unchanged"

    def execute(self, input_text: str) -> str:
        return input_text
