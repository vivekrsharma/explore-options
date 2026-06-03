from __future__ import annotations

import argparse
from datetime import date

from explore_options.connectivity.cboe_options import JsonOptionChainProvider
from explore_options.connectivity.diagonal_snapshot import create_diagonal_snapshot_report
from explore_options.strategies.base import StrategyInput
from explore_options.strategies.registry import get_strategy, list_strategies


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run or list available strategies.")
    parser.add_argument("--list", action="store_true", help="List available strategies")
    parser.add_argument("--strategy", help="Strategy name to run")
    parser.add_argument("--input", default="", help="Input passed to the strategy")
    parser.add_argument(
        "--diagonal-snapshot",
        action="store_true",
        help="Show a concrete LEAPS + short-call snapshot from market data",
    )
    parser.add_argument("--symbol", default="SNOW", help="Underlying ticker symbol")
    parser.add_argument(
        "--long-expiry",
        default="2028-01-21",
        help="Long-call expiry in YYYY-MM-DD",
    )
    parser.add_argument(
        "--short-expiry",
        default="2026-07-17",
        help="Short-call expiry in YYYY-MM-DD",
    )
    parser.add_argument(
        "--as-of",
        help="Scenario as-of date in YYYY-MM-DD (use with historical chain snapshots)",
    )
    parser.add_argument(
        "--chain-json",
        help="Path to saved Cboe-style option chain JSON for backdated analysis",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.diagonal_snapshot:
        long_expiry = date.fromisoformat(args.long_expiry)
        short_expiry = date.fromisoformat(args.short_expiry)
        as_of_date = date.fromisoformat(args.as_of) if args.as_of else None
        provider = JsonOptionChainProvider(args.chain_json) if args.chain_json else None
        print(
            create_diagonal_snapshot_report(
                symbol=args.symbol,
                long_expiry=long_expiry,
                short_expiry=short_expiry,
                provider=provider,
                as_of_date=as_of_date,
            )
        )
        return 0

    if args.list:
        print("Available strategies:")
        for strategy in list_strategies():
            print(f"- {strategy.name}: {strategy.description}")
        return 0

    if not args.strategy:
        parser.error("--strategy is required unless --list is used")

    strategy = get_strategy(args.strategy)
    if strategy is None:
        parser.error(f"Unknown strategy: {args.strategy}")

    strategy_input = StrategyInput(
        symbol=(args.input.strip() or "UNDERLYING"),
        text_input=args.input,
    )
    output = strategy.execute(strategy_input)
    print(output.render_text())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
