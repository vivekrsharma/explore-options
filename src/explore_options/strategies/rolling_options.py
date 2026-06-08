from __future__ import annotations

from explore_options.strategies.base import Strategy, StrategyInput, StrategyOutput


class RollingOptionsStrategy(Strategy):
    name = "rolling-options"
    description = "Roll option positions to extend duration and improve annualized return"

    def execute(self, input_data: StrategyInput) -> StrategyOutput:
        symbol = input_data.symbol.strip() or "UNDERLYING"
        return StrategyOutput(
            headline=f"Strategy: Rolling Options ({symbol})",
            sections={
                "Structure:": [
                    "Start with an existing short option (often near expiration).",
                    "Close current contract and open a later-dated contract in one roll.",
                    "Adjust strike and expiry to rebalance assignment risk and credit.",
                ],
                "Objective:": [
                    "Extend trade duration while collecting additional credit.",
                    "Maintain target risk while improving annualized return profile.",
                ],
                "Risk and trade-offs:": [
                    "Repeated rolls can defer but not remove directional risk.",
                    "Rolling for debit can reduce overall expectancy.",
                    "Liquidity and slippage can materially impact realized credits.",
                ],
                "Management checklist:": [
                    "Prefer rolling before assignment risk becomes acute.",
                    "Target rolls that preserve or improve annualized return.",
                    "Avoid low-liquidity strikes and expirations with wide spreads.",
                ],
            },
        )
