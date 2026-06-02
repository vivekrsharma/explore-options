from explore_options.main import main


def test_main_runs(capsys):
    main()
    captured = capsys.readouterr()
    assert "Hello from explore-options" in captured.out
