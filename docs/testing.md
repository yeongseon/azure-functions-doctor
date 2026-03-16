# Testing

## Overview
Azure Functions Doctor uses pytest as its primary testing framework. The test suite consists of 15 files with approximately 1,830 lines of code. These tests provide coverage for the CLI, diagnostic handlers, rule registration, configuration management, and error handling.

## Running Tests
You can execute the tests using the provided Makefile or by calling pytest directly.

```bash
make test                                  # Run all tests
make cov                                   # Run with coverage (terminal, HTML, and XML reports)
python -m pytest tests/test_handler.py -v  # Run a specific test file
```

## Test Structure
The codebase follows a modular test structure to ensure specific components are isolated and verified correctly.

| File | Lines | Description |
|------|-------|-------------|
| test_handler.py | 377 | Individual check handler implementations |
| test_error_handling.py | 244 | Error handling and edge cases |
| test_handler_registry.py | 214 | Handler dispatch and registration |
| test_config.py | 155 | Configuration loading and validation |
| test_programming_model_detection.py | 137 | v1 vs v2 model detection |
| test_doctor.py | 130 | Core diagnostic engine |
| test_rule_loading.py | 121 | Rule JSON loading and validation |
| test_logging_config.py | 106 | Logging configuration |
| test_cli.py | 104 | CLI command tests |
| test_rules_schema.py | 77 | Rules schema consistency |
| test_target_resolver.py | 77 | Version resolution utilities |
| test_api.py | 40 | Public API surface |
| test_examples.py | 29 | Example project smoke tests |
| test_utils.py | 19 | Utility function tests |

## Test Patterns

### Handler Tests (test_handler.py)
These tests verify individual diagnostic check handlers. They use the `tmp_path` fixture to create isolated filesystem environments. Testing covers various outcomes including pass, warn, fail, and skip.

Specific handlers tested include:
- file_exists and path_exists
- package_declared
- source_code_contains
- executable_exists
- compare_version
- conditional_exists
- callable_detection

### CLI Tests (test_cli.py)
CLI tests use Typer's CliRunner to invoke commands and verify output. They ensure the `doctor` subcommand behaves correctly with different flags such as `--format json`, `--profile minimal`, and `--path`. Exit codes are verified to be 0 for successful checks and 1 when failures occur.

### Rules Tests
- **test_rule_loading.py**: Validates the loading of v1.json and v2.json rule files.
- **test_rules_schema.py**: Ensures rule JSON files adhere to the defined schema.
- Custom rules: Verifies that the `--rules` flag correctly loads external rule files.

### Error Handling (test_error_handling.py)
These tests confirm that the system handles failures gracefully. They check handler failures, exception recovery, and context logging to ensure the application doesn't crash during unexpected diagnostic errors.

### Example Smoke Tests (test_examples.py)
Lightweight smoke tests validate that the projects in the `examples/` directory remain runnable. This provides a baseline level of end-to-end verification without the overhead of full infrastructure tests.

## Coverage Configuration
Coverage settings are defined in `pyproject.toml`.
- **Source**: src/azure_functions_doctor
- **Branch coverage**: Enabled
- **Reports**: Terminal (missing lines), HTML, and XML
- **pytest options**: `--cov=src/azure_functions_doctor --cov-report=xml --cov-report=term-missing -ra -q`

## Writing New Tests
When contributing new features or bug fixes, follow these guidelines:

1. Place handler tests in `test_handler.py` using the `tmp_path` fixture.
2. Place CLI tests in `test_cli.py` using `CliRunner`.
3. Use descriptive test names following the pattern: `test_<handler>_returns_<status>_when_<condition>`.
4. Ensure all result statuses (pass, warn, fail, skip) are covered.
5. Mock external dependencies like the filesystem, executables, or network calls.
6. If adding new diagnostic rules, include corresponding handler tests.

## CI Test Matrix
The test suite runs automatically on GitHub Actions with the following configuration:
- **OS**: ubuntu-latest
- **Python Versions**: 3.10, 3.11, 3.12, 3.13, 3.14
- **Workflow**: .github/workflows/ci-test.yml

## Real Azure E2E Tests

The project includes a real Azure end-to-end test workflow that deploys an actual Function App to Azure and validates HTTP endpoints.

### Workflow

- **File**: `.github/workflows/e2e-azure.yml`
- **Trigger**: Manual (`workflow_dispatch`) or weekly schedule (Mondays 02:00 UTC)
- **Infrastructure**: Azure Consumption plan, `koreacentral` region
- **Cleanup**: Resource group deleted immediately after tests (`if: always()`)

### Running E2E Tests

```bash
gh workflow run e2e-azure.yml --ref main
```

### Required Secrets & Variables

| Name | Type | Description |
| --- | --- | --- |
| `AZURE_CLIENT_ID` | Secret | App Registration Client ID (OIDC) |
| `AZURE_TENANT_ID` | Secret | Azure Tenant ID |
| `AZURE_SUBSCRIPTION_ID` | Secret | Azure Subscription ID |
| `AZURE_LOCATION` | Variable | Azure region (default: `koreacentral`) |

### Test Report

HTML test report is uploaded as a GitHub Actions artifact (retained 30 days).
