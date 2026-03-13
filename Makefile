SHELL := /bin/bash
.PHONY: help build format lint test

help:
	@grep '^\.PHONY' Makefile | cut -d' ' -f2- | tr ' ' '\n'

build:
	uv run python build.py

format:
	uv run isort .
	uv run black .

lint:
	uv run isort -c --diff .
	uv run black --check .
	uv run flake8 .

test:
	uv run pytest --cov=api --cov-report term --cov-report xml ./tests
