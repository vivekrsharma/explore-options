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
    dte_days: int = 30
    annualized_percent_return: float = 0.0


@dataclass(frozen=True)
class ChecklistResult:
    strategy_name: str
    passed: bool
    score: int
    max_score: int
    confidence_score: int
    confidence_label: str
    confidence_adjustments: list[str] = field(default_factory=list)
    hard_failures: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def render_text(self) -> str:
        lines = [
            f"Checklist for {self.strategy_name}",
            f"Result: {'PASS' if self.passed else 'FAIL'}",
            f"Score: {self.score}/{self.max_score}",
            f"Confidence: {self.confidence_score} ({self.confidence_label})",
        ]

        if self.confidence_adjustments:
            lines.append("Confidence adjustments:")
            for item in self.confidence_adjustments:
                lines.append(f"- {item}")

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

    return failures


def evaluate_strategy_checklist(
    strategy_name: str,
    checklist: ChecklistInput,
) -> ChecklistResult:
    hard_failures = _evaluate_common_hard_rules(strategy_name, checklist)

    normalized_name = strategy_name.lower().strip()
    is_rolling = normalized_name == "rolling-options"

    score = 0
    max_score = 2
    warnings: list[str] = []

    if is_rolling:
        if checklist.dte_days >= 30:
            score += 1
        else:
            warnings.append("Rolling options requires DTE of at least 30 days.")

        if checklist.annualized_percent_return > 20:
            score += 1
        else:
            warnings.append("Rolling options requires annualized percent return above 20%.")
    else:
        if checklist.capital_available > 10_000:
            score += 1
        else:
            warnings.append("Capital must be greater than 10,000.")

        if checklist.dte_days >= 30:
            score += 1
        else:
            warnings.append("DTE must be 30 days or greater.")

    passed = not hard_failures and score == max_score

    confidence_adjustments: list[str] = []
    base_confidence = round((score / max_score) * 100)
    confidence_score = base_confidence

    if hard_failures and confidence_score > 25:
        confidence_adjustments.append("capped to 25 due to hard-failure policy")
        confidence_score = 25

    if confidence_score >= 80:
        confidence_label = "High"
    elif confidence_score >= 60:
        confidence_label = "Medium"
    else:
        confidence_label = "Low"

    return ChecklistResult(
        strategy_name=strategy_name,
        passed=passed,
        score=score,
        max_score=max_score,
        confidence_score=confidence_score,
        confidence_label=confidence_label,
        confidence_adjustments=confidence_adjustments,
        hard_failures=hard_failures,
        warnings=warnings,
    )


def evaluate_all_strategy_checklists(
    strategy_names: list[str],
    checklist: ChecklistInput,
) -> list[ChecklistResult]:
    return [evaluate_strategy_checklist(name, checklist) for name in sorted(strategy_names)]
