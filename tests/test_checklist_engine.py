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
            dte_days=45,
        ),
    )

    assert result.passed is True
    assert result.score == 2
    assert result.confidence_score == 100
    assert result.confidence_label == "High"


def test_evaluate_strategy_checklist_fails_when_dte_too_short() -> None:
    result = evaluate_strategy_checklist(
        "long-leaps-short-calls-diagonal",
        ChecklistInput(capital_available=20_000, dte_days=15),
    )

    assert result.passed is False
    assert any("DTE" in item for item in result.warnings)
    assert result.score == 1
    assert result.confidence_score == 50
    assert result.confidence_label == "Low"


def test_evaluate_strategy_checklist_fails_for_banned_csp() -> None:
    result = evaluate_strategy_checklist("csp", ChecklistInput())

    assert result.passed is False
    assert any("emotional-turmoil policy" in item for item in result.hard_failures)
    assert result.confidence_score <= 25
    assert result.confidence_label == "Low"


def test_evaluate_all_strategy_checklists_returns_sorted_results() -> None:
    results = evaluate_all_strategy_checklists(
        ["reverse", "covered-calls"],
        ChecklistInput(),
    )

    names = [result.strategy_name for result in results]
    assert names == ["covered-calls", "reverse"]


def test_checklist_result_render_includes_confidence() -> None:
    result = evaluate_strategy_checklist("covered-calls", ChecklistInput())
    rendered = result.render_text()

    assert "Confidence:" in rendered
