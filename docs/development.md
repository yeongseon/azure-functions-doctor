# Development Guide

This project uses Hatch, pytest, Ruff, Black, mypy, and Bandit.

## Prerequisites

- Python 3.10+
- Hatch
- Make

## Setup

```bash
make bootstrap
source .venv/bin/activate
make install
make precommit-install
```

## Common Commands

```bash
make format
make lint
make typecheck
make test
make security
make check-all
```

## Project Areas

- `src/azure_functions_doctor/`: runtime code
- `src/azure_functions_doctor/assets/rules/v2.json`: built-in rules
- `src/azure_functions_doctor/schemas/rules.schema.json`: rules schema
- `tests/`: unit and integration tests
- `docs/`: MkDocs content
- `examples/v2/`: supported sample apps

## Workflow

1. Update runtime code or the v2 ruleset.
2. Add or update tests.
3. Run `make check-all`.
4. Use English for code comments, docs, and commit messages.
