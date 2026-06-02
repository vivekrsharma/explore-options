from __future__ import annotations

from explore_options.strategies.base import Strategy


class CoveredCallsStrategy(Strategy):
    name = "covered-calls"
    description = "Long stock plus short call for income and partial downside buffer"

    def execute(self, input_text: str) -> str:
        symbol = input_text.strip() or "UNDERLYING"
        return "\n".join(
            [
                f"Strategy: Covered Calls ({symbol})",
                "Structure:",
                "- Buy or hold 100 shares of stock.",
                "- Sell 1 OTM call against every 100 shares.",
                "",
                "Objective:",
                "- Generate income from option premium.",
                "- Allow moderate upside up to strike price.",
                "",
                "Risk and trade-offs:",
                "- Downside risk from stock remains substantial.",
                "- Upside is capped above the short-call strike.",
                "- Assignment can occur before expiration.",
                "",
                "Management checklist:",
                "- Pick strike near target exit level.",
                "- Prefer expirations with sufficient premium and liquidity.",
                "- Roll or close if assignment risk is undesirable.",
            ]
        )
