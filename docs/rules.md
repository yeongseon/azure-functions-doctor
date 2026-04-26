# Rules

Azure Functions Doctor executes declarative rules from a JSON ruleset.

Built-in rules are defined in:

`src/azure_functions_doctor/assets/rules/v2.json`

You can replace the built-in set with `--rules <file>`.

## Rule execution model

Each rule contains:

- identity (`id`, `label`)
- grouping (`category`, `section`)
- behavior (`type`, `condition`)
- severity intent (`required`)
- ordering (`check_order`)
- remediation (`hint`, optional `hint_url`)

Rules are validated by:

`src/azure_functions_doctor/schemas/rules.schema.json`

## Required vs optional

- `required: true` + raw handler fail -> item status `fail`
- `required: false` + raw handler fail -> item status `warn`

Only required failures produce non-zero process exit code.

## Built-in rule types

- `compare_version`
- `env_var_exists`
- `path_exists`
- `file_exists`
- `package_installed`
- `package_declared`
- `source_code_contains`
- `conditional_exists`
- `callable_detection`
- `executable_exists`
- `any_of_exists`
- `file_glob_check`
- `host_json_property`
- `blueprint_registration`

## Rule-by-rule reference

## 1) `check_programming_model_v2`

- **What it checks:** Source contains Azure Functions decorator usage (`@app.`) via AST detection.
- **Why it matters:** Doctor targets Python v2 projects; this check protects model compatibility.
- **How to fix:** Use `func.FunctionApp()` and decorator-based triggers.

Example failing detail:

```text
Keyword '@app.' not found in source code (AST)
```

## 2) `check_blueprint_registration`

- **What it checks:** Blueprint aliases declared with `func.Blueprint()` and used in decorators are also registered via `app.register_functions(bp)` somewhere in the project. Only the official Azure Functions Python v2 API is recognized; Flask/FastAPI-style `register_blueprint(...)` calls are not treated as registration.
- **Why it matters:** Unregistered Blueprints look valid in code but their routes never index at runtime.
- **How to fix:** Register each Blueprint on your `FunctionApp`, typically from `function_app.py`.

Example warning detail:

```text
Detected:
- bp = func.Blueprint()
- @bp.route(...)

Missing:
- app.register_functions(bp)

Fix: add `app.register_functions(bp)` in function_app.py.
```

## 3) `check_python_version`

- **What it checks:** Python version evaluated for the app target is `>=3.10`.
- **Why it matters:** Azure Functions Python runtime compatibility depends on the deployed target version, not just the interpreter running the doctor.
- **How to fix:** Use Python 3.10+ locally and in CI, or pass `--target-python <3.10|3.11|3.12|3.13|3.14>` when your deploy target differs from the tool runtime. Note that on the Linux Consumption plan the maximum supported runtime is Python 3.12.

Example output:

```text
Python 3.9.18 (tool runtime, >=3.10)
```

With override:

```text
Target Python: 3.12 (override) — Tool runtime: 3.13.0
```

## 4) `check_venv`

- **What it checks:** Environment variable `VIRTUAL_ENV` exists.
- **Why it matters:** Virtual environments reduce dependency drift and environment pollution.
- **How to fix:** Create and activate `.venv` before running diagnostics.

Example failing detail:

```text
VIRTUAL_ENV is not set
```

## 5) `check_python_executable`

- **What it checks:** `sys.executable` points to an existing path.
- **Why it matters:** Broken interpreter paths indicate unstable runtime environment.
- **How to fix:** Reinstall or reactivate Python environment.

Example detail:

```text
/usr/bin/python3 exists
```

## 6) `check_requirements_txt`

- **What it checks:** `requirements.txt` exists at project root.
- **Why it matters:** Deployability and reproducibility depend on declared dependencies.
- **How to fix:** Add `requirements.txt` and include runtime dependencies.

Example failing detail:

```text
/workspace/app/requirements.txt not found
```

## 7) `check_azure_functions_library`

- **What it checks:** `azure-functions` appears in `requirements.txt`.
- **Why it matters:** Function app code depends on Azure Functions Python library.
- **How to fix:** Add `azure-functions` to dependency declarations.

Example failing detail:

```text
Package 'azure-functions' not declared in requirements.txt
```

## 8) `check_host_json`

- **What it checks:** `host.json` exists at project root.
- **Why it matters:** Azure Functions host configuration is required for valid app structure.
- **How to fix:** Add a valid `host.json` (at minimum `{ "version": "2.0" }`).

Example failing detail:

```text
/workspace/app/host.json not found
```

## 9) `check_local_settings`

- **What it checks:** `local.settings.json` exists.
- **Why it matters:** Local development often needs this file for settings and connection values.
- **How to fix:** Create local settings file for local runs (do not commit secrets).

Example warning detail:

```text
/workspace/app/local.settings.json not found (optional)
```

## 10) `check_func_cli`

- **What it checks:** `func` executable is available on `PATH`.
- **Why it matters:** Core Tools enable local hosting and rich runtime tooling.
- **How to fix:** Install Azure Functions Core Tools v4+.

Example warning detail:

```text
func not found
```

## 11) `check_func_core_tools_version`

- **What it checks:** Core Tools version is `>=4.0`.
- **Why it matters:** Older versions can diverge from current host/runtime expectations.
- **How to fix:** Upgrade Core Tools installation.

Example warning detail:

```text
func 3.0.3904 (>=4.0)
```

## 12) `check_durabletask_config`

- **What it checks:** If durable usage is detected in source, `$.extensions.durableTask` exists in `host.json`.
- **Why it matters:** Durable Functions need matching host configuration.
- **How to fix:** Add durableTask configuration when using durable features.

Example details:

```text
No Durable Functions usage detected; check skipped
```

or

```text
Required host.json property '$.extensions.durableTask' not found
```

## 13) `check_app_insights`

- **What it checks:** At least one telemetry signal exists:
  - `APPLICATIONINSIGHTS_CONNECTION_STRING`
  - `APPINSIGHTS_INSTRUMENTATIONKEY`
  - `host.json:instrumentationKey`
- **Why it matters:** Telemetry is critical for production diagnostics.
- **How to fix:** Configure one supported telemetry source.

Example warning detail:

```text
Targets not found
```

## 14) `check_extension_bundle`

- **What it checks:** `$.extensionBundle` exists in `host.json`.
- **Why it matters:** Extension bundles help ensure binding dependencies are available.
- **How to fix:** Add extensionBundle section to host config.

Example warning detail:

```text
host.json property '$.extensionBundle' not found
```

## 15) `check_asgi_wsgi_exposure`

- **What it checks:** Source has ASGI/WSGI exposure patterns.
- **Why it matters:** Useful signal for framework-host integration readiness.
- **How to fix:** Ensure framework callable exposure follows expected patterns.

Example warning detail:

```text
No ASGI/WSGI callable detected in project source
```

## 16) `check_unused_files`

- **What it checks:** Presence of unwanted patterns (for example `**/*.pyc`, `**/__pycache__`, `.venv`, `tests/`).
- **Why it matters:** Reduces deployment package clutter and risk.
- **How to fix:** Clean or exclude unwanted files from deployment artifacts.

Example warning detail:

```text
Found unwanted files: ['tests/', '.venv']
```

## Rule authoring template

```json
{
  "id": "check_example",
  "category": "structure",
  "section": "project_structure",
  "label": "host.json",
  "description": "Checks host.json exists.",
  "type": "file_exists",
  "required": true,
  "condition": {
    "target": "host.json"
  },
  "hint": "Add host.json to project root.",
  "check_order": 10
}
```

## Guidance for custom rules

- Keep IDs stable and descriptive
- Use deterministic `check_order` values
- Start policy experiments as optional rules
- Promote to required only after false-positive review
- Include clear `hint` text for faster remediation

Custom rules docs: [Examples: Custom Rules](examples/custom_rules.md)

## Safety and trust model

Rules may inspect local files, source code, environment variables, executable presence, and importable modules.

!!! warning
    Only run trusted custom rules files, especially in shared CI environments.

## Related docs

- [Diagnostics](diagnostics.md)
- [Rule Inventory](rule_inventory.md)
- [Minimal Profile](minimal_profile.md)
- [Semver Policy](semver_policy.md)
