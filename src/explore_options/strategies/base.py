from __future__ import annotations

from abc import ABC, abstractmethod


class Strategy(ABC):
    name: str
    description: str

    @abstractmethod
    def execute(self, input_text: str) -> str:
        """Run the strategy and return its output."""
