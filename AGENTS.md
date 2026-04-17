# AGENTS.md

## Purpose
`azure-functions-doctor-python` is a Python CLI that diagnoses common Azure Functions project issues.

## Read First
- `README.md`
- `CONTRIBUTING.md`
- `docs/agent-playbook.md`

## Working Rules
- Keep diagnostics deterministic and user-facing messages actionable.
- Prefer extending existing rule patterns over introducing one-off flows.
- If a CLI option or exit code changes, update docs and tests in the same change.
- Preserve Python 3.10+ compatibility declared in `pyproject.toml`.

## Validation
- `make test`
- `make lint`
- `make typecheck`
- `make build`

## Release Process
- Version is managed via `hatch` (dynamic from `src/azure_functions_doctor/__init__.py`).
- **Do NOT manually edit version strings.** Use the Makefile targets below.
- When bumping version, update `tests/test_public_api.py` to match the new version string.

### Commands
- `make release-patch` — bump patch version, update changelog, tag, and push
- `make release-minor` — bump minor version, update changelog, tag, and push
- `make release-major` — bump major version, update changelog, tag, and push
- `make release VERSION=x.y.z` — set explicit version, update changelog, tag, and push
- `make tag-release VERSION=x.y.z` — create and push an annotated tag (used internally by release targets)

### Flow
1. `make release-patch` (or `-minor` / `-major`) on `main`
2. This runs: `hatch version` → `git commit` → `make changelog` → `git commit` → `git tag` → `git push`
3. Tag push triggers **Publish to PyPI** GitHub Actions workflow automatically.
4. Update `docs/changelog.md` separately if needed (different format from `CHANGELOG.md`).
