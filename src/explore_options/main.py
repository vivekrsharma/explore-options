from __future__ import annotations

import argparse
from datetime import date

from explore_options.checklist import (
    ChecklistInput,
    evaluate_all_strategy_checklists,
    evaluate_strategy_checklist,
)
from explore_options.connectivity.cboe_options import JsonOptionChainProvider
from explore_options.connectivity.diagonal_snapshot import create_diagonal_snapshot_report
from explore_options.strategies.base import StrategyInput
from explore_options.strategies.registry import get_strategy, list_strategies


_BANNED_STRATEGY_NAMES = {
    "cash-secured-put",
    "cash-secured-puts",
    "cash secured put",
    "csp",
}


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
    parser.add_argument(
        "--checklist",
        action="store_true",
        help="Run checklist evaluation for a strategy",
    )
    parser.add_argument(
        "--checklist-all",
        action="store_true",
        help="Run checklist evaluation for all registered strategies",
    )
    parser.add_argument(
        "--capital",
        type=float,
        default=25_000,
        help="Capital available for the strategy",
    )
    parser.add_argument(
        "--max-drawdown-pct",
        type=float,
        default=30,
        help="Maximum drawdown tolerance in percent",
    )
    parser.add_argument(
        "--monitoring-days-per-week",
        type=int,
        default=3,
        help="How many days per week you can actively monitor positions",
    )
    parser.add_argument(
        "--assignment-tolerance",
        choices=["yes", "no"],
        default="yes",
        help="Whether assignment risk is acceptable",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    checklist_input = ChecklistInput(
        capital_available=args.capital,
        max_drawdown_tolerance_pct=args.max_drawdown_pct,
        monitoring_days_per_week=args.monitoring_days_per_week,
        assignment_tolerance=(args.assignment_tolerance == "yes"),
    )

    if args.checklist_all:
        names = [strategy.name for strategy in list_strategies()]
        results = evaluate_all_strategy_checklists(names, checklist_input)
        for index, result in enumerate(results):
            if index > 0:
                print()
            print(result.render_text())
        return 0

    if args.checklist:
        if not args.strategy:
            parser.error("--strategy is required when --checklist is used")
        result = evaluate_strategy_checklist(args.strategy, checklist_input)
        print(result.render_text())
        return 0

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

    if args.strategy.lower() in _BANNED_STRATEGY_NAMES:
        parser.error(f"Strategy disabled by policy: {args.strategy}")

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
