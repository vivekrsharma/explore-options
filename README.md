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
