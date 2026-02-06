.PHONY: install lint format test check all

install:
	uv sync --extra dev
	uv run pre-commit install

lint:
	uv run ruff check .

format:
	uv run ruff format .
	uv run ruff check --fix .

test:
	uv run pytest -v

check:
	uv run ruff check .
	uv run ruff format --check .
	uv run pytest -v

all: format lint test
