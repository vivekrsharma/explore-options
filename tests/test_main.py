import pytest

import explore_options.main as main_module
from explore_options.main import main


def test_list_strategies(capsys):
    exit_code = main(["--list"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "covered-calls" in captured.out
    assert "echo" in captured.out
    assert "long-leaps-short-calls-diagonal" in captured.out
    assert "reverse" in captured.out


def test_run_reverse_strategy(capsys):
    exit_code = main(["--strategy", "reverse", "--input", "abcd"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out.strip() == "dcba"


def test_unknown_strategy_fails():
    with pytest.raises(SystemExit):
        main(["--strategy", "missing"])


@pytest.mark.parametrize("name", ["cash-secured-put", "cash-secured-puts", "csp"])
def test_banned_cash_secured_put_strategy_fails(name: str):
    with pytest.raises(SystemExit):
        main(["--strategy", name])


def test_run_long_leaps_short_calls_diagonal_strategy(capsys):
    exit_code = main(
        ["--strategy", "long-leaps-short-calls-diagonal", "--input", "AAPL"]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Long LEAPS + Short Calls Diagonal (AAPL)" in captured.out


def test_run_covered_calls_strategy(capsys):
    exit_code = main(["--strategy", "covered-calls", "--input", "SNOW"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Strategy: Covered Calls (SNOW)" in captured.out


def test_diagonal_snapshot_cli(monkeypatch: pytest.MonkeyPatch, capsys):
    def _fake_report(symbol, long_expiry, short_expiry, provider, as_of_date):
        assert symbol == "SNOW"
        assert long_expiry.isoformat() == "2028-01-21"
        assert short_expiry.isoformat() == "2026-07-17"
        assert provider is None
        assert as_of_date is None
        return "snapshot-ok"

    monkeypatch.setattr(main_module, "create_diagonal_snapshot_report", _fake_report)

    exit_code = main(["--diagonal-snapshot"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out.strip() == "snapshot-ok"


def test_diagonal_snapshot_cli_with_as_of_and_chain_json(
    monkeypatch: pytest.MonkeyPatch,
    capsys,
):
    def _fake_provider(path: str):
        assert path == "tests/fixtures/snow_2021-06-15.json"
        return "provider-ok"

    def _fake_report(symbol, long_expiry, short_expiry, provider, as_of_date):
        assert symbol == "SNOW"
        assert provider == "provider-ok"
        assert as_of_date.isoformat() == "2021-06-15"
        return "snapshot-with-as-of"

    monkeypatch.setattr(main_module, "JsonOptionChainProvider", _fake_provider)
    monkeypatch.setattr(main_module, "create_diagonal_snapshot_report", _fake_report)

    exit_code = main(
        [
            "--diagonal-snapshot",
            "--symbol",
            "SNOW",
            "--long-expiry",
            "2024-07-19",
            "--short-expiry",
            "2021-08-20",
            "--as-of",
            "2021-06-15",
            "--chain-json",
            "tests/fixtures/snow_2021-06-15.json",
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out.strip() == "snapshot-with-as-of"


def test_checklist_cli_requires_strategy():
    with pytest.raises(SystemExit):
        main(["--checklist"])


def test_checklist_cli_single_strategy(capsys):
    exit_code = main(["--checklist", "--strategy", "covered-calls"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Checklist for covered-calls" in captured.out


def test_checklist_cli_all_strategies(capsys):
    exit_code = main(["--checklist-all"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Checklist for covered-calls" in captured.out
    assert "Checklist for long-leaps-short-calls-diagonal" in captured.out
