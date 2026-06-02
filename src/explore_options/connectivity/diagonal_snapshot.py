from __future__ import annotations

from datetime import date
from typing import Protocol

from explore_options.connectivity.cboe_options import (
    CboeDelayedOptionsProvider,
    OptionCallQuote,
    OptionChainSnapshot,
)


class OptionChainProvider(Protocol):
    def get_option_chain(self, symbol: str) -> OptionChainSnapshot:
        ...


def _is_liquid(option: OptionCallQuote) -> bool:
    return option.open_interest > 0 and option.bid > 0 and option.ask > 0


def _select_long_leaps(calls: list[OptionCallQuote], limit: int = 6) -> list[OptionCallQuote]:
    liquid = [option for option in calls if _is_liquid(option)]
    deep_itm = [option for option in liquid if (option.delta or 0) >= 0.7]
    ranked = sorted(
        deep_itm,
        key=lambda option: (option.open_interest, -(option.ask - option.bid)),
        reverse=True,
    )
    return ranked[:limit]


def _select_short_calls(
    calls: list[OptionCallQuote],
    spot: float,
    limit: int = 8,
) -> list[OptionCallQuote]:
    liquid = [option for option in calls if _is_liquid(option)]
    otm_band = [
        option
        for option in liquid
        if option.strike > spot and 0.15 <= (option.delta or 0) <= 0.40
    ]
    ranked = sorted(
        otm_band,
        key=lambda option: (option.open_interest, option.volume),
        reverse=True,
    )
    return ranked[:limit]


def create_diagonal_snapshot_report(
    symbol: str,
    long_expiry: date,
    short_expiry: date,
    provider: OptionChainProvider | None = None,
    as_of_date: date | None = None,
) -> str:
    source: OptionChainProvider = provider or CboeDelayedOptionsProvider()

    if as_of_date is not None:
        if long_expiry <= as_of_date:
            raise ValueError("Long expiry must be later than as-of date.")
        if short_expiry <= as_of_date:
            raise ValueError("Short expiry must be later than as-of date.")

    snapshot: OptionChainSnapshot = source.get_option_chain(symbol)

    available_calls = snapshot.calls
    if as_of_date is not None:
        available_calls = [option for option in available_calls if option.expiry > as_of_date]

    long_calls = [option for option in available_calls if option.expiry == long_expiry]
    short_calls = [option for option in available_calls if option.expiry == short_expiry]

    selected_long = _select_long_leaps(long_calls)
    selected_short = _select_short_calls(short_calls, spot=snapshot.spot)

    lines = [
        f"Diagonal snapshot for {snapshot.symbol}",
        f"Spot: {snapshot.spot:.2f}",
        (
            f"Scenario as-of date: {as_of_date.isoformat()}"
            if as_of_date is not None
            else "Scenario as-of date: live snapshot"
        ),
        f"Long expiry: {long_expiry.isoformat()} (available calls: {len(long_calls)})",
        f"Short expiry: {short_expiry.isoformat()} (available calls: {len(short_calls)})",
        f"Data timestamp: {snapshot.timestamp}",
        "",
        "LEAPS long-call candidates:",
    ]

    if selected_long:
        for option in selected_long:
            lines.append(
                "- "
                f"{option.contract} | strike {option.strike:.2f} | "
                f"bid/ask {option.bid:.2f}/{option.ask:.2f} | "
                f"delta {(option.delta or 0):.4f} | OI {int(option.open_interest)} | "
                f"vol {int(option.volume)}"
            )
    else:
        lines.append("- No LEAPS candidates matched the liquidity and delta filters.")

    lines.append("")
    lines.append("Short-call candidates:")

    if selected_short:
        for option in selected_short:
            lines.append(
                "- "
                f"{option.contract} | strike {option.strike:.2f} | "
                f"bid/ask {option.bid:.2f}/{option.ask:.2f} | "
                f"delta {(option.delta or 0):.4f} | OI {int(option.open_interest)} | "
                f"vol {int(option.volume)}"
            )
    else:
        lines.append("- No short-call candidates matched the OTM delta band and liquidity filters.")

    return "\n".join(lines)
