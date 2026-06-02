import pytest

import explore_options.main as main_module
from explore_options.main import main


def test_list_strategies(capsys):
    exit_code = main(["--list"])
    captured = capsys.readouterr()

    assert exit_code == 0
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


def test_run_long_leaps_short_calls_diagonal_strategy(capsys):
    exit_code = main(
        ["--strategy", "long-leaps-short-calls-diagonal", "--input", "AAPL"]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Long LEAPS + Short Calls Diagonal (AAPL)" in captured.out


def test_diagonal_snapshot_cli(monkeypatch: pytest.MonkeyPatch, capsys):
    def _fake_report(symbol, long_expiry, short_expiry):
        assert symbol == "SNOW"
        assert long_expiry.isoformat() == "2028-01-21"
        assert short_expiry.isoformat() == "2026-07-17"
        return "snapshot-ok"

    monkeypatch.setattr(main_module, "create_diagonal_snapshot_report", _fake_report)

    exit_code = main(["--diagonal-snapshot"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out.strip() == "snapshot-ok"
