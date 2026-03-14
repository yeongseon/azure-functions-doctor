# Example: CI Integration

This example shows how to enforce required diagnostics in CI and publish rich artifacts.

## CI goal

- Fail builds on required issues
- Keep logs readable
- Preserve machine-readable reports for triage

Recommended command:

```bash
azure-functions doctor --profile minimal --format json --output doctor.json
```

Why this works:

- `minimal` keeps scope to required checks only
- `json` provides parser-safe structure
- process exit code is gate signal (`0` pass, `1` fail)

## GitHub Actions workflow

```yaml
name: Doctor Check

on:
  pull_request:
  push:
    branches: [main]

jobs:
  doctor:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install package
        run: |
          python -m pip install --upgrade pip
          python -m pip install azure-functions-doctor

      - name: Run doctor (required checks)
        run: |
          azure-functions doctor \
            --profile minimal \
            --format json \
            --output doctor.json

      - name: Upload doctor artifact
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: doctor-report
          path: doctor.json
```

## Exit code behavior in CI

The doctor exits non-zero when required checks fail.

- Exit `0`: job continues
- Exit `1`: step fails immediately unless explicitly tolerated

If you want to always upload artifacts before failing, split gate and report steps.

## Pattern: always upload + explicit gate

```yaml
      - name: Run doctor and capture status
        id: doctor
        run: |
          set +e
          azure-functions doctor --profile minimal --format json --output doctor.json
          echo "exit_code=$?" >> "$GITHUB_OUTPUT"

      - name: Upload doctor artifact
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: doctor-report
          path: doctor.json

      - name: Fail job when doctor failed
        if: steps.doctor.outputs.exit_code != '0'
        run: exit 1
```

## Parse JSON to produce summary

### Python parser snippet

```python
import json
from pathlib import Path


def summarize(path: str) -> tuple[int, int, int]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    passed = warned = failed = 0
    for section in payload["results"]:
        for item in section["items"]:
            if item["status"] == "pass":
                passed += 1
            elif item["status"] == "warn":
                warned += 1
            elif item["status"] == "fail":
                failed += 1
    return passed, warned, failed
```

### `jq` parser snippet

```bash
fails=$(jq '[.results[].items[] | select(.status=="fail")] | length' doctor.json)
warns=$(jq '[.results[].items[] | select(.status=="warn")] | length' doctor.json)
passes=$(jq '[.results[].items[] | select(.status=="pass")] | length' doctor.json)
echo "doctor: $fails fails, $warns warnings, $passes passed"
```

## Fail only on required failures

You usually do not need custom logic because exit codes already represent required failures.

Still, explicit JSON-based checks can be useful for custom messaging:

```bash
required_failures=$(jq '[.results[].items[] | select(.status=="fail")] | length' doctor.json)
if [ "$required_failures" -gt 0 ]; then
  echo "Required diagnostics failed: $required_failures"
  exit 1
fi
```

## Multi-format publishing

For richer ecosystem integration, emit multiple formats in separate steps:

```bash
azure-functions doctor --profile minimal --format json --output doctor.json
azure-functions doctor --profile minimal --format sarif --output doctor.sarif
azure-functions doctor --profile minimal --format junit --output doctor-junit.xml
```

Then upload artifacts for each format.

## Security guidance for CI usage

- Do not execute untrusted custom rules files from forked PRs
- Keep path target explicit in monorepos (`--path`)
- Store artifacts for failed runs to speed triage

## Monorepo pattern

Run one job per function project:

```yaml
strategy:
  matrix:
    app_path:
      - apps/orders-function
      - apps/payments-function

steps:
  - run: azure-functions doctor --path ${{ matrix.app_path }} --profile minimal --format json --output doctor-${{ matrix.app_path }}.json
```

## Common CI pitfalls

- Running in wrong working directory
- Forgetting to install project dependencies before checks
- Treating warnings as failures without clear team policy
- Parsing display-only fields instead of status fields

## Related docs

- [Configuration](../configuration.md)
- [JSON Output Contract](../json_output_contract.md)
- [Minimal Profile](../minimal_profile.md)
- [Troubleshooting](../troubleshooting.md)
