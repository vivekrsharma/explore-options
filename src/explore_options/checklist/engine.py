from __future__ import annotations

from dataclasses import dataclass, field


_BANNED_EMOTIONAL_TURMOIL_STRATEGIES = {
    "cash-secured-put",
    "cash-secured-puts",
    "cash secured put",
    "csp",
}


@dataclass(frozen=True)
class ChecklistInput:
    capital_available: float = 25_000.0
    max_drawdown_tolerance_pct: float = 30.0
    monitoring_days_per_week: int = 3
    assignment_tolerance: bool = True


@dataclass(frozen=True)
class ChecklistResult:
    strategy_name: str
    passed: bool
    score: int
    max_score: int
    hard_failures: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def render_text(self) -> str:
        lines = [
            f"Checklist for {self.strategy_name}",
            f"Result: {'PASS' if self.passed else 'FAIL'}",
            f"Score: {self.score}/{self.max_score}",
        ]

        if self.hard_failures:
            lines.append("Hard failures:")
            for item in self.hard_failures:
                lines.append(f"- {item}")

        if self.warnings:
            lines.append("Warnings:")
            for item in self.warnings:
                lines.append(f"- {item}")

        return "\n".join(lines)


def _evaluate_common_hard_rules(strategy_name: str, checklist: ChecklistInput) -> list[str]:
    failures: list[str] = []

    if strategy_name.lower() in _BANNED_EMOTIONAL_TURMOIL_STRATEGIES:
        failures.append("Strategy is banned by emotional-turmoil policy.")

    if not checklist.assignment_tolerance and strategy_name in {
        "covered-calls",
        "long-leaps-short-calls-diagonal",
    }:
        failures.append("Assignment tolerance is required for short-call strategies.")

    return failures


def evaluate_strategy_checklist(
    strategy_name: str,
    checklist: ChecklistInput,
) -> ChecklistResult:
    hard_failures = _evaluate_common_hard_rules(strategy_name, checklist)

    score = 0
    max_score = 5
    warnings: list[str] = []

    if checklist.capital_available >= 10_000:
        score += 1
    else:
        warnings.append("Capital below 10,000 may limit flexibility.")

    if checklist.max_drawdown_tolerance_pct >= 25:
        score += 1
    else:
        warnings.append("Drawdown tolerance below 25% may not fit equity-based options.")

    if checklist.monitoring_days_per_week >= 2:
        score += 1
    else:
        warnings.append("Monitoring fewer than 2 days/week may be insufficient for adjustments.")

    if strategy_name == "covered-calls":
        if checklist.capital_available >= 15_000:
            score += 1
        else:
            warnings.append("Covered calls generally need enough capital for 100-share lots.")

        if checklist.max_drawdown_tolerance_pct >= 30:
            score += 1
        else:
            warnings.append("Covered calls still carry meaningful downside stock risk.")

    elif strategy_name == "long-leaps-short-calls-diagonal":
        if checklist.monitoring_days_per_week >= 3:
            score += 1
        else:
            warnings.append("Diagonal strategies benefit from active monitoring.")

        if checklist.max_drawdown_tolerance_pct >= 35:
            score += 1
        else:
            warnings.append("Diagonal setups can experience larger drawdowns and greek drift.")

    else:
        # Generic strategy path.
        score += 2

    passed = not hard_failures and score >= 3

    return ChecklistResult(
        strategy_name=strategy_name,
        passed=passed,
        score=score,
        max_score=max_score,
        hard_failures=hard_failures,
        warnings=warnings,
    )


def evaluate_all_strategy_checklists(
    strategy_names: list[str],
    checklist: ChecklistInput,
) -> list[ChecklistResult]:
    return [evaluate_strategy_checklist(name, checklist) for name in sorted(strategy_names)]
