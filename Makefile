export PATH := $(HOME)/.local/bin:$(PATH)

UV = $(HOME)/.local/bin/uv
MAP ?= maps/easy_01.txt

.PHONY: install run debug clean lint lint-strict

install:
	@if ! command -v uv >/dev/null 2>&1; then \
		echo "Installing uv..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	fi
	@command -v uv >/dev/null 2>&1 || { echo "uv installation failed"; exit 1; }
	uv sync

run:
	uv run python main.py $(MAP)

debug:
	uv run python -m pdb main.py $(MAP)

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache

lint:
	uv run flake8 .
	uv run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run --with flake8 flake8 .
	uv run python -m mypy . --strict