from __future__ import annotations

from explore_options.strategies.base import Strategy


class LongLeapsShortCallsDiagonalStrategy(Strategy):
    name = "long-leaps-short-calls-diagonal"
    description = "Long-dated call plus short front-month calls (PMCC style diagonal)"

    def execute(self, input_text: str) -> str:
        symbol = input_text.strip() or "UNDERLYING"
        return "\n".join(
            [
                f"Strategy: Long LEAPS + Short Calls Diagonal ({symbol})",
                "Structure:",
                "- Buy a long-dated call (LEAPS), typically deep ITM with high delta.",
                "- Sell shorter-dated OTM call(s) against the LEAPS.",
                "- Use different strike and expiration: diagonal across strike and calendar.",
                "",
                "Typical objective:",
                "- Reduce LEAPS cost basis over time from short-call premium.",
                "- Keep directional upside exposure while capping near-term upside.",
                "",
                "Risk focus:",
                "- Large downside risk if underlying falls and LEAPS value decays.",
                "- Assignment risk on short calls near expiration/ex-div dates.",
                "- Volatility and term-structure changes can impact both legs differently.",
                "",
                "Management checklist:",
                "- Choose LEAPS with enough time/value buffer.",
                "- Sell short call above expected near-term move.",
                "- Roll short call if tested or near expiration.",
                "- Re-evaluate if thesis breaks or net delta becomes too small/large.",
            ]
        )