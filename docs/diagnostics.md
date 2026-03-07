# Diagnostics Reference

Azure Functions Doctor ships with a built-in diagnostics set for the **Azure Functions Python v2 programming model**.

## Required Checks

| Check | Purpose |
| --- | --- |
| Programming model v2 | Detect decorator-based Azure Functions usage. |
| Python version | Ensure Python 3.10 or newer. |
| Virtual environment | Confirm local development is isolated. |
| Python executable | Confirm Python is available and resolvable. |
| `requirements.txt` | Ensure dependency declarations exist. |
| `azure-functions` package | Ensure the Functions library is declared. |
| `host.json` | Ensure the project includes host configuration. |

## Optional Checks

| Check | Purpose |
| --- | --- |
| `local.settings.json` | Flag missing local settings for development. |
| Azure Functions Core Tools | Recommend local tooling presence. |
| Core Tools version | Recommend Functions Core Tools v4+. |
| Durable Functions configuration | Validate `durableTask` when durable usage is detected. |
| Application Insights configuration | Detect telemetry configuration signals. |
| `extensionBundle` | Check host extension bundle configuration. |
| ASGI/WSGI compatibility | Detect framework callable exposure. |
| Unwanted files | Flag common junk files in project trees. |

## Status Mapping

- `pass`: check succeeded
- `warn`: optional check failed
- `fail`: required check failed
