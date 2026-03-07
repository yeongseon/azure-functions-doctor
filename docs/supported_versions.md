# Supported Versions

## Python

Azure Functions Doctor supports **Python 3.10 and above**.

- Minimum supported version: 3.10
- Targeted versions: 3.10, 3.11, 3.12, 3.13, 3.14

## Azure Functions Model

Azure Functions Doctor supports the **Azure Functions Python v2 programming model** only.

- Supported: `func.FunctionApp()` and decorator-based triggers
- Not supported: legacy `function.json`-based Python v1 projects

## Maintenance Policy

When the supported baseline changes, update:

- `pyproject.toml`
- `src/azure_functions_doctor/assets/rules/v2.json`
- CI matrices
- this document and the main README
