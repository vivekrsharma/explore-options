PYTHON ?= /opt/homebrew/bin/python3.11
VENV := .venv
VENV_PY := $(VENV)/bin/python
VENV_PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest

.PHONY: setup test run lint typecheck clean

setup:
	$(PYTHON) -m venv $(VENV)
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install -e '.[dev]'

test:
	$(PYTEST) -q

run:
	$(VENV_PY) -m explore_options.main

lint:
	$(VENV)/bin/ruff check src tests

typecheck:
	$(VENV)/bin/mypy src

clean:
	rm -rf $(VENV) .pytest_cache .mypy_cache .ruff_cache