# Azure Functions Doctor

Azure Functions Doctor validates local projects built on the **Azure Functions Python v2 programming model**.

Use it to catch common setup and configuration issues before running locally or shipping through CI.

It supports both CLI usage (`azure-functions doctor`) and programmatic usage
through `run_diagnostics(path, profile, rules_path)`.

## Features

- Validates Azure Functions Python v2 project signals (decorators, host files, dependencies).
- Differentiates required failures from optional warnings for clear gating.
- Supports output formats for humans and machines (`table`, `json`, `sarif`, `junit`).
- Allows custom rule files with schema validation.
- Supports profile-based execution (`full` and `minimal`).
- Produces deterministic grouped output by section and check order.

## Quick Start

```bash
pip install azure-functions-doctor
azure-functions doctor
```

Run against a specific project directory:

```bash
azure-functions doctor --path ./my-function-app
```

Run required checks only:

```bash
azure-functions doctor --profile minimal
```

Sample output:

```text
Section: Python Env (status: fail)
  - Programming model v2: pass
  - Python version: pass
  - requirements.txt: fail (required)

Section: Tooling (status: pass)
  - Azure Functions Core Tools (func): warn (optional)

Overall: 1 required failure, 1 warning
Exit code: 1
```

## How It Works

Execution pipeline:

```text
[CLI or API input]
        |
        v
[Doctor(path, profile, rules_path)]
        |
        v
[Load rules: custom or built-in v2.json]
        |
        v
[Validate against rules.schema.json]
        |
        v
[Dispatch each rule by type via HandlerRegistry]
        |
        v
[Aggregate by section + map optional failures to warn]
        |
        v
[Render output + return exit code/results]
```

Programmatic equivalent:

```python
from azure_functions_doctor.api import run_diagnostics


def run_and_print(path: str) -> None:
    sections = run_diagnostics(path=path, profile="full", rules_path=None)
    for section in sections:
        print(f"[{section['title']}] {section['status']}")
        for item in section["items"]:
            print(f"- {item['label']}: {item['status']} ({item['value']})")
```

## What it checks

- Python 3.10+
- v2 decorator usage
- `requirements.txt`
- `azure-functions`
- `host.json`
- optional local tooling and host configuration

See [Diagnostics Reference](diagnostics.md) for complete check definitions and behavior.

## When to Use

- Before first local run of a new Azure Functions Python v2 project.
- During migration from ad-hoc local setup to repeatable team setup.
- In CI to block merges on required runtime/configuration issues.
- In release pipelines to emit JSON/SARIF/JUnit diagnostics artifacts.
- During repository cleanup to detect deployment junk files and missing telemetry signals.

## API and CLI Entry Points

- CLI: `azure-functions doctor`
- Python API: `from azure_functions_doctor.api import run_diagnostics`

## Documentation

- [Usage Guide](usage.md)
- [Rules Reference](rules.md)
- [Rule Inventory](rule_inventory.md)
- [Minimal Profile](minimal_profile.md)
- [JSON Output Contract](json_output_contract.md)
- [Semver Policy](semver_policy.md)
- [Diagnostics Reference](diagnostics.md)
- [Supported Versions](supported_versions.md)
- [Development Guide](development.md)
- [Release Process](release_process.md)

## Examples

- [Representative example](https://github.com/yeongseon/azure-functions-doctor/blob/main/examples/v2/http-trigger/README.md)
- [Complex example](https://github.com/yeongseon/azure-functions-doctor/blob/main/examples/v2/multi-trigger/README.md)
