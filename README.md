# explore-options

Starter Python project scaffold.

## Quick start

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Make targets

```sh
make setup   # Create .venv and install dependencies
make test    # Run tests
make run     # Run the app entry point
make lint    # Run ruff checks
make typecheck
make clean
```

Override Python if needed:

```sh
make setup PYTHON=/path/to/python3.11
```

## Strategy Organization

This project is set up to organize each strategy as its own class under
`src/explore_options/strategies/`.

- `base.py`: shared Strategy interface
- one file per strategy, for example `echo.py` or `reverse.py`
- `registry.py`: central place where strategies are registered

Use the runner:

```sh
python -m explore_options.main --list
python -m explore_options.main --strategy reverse --input "hello"
python -m explore_options.main --strategy long-leaps-short-calls-diagonal --input "AAPL"
python -m explore_options.main --diagonal-snapshot --symbol SNOW --long-expiry 2028-01-21 --short-expiry 2026-07-17
python -m explore_options.main --diagonal-snapshot --symbol SNOW --long-expiry 2024-07-19 --short-expiry 2021-08-20 --as-of 2021-06-15 --chain-json data/snow_2021-06-15.json
```

### Add a new strategy

1. Create a new file in `src/explore_options/strategies/`.
2. Implement a class that extends `Strategy`.
3. Register an instance in `registry.py`.

Example skeleton:

```python
from explore_options.strategies.base import Strategy


class MyStrategy(Strategy):
	name = "my-strategy"
	description = "Describe what it does"

	def execute(self, input_text: str) -> str:
		return input_text
```

## Connectivity Module

Use connectivity providers from `src/explore_options/connectivity/` to pull data.

- `StooqProvider`: read-only daily bars without API keys (good for prototyping)
- `RobinhoodUnofficialProvider`: intentionally disabled with a runtime error

Why not Robinhood public APIs?

- Robinhood does not provide an official public market data API for this workflow.
- Unofficial endpoints can break, change without notice, or create account/compliance risk.

Recommended approach:

- Keep provider abstraction and start with stable/official data APIs.
- Add authenticated providers later (for example Polygon, Alpaca, Tradier) via the same interface.

### Concrete diagonal example command

Use the built-in command below to pull and rank LEAPS long-call candidates and
short-call candidates for a diagonal setup:

```sh
python -m explore_options.main --diagonal-snapshot --symbol SNOW --long-expiry 2028-01-21 --short-expiry 2026-07-17
```

For backdated analysis, save a Cboe-style chain JSON from the historical date and
run the same command with `--as-of` and `--chain-json`:

```sh
python -m explore_options.main --diagonal-snapshot --symbol SNOW --long-expiry 2024-07-19 --short-expiry 2021-07-16 --as-of 2021-06-15 --chain-json data/snow_2021-06-15.json
```
