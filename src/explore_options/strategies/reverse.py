from __future__ import annotations

from explore_options.strategies.base import Strategy


class ReverseStrategy(Strategy):
    name = "reverse"
    description = "Reverse input text"

    def execute(self, input_text: str) -> str:
        return input_text[::-1]
