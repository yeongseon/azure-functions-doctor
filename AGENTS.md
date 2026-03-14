# AGENTS.md

## Purpose
`azure-functions-doctor` is a Python CLI that diagnoses common Azure Functions project issues.

## Read First
- `README.md`
- `CONTRIBUTING.md`
- `docs/agent-playbook.md`

## Working Rules
- Keep diagnostics deterministic and user-facing messages actionable.
- Prefer extending existing rule patterns over introducing one-off flows.
- If a CLI option or exit code changes, update docs and tests in the same change.
- Preserve Python 3.9+ compatibility declared in `pyproject.toml`.

## Validation
- `make test`
- `make lint`
- `make typecheck`
