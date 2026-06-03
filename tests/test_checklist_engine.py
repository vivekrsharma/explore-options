from __future__ import annotations

from explore_options.checklist.engine import (
    ChecklistInput,
    evaluate_all_strategy_checklists,
    evaluate_strategy_checklist,
)


def test_evaluate_strategy_checklist_passes_for_covered_calls() -> None:
    result = evaluate_strategy_checklist(
        "covered-calls",
        ChecklistInput(
            capital_available=30_000,
            max_drawdown_tolerance_pct=40,
            monitoring_days_per_week=3,
            assignment_tolerance=True,
        ),
    )

    assert result.passed is True
    assert result.score >= 3


def test_evaluate_strategy_checklist_fails_when_assignment_not_tolerated() -> None:
    result = evaluate_strategy_checklist(
        "long-leaps-short-calls-diagonal",
        ChecklistInput(assignment_tolerance=False),
    )

    assert result.passed is False
    assert any("Assignment tolerance" in item for item in result.hard_failures)


def test_evaluate_strategy_checklist_fails_for_banned_csp() -> None:
    result = evaluate_strategy_checklist("csp", ChecklistInput())

    assert result.passed is False
    assert any("emotional-turmoil policy" in item for item in result.hard_failures)


def test_evaluate_all_strategy_checklists_returns_sorted_results() -> None:
    results = evaluate_all_strategy_checklists(
        ["reverse", "covered-calls"],
        ChecklistInput(),
    )

    names = [result.strategy_name for result in results]
    assert names == ["covered-calls", "reverse"]
