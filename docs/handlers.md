# Handlers

Handlers execute rule definitions from `src/azure_functions_doctor/assets/rules/v2.json`.

Each rule has a `type`, and `HandlerRegistry` routes the rule to the corresponding
handler implementation in `src/azure_functions_doctor/handlers.py`.

## Contract

- Input: `rule` and project `path`
- Output: a dictionary with `status` and `detail`
- Status values: `pass` or `fail`

Optional rules are converted to `warn` later in the aggregation layer.

### Rule Input Contract

Rules are JSON objects validated by the schema in
`src/azure_functions_doctor/schemas/rules.schema.json`.
The minimum practical structure for handler execution is:

```json
{
  "id": "check_example",
  "type": "file_exists",
  "label": "host.json",
  "required": true,
  "condition": {
    "target": "host.json"
  }
}
```

### Handler Output Contract

Handlers return a normalized dictionary:

| Key | Type | Meaning |
| --- | --- | --- |
| `status` | `"pass"` or `"fail"` | Raw check result before optional-to-warn mapping. |
| `detail` | `str` | Human-readable diagnostic detail used in reports. |
| `internal_error` | `"true"` (optional) | Present when an internal exception is captured. |

## HandlerRegistry Pattern

`HandlerRegistry` centralizes dispatch so each rule type maps to one method.
This keeps `Doctor` focused on orchestration while handlers focus on evaluation.

Dispatch flow:

1. `Doctor.run_all_checks()` passes each rule to `generic_handler(rule, path)`.
2. `generic_handler` forwards execution to a global `HandlerRegistry` instance.
3. `HandlerRegistry.handle()` resolves `rule["type"]`.
4. A concrete `_handle_*` method returns `{"status": ..., "detail": ...}`.
5. `Doctor` maps optional failures to `warn` and builds section results.

## Built-in Handlers

- `compare_version`
- `file_exists`
- `env_var_exists`
- `path_exists`
- `package_installed`
- `package_declared`
- `source_code_contains`
- `conditional_exists`
- `callable_detection`
- `executable_exists`
- `any_of_exists`
- `file_glob_check`
- `host_json_property`

### Handler Reference

| Handler Type | Condition Keys | Typical Use |
| --- | --- | --- |
| `compare_version` | `target`, `operator`, `value` | Python version and Core Tools version checks. |
| `env_var_exists` | `target` | Environment variable presence checks. |
| `path_exists` | `target` | Check concrete paths or `sys.executable`. |
| `file_exists` | `target` | Required project files (`host.json`, `requirements.txt`). |
| `package_installed` | `target` | Validate importable module availability. |
| `package_declared` | `package`, optional `file` | Confirm package declaration in dependency file. |
| `source_code_contains` | `keyword`, optional `mode` | Detect decorators or source signals. |
| `conditional_exists` | `jsonpath` | Conditional host checks (for example Durable settings). |
| `callable_detection` | none | Detect ASGI/WSGI callable exposure patterns. |
| `executable_exists` | `target` | Ensure local binaries exist on `PATH`. |
| `any_of_exists` | `targets` | Pass when any env/file/host signal is present. |
| `file_glob_check` | `patterns` | Detect junk files and deployment artifacts. |
| `host_json_property` | `jsonpath` | Validate specific host.json properties. |

## Example Rule JSON by Handler Type

```json
[
  {
    "id": "python_min",
    "type": "compare_version",
    "condition": {"target": "python", "operator": ">=", "value": "3.10"}
  },
  {
    "id": "venv_active",
    "type": "env_var_exists",
    "condition": {"target": "VIRTUAL_ENV"}
  },
  {
    "id": "python_path",
    "type": "path_exists",
    "condition": {"target": "sys.executable"}
  },
  {
    "id": "host_file",
    "type": "file_exists",
    "condition": {"target": "host.json"}
  },
  {
    "id": "module_installed",
    "type": "package_installed",
    "condition": {"target": "azure.functions"}
  },
  {
    "id": "package_declared",
    "type": "package_declared",
    "condition": {"package": "azure-functions", "file": "requirements.txt"}
  },
  {
    "id": "decorator_signal",
    "type": "source_code_contains",
    "condition": {"keyword": "@app.", "mode": "ast"}
  },
  {
    "id": "durable_host",
    "type": "conditional_exists",
    "condition": {"jsonpath": "$.extensions.durableTask"}
  },
  {
    "id": "asgi_wsgi",
    "type": "callable_detection",
    "condition": {}
  },
  {
    "id": "func_cli",
    "type": "executable_exists",
    "condition": {"target": "func"}
  },
  {
    "id": "telemetry_any",
    "type": "any_of_exists",
    "condition": {
      "targets": [
        "APPLICATIONINSIGHTS_CONNECTION_STRING",
        "APPINSIGHTS_INSTRUMENTATIONKEY",
        "host.json:instrumentationKey"
      ]
    }
  },
  {
    "id": "junk_files",
    "type": "file_glob_check",
    "condition": {"patterns": ["**/*.pyc", "**/__pycache__"]}
  },
  {
    "id": "extension_bundle",
    "type": "host_json_property",
    "condition": {"jsonpath": "$.extensionBundle"}
  }
]
```

## Notes

- `source_code_contains` supports a simple string mode and an AST-based mode.
- `conditional_exists` is used for checks that only matter when a related feature is detected.
- Handler implementations live in `src/azure_functions_doctor/handlers.py`.

## Programmatic Usage Examples

### Execute One Rule Through `HandlerRegistry`

```python
from pathlib import Path

from azure_functions_doctor.handlers import HandlerRegistry


def run_host_check(project_path: str) -> dict[str, str]:
    registry = HandlerRegistry()
    rule = {
        "id": "host_file",
        "type": "file_exists",
        "label": "host.json",
        "required": True,
        "condition": {"target": "host.json"},
    }
    return registry.handle(rule=rule, path=Path(project_path))
```

### Register a Custom Handler in a Subclass

```python
from pathlib import Path

from azure_functions_doctor.handlers import HandlerRegistry


class ExtendedRegistry(HandlerRegistry):
    def __init__(self) -> None:
        super().__init__()
        self._handlers["always_pass"] = self._handle_always_pass

    def _handle_always_pass(self, rule: dict, path: Path) -> dict[str, str]:
        _ = (rule, path)
        return {"status": "pass", "detail": "Custom handler executed"}


def run_custom_rule(project_path: str) -> dict[str, str]:
    registry = ExtendedRegistry()
    custom_rule = {
        "id": "custom_demo",
        "type": "always_pass",
        "condition": {},
    }
    return registry.handle(custom_rule, Path(project_path))
```

## Development

When adding a new handler:

1. Extend the `Rule["type"]` literal
2. Register the handler in `HandlerRegistry`
3. Update `rules.schema.json`
4. Add tests in `tests/test_handler.py`
