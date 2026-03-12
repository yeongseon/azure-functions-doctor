# Minimal Profile

The `--profile minimal` flag provides a low-noise CI baseline by running only the rules required for a functioning Azure Functions Python v2 application.

## Core Purpose

The minimal profile focuses on the critical path. While the full doctor check (default or `--profile full`) runs 15 checks including optional items like telemetry or unused files, the minimal profile runs only the required rules (currently 7).

## Required Rules

The minimal profile includes:

1. `check_programming_model_v2`: Confirm decorator-based v2 model.
2. `check_python_version`: Ensure Python 3.10 or higher.
3. `check_venv`: Confirm active virtual environment.
4. `check_python_executable`: Verify Python path.
5. `check_requirements_txt`: Ensure requirements.txt exists.
6. `check_azure_functions_library`: Confirm azure-functions package declaration.
7. `check_host_json`: Ensure host.json exists.

## Rule Inclusion Criteria

A rule is included in the minimal profile if it is marked as `required: true` in the `v2.json` ruleset. Adding a new required rule to the minimal profile is a breaking change and requires a major version release.

## Usage

For local low-noise checks:

```bash
azure-functions doctor --profile minimal
```

For automated CI/CD pipelines:

```bash
azure-functions doctor --profile minimal --format json
```
