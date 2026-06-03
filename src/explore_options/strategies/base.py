from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date


@dataclass(frozen=True)
class StrategyInput:
    symbol: str = ""
    text_input: str = ""
    as_of_date: date | None = None
    long_expiry: date | None = None
    short_expiry: date | None = None
    assumptions: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class StrategyOutput:
    headline: str
    sections: dict[str, list[str]] = field(default_factory=dict)
    plain_text: str | None = None

    def render_text(self) -> str:
        if self.plain_text is not None:
            return self.plain_text

        lines = [self.headline]
        for section_title, items in self.sections.items():
            lines.append(section_title)
            for item in items:
                lines.append(f"- {item}")
            lines.append("")

        # Avoid a trailing blank line in CLI output.
        while lines and lines[-1] == "":
            lines.pop()

        return "\n".join(lines)


class Strategy(ABC):
    name: str
    description: str

    @abstractmethod
    def execute(self, input_data: StrategyInput) -> StrategyOutput:
        """Run the strategy and return its output."""
