# Handlers

This document describes the handler contract, built-in handlers, adapter-style patterns,
and tips for extending and testing handlers implemented in `src/azure_functions_doctor/handlers.py`.

## Purpose

Handlers connect rule definitions (`assets/rules/*.json`) to actual check logic. Rules are declarative
and handlers must follow this contract:

Handler contract (simplified)
- Input: `rule: dict` (full rule object), `path: pathlib.Path` (project root)
- Output: `bool` or `HandlerResult` (this project returns simple boolean/detail pairs)
- Failure mode: prefer returning `False` or logging details instead of raising exceptions

Handlers are registered in the `HandlerRegistry` and are mapped by the `type` field. Custom handlers
can be registered with the `@handler.register("your_type")` decorator.

---

## Built-in handlers overview

Below are the main handlers included in this repository with example rules. For full implementations,
see `src/azure_functions_doctor/handlers.py`.

1) compare_version
- Description: compare versions (e.g., Python or Core Tools).
- Example rule:
  ```json
  {"type": "compare_version", "target": "python", "operator": ">=", "value": "3.9"}
  ```

2) file_exists
- Description: check whether a file exists.
- Example rule:
  ```json
  {"type": "file_exists", "target": "host.json"}
  ```

3) file_contains
- Description: check whether a file contains a key or string (simple text or key path).

---

## v2 adapter/utility handlers

These lightweight handlers are used by the v2 rule set (`assets/rules/v2.json`). They intentionally
use simple heuristics to catch common configuration issues.

- executable_exists
  - Purpose: verify an executable is present on PATH (e.g., `func`).
  - Condition example: `{ "target": "func" }`

- any_of_exists
  - Purpose: pass if any item in `targets: [ ... ]` exists (supports env vars, `host.json:<jsonpath>`,
    or relative file paths).
  - Condition example: `{ "targets": ["requirements.txt", "Pipfile"] }`

- file_glob_check
  - Purpose: search for files using glob patterns. Useful for detecting sensitive files
    (e.g., `.env`, `.pem`) or artifacts.
  - Condition example: `{ "patterns": ["**/.env", "**/*.pem"] }`

- host_json_property
  - Purpose: check the existence or value of a simple key path inside `host.json`
    (e.g., `$.extensionBundle.id`).
  - Condition example: `{ "key": "$.extensionBundle" }`

- binding_validation
  - Purpose: lightweight validation of `function.json` bindings (e.g., ensure `httpTrigger`
    has `authLevel` and `methods`).
  - Goal: catch common typos or omissions without full schema validation.

- cron_validation
  - Purpose: heuristic checks for `timerTrigger` schedule strings (allowing 5- or 6-field cron).
  - Goal: detect common formatting errors (wrong field count, empty fields, etc.).

> Note: These handlers do not enforce full schemas. For strict validation, consider a custom handler
> using libraries like `croniter` or `jsonschema`.

---

## Adapter pattern guide

To reduce duplication and reuse logic across multiple rules, write adapter-style handlers. Core idea:

- Rule JSON defines only simple conditions (e.g., `targets`, `patterns`, `key`).
- Handlers parse different input shapes (env vars, file paths, host.json keys) and delegate to shared
  check functions.

Example: `any_of_exists` loops through targets and tries the following per entry:
- environment variable (`$ENV`)
- `host.json:<path>` parsing
- relative file existence check

Pass condition: any target is found.

---

## Writing custom handlers (quick example)

1. Add a new function in `src/azure_functions_doctor/handlers.py`.
2. Register the type with `@handler.register("my_custom")`.
3. Use `"type": "my_custom"` in the rule JSON.

Template:

```python
# src/azure_functions_doctor/handlers.py

@handler.register("my_custom")
def _handle_my_custom(rule: dict, path: pathlib.Path) -> bool:
    condition = rule.get("condition", {})
    # ... check logic ...
    return True  # or False
```

Example rule:
```json
{
  "id": "check_my_custom",
  "section": "custom",
  "label": "My custom check",
  "type": "my_custom",
  "condition": {"key": "value"},
  "hint": "Do X if missing"
}
```

---

## Testing and debugging tips

- Unit tests: add happy-path and failure cases in `tests/test_handler.py`.
- Logging: use `logging` in handlers to explain failures; useful in verbose CLI mode.
- Performance: for globbing or large scans, add filters to reduce search scope.

---

## Example rule

```json
{
  "id": "no_env_files",
  "section": "secrets",
  "label": ".env files present",
  "type": "file_glob_check",
  "condition": { "patterns": ["**/.env"] },
  "hint": "Remove secrets from repository or add to .gitignore"
}
```

---

## Extension ideas

- Stronger JSONPath support: integrate `jsonpath-ng` for complex host.json queries.
- Strict cron validation: validate expressions with `croniter`.
- Advanced binding checks: deep validation aligned with Azure Functions schemas.

---

For detailed API reference, see the `Handlers` section in `docs/api.md`.
