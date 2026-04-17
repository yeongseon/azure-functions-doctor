# Azure Functions Doctor - Complete Codebase Analysis

**Generated:** 2026-03-15  
**Purpose:** Complete codebase inventory for gap analysis against design specification

---

## 1. PROJECT OVERVIEW

### Identity
- **Name:** azure-functions-doctor-python
- **Version:** 0.15.1
- **Type:** Python CLI diagnostic tool
- **Target:** Azure Functions Python v2 programming model (decorator-based)
- **Python Support:** 3.10, 3.11, 3.12, 3.13, 3.14

### Core Purpose
Pre-deployment health gate that catches configuration issues, missing dependencies, and environment problems **before** they cause runtime failures in production.

### CLI Entry Points
- `azure-functions doctor`
- `azure-functions-doctor-python doctor`
- `fdoctor doctor`

### Key Dependencies
- `jsonschema` - Rule validation
- `packaging` - Version comparison
- `rich` - Terminal output formatting
- `typer` - CLI framework

---

## 2. DIRECTORY STRUCTURE

```
src/azure_functions_doctor/
├── __init__.py                 # Version: 0.15.1
├── api.py                      # Public API entry point
├── cli.py                      # CLI entry point (typer)
├── config.py                   # Configuration management (env vars)
├── doctor.py                   # Core diagnostic runner
├── handlers.py                 # Rule handler registry (722 lines)
├── logging_config.py           # Centralized logging
├── target_resolver.py          # Version/target resolution
├── utils.py                    # Output formatting utilities
├── assets/
│   ├── __init__.py
│   └── rules/
│       └── v2.json             # Built-in ruleset (19 rules)
└── schemas/
    ├── __init__.py
    └── rules.schema.json       # JSON Schema for rule validation

tests/
├── test_api.py                 # API tests (2 tests)
├── test_cli.py                 # CLI output format tests (5 tests)
├── test_config.py              # Configuration tests (13 tests)
├── test_doctor.py              # Doctor core tests (6 tests)
├── test_error_handling.py      # Error handling tests
├── test_examples.py            # Smoke tests for bundled examples
├── test_handler.py             # Handler tests (44 tests)
├── test_handler_registry.py    # Registry tests
├── test_logging_config.py      # Logging tests
├── test_programming_model_detection.py
├── test_rule_loading.py        # Rule loading/validation tests
├── test_rules_schema.py        # Schema validation tests
├── test_target_resolver.py     # Target resolution tests
└── test_utils.py               # Utility tests

examples/v2/
├── http-trigger/               # Passing example
├── timer-trigger/              # Passing example
├── multi-trigger/              # Passing example
├── blueprint/                  # Passing example (Blueprint pattern)
├── broken-missing-host-json/   # Broken example
├── broken-missing-requirements/ # Broken example
├── broken-missing-azure-functions/ # Broken example
└── broken-no-v2-decorators/    # Broken example

docs/
├── index.md
├── usage.md
├── rules.md
├── rule_inventory.md           # Authoritative rule reference
├── diagnostics.md
├── configuration.md
├── development.md
├── testing.md
├── api.md
├── handlers.md
├── json_output_contract.md
├── minimal_profile.md
├── examples/
│   ├── basic_check.md
│   ├── ci_integration.md
│   └── custom_rules.md
└── ...
```

---

## 3. COMPLETE CHECK INVENTORY (19 Built-in Checks)

All checks are defined in: `src/azure_functions_doctor/assets/rules/v2.json`

### CHECK BREAKDOWN BY REQUIREMENT LEVEL

**REQUIRED Checks (7)** - Exit code 1 on failure
1. `check_python_version` - Python >=3.10
2. `check_requirements_txt` - requirements.txt exists
3. `check_azure_functions_library` - azure-functions declared in requirements.txt
4. `check_host_json` - host.json exists
5. `check_host_json_version` - host.json has "version": "2.0"

**OPTIONAL Checks (14)** - Warning on failure, exit code 0
6. `check_programming_model_v2` - @app. or @bp. decorators detected (AST)
7. `check_venv` - Virtual environment activated (VIRTUAL_ENV, CONDA_PREFIX, UV_PROJECT_ENVIRONMENT)
8. `check_python_executable` - sys.executable path exists
9. `check_azure_functions_worker` - azure-functions-worker NOT in requirements.txt (forbidden)
10. `check_local_settings` - local.settings.json exists
11. `check_func_cli` - func executable on PATH
12. `check_func_core_tools_version` - func >=4.0
13. `check_durabletask_config` - $.extensions.durableTask in host.json (conditional on durable usage)
14. `check_app_insights` - APPLICATIONINSIGHTS_CONNECTION_STRING or APPINSIGHTS_INSTRUMENTATIONKEY or host.json:instrumentationKey
15. `check_extension_bundle` - $.extensionBundle in host.json
16. `check_asgi_wsgi_exposure` - ASGI/WSGI callable patterns detected
17. `check_unused_files` - Unwanted files detected (__pycache__, *.pyc, .venv, tests/)
18. `check_funcignore` - .funcignore exists
19. `check_local_settings_git_tracked` - local.settings.json NOT tracked by git
20. `check_extension_bundle_v4` - extensionBundle uses [4.*, 5.0.0) range

---

## 4. DETAILED CHECK SPECIFICATIONS

### Check 1: `check_programming_model_v2`
- **ID:** `check_programming_model_v2`
- **Label:** "Programming model v2"
- **Type:** `source_code_contains`
- **Required:** `false` (optional)
- **Condition:**
  ```json
  {
    "keyword": "@app.|@bp.",
    "mode": "ast"
  }
  ```
- **Category:** `project_structure`
- **Section:** `programming_model`
- **Check Order:** 0
- **What it tests:** Uses AST parsing to detect `@app.*` or `@bp.*` decorators (supports both standard FunctionApp and Blueprint patterns)
- **Pass condition:** At least one Python file contains decorator usage
- **Fail message:** "Keyword '@app.|@bp.' not found in source code (AST)"
- **Hint:** "Use func.FunctionApp() and decorator-based triggers such as @app.route()."
- **Hint URL:** https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python?pivots=python-mode-decorators

### Check 2: `check_python_version`
- **ID:** `check_python_version`
- **Label:** "Python version"
- **Type:** `compare_version`
- **Required:** `true`
- **Condition:**
  ```json
  {
    "target": "python",
    "operator": ">=",
    "value": "3.10"
  }
  ```
- **Category:** `environment`
- **Section:** `python_env`
- **Check Order:** 1
- **What it tests:** sys.version_info against minimum version
- **Pass detail:** "Python 3.10.x (>=3.10)"
- **Fail detail:** "Python 3.9.x (>=3.10)"
- **Source Type:** `ms_learn`
- **Source URL:** https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python#supported-python-versions
- **Why it matters:** "Azure Functions only supports Python 3.10+ for v2. Running an older interpreter causes immediate deployment failures and unsupported runtime errors."
- **Symptoms:** "Deployment fails with 'Python version not supported'; functions fail to start; 3.9 or earlier behaviours may cause silent type mismatches."
- **Fix Command:** `pyenv install 3.10.16`

### Check 3: `check_venv`
- **ID:** `check_venv`
- **Label:** "Virtual environment"
- **Type:** `any_of_exists`
- **Required:** `false`
- **Condition:**
  ```json
  {
    "targets": [
      "VIRTUAL_ENV",
      "CONDA_PREFIX",
      "UV_PROJECT_ENVIRONMENT"
    ]
  }
  ```
- **Category:** `environment`
- **Section:** `python_env`
- **Check Order:** 2
- **What it tests:** Checks if any of the three venv-related env vars are set
- **Pass detail:** "env:VIRTUAL_ENV set"
- **Fail detail:** "Targets not found"

### Check 4: `check_python_executable`
- **ID:** `check_python_executable`
- **Label:** "Python executable"
- **Type:** `path_exists`
- **Required:** `false`
- **Condition:**
  ```json
  {
    "target": "sys.executable"
  }
  ```
- **Category:** `environment`
- **Section:** `python_env`
- **Check Order:** 3
- **What it tests:** sys.executable path exists on filesystem
- **Pass detail:** "/usr/bin/python3.10 exists"
- **Fail detail:** "sys.executable is empty" or path missing

### Check 5: `check_requirements_txt`
- **ID:** `check_requirements_txt`
- **Label:** "requirements.txt"
- **Type:** `file_exists`
- **Required:** `true`
- **Condition:**
  ```json
  {
    "target": "requirements.txt"
  }
  ```
- **Category:** `dependencies`
- **Section:** `python_env`
- **Check Order:** 4
- **What it tests:** requirements.txt exists at project root
- **Pass detail:** "/path/to/requirements.txt exists"
- **Fail detail:** "/path/to/requirements.txt not found"
- **Source Type:** `ms_learn`
- **Source URL:** https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python#managing-dependencies
- **Why it matters:** "Azure Functions reads requirements.txt to install packages at deployment time. Without it, the runtime cannot resolve dependencies and the function app will fail to start."
- **Symptoms:** "ModuleNotFoundError at runtime; deployment pipeline fails with missing package errors; cold start crashes."
- **Fix Command:** `pip freeze > requirements.txt`

### Check 6: `check_azure_functions_library`
- **ID:** `check_azure_functions_library`
- **Label:** "azure-functions package"
- **Type:** `package_declared`
- **Required:** `true`
- **Condition:**
  ```json
  {
    "package": "azure-functions",
    "file": "requirements.txt"
  }
  ```
- **Category:** `dependencies`
- **Section:** `python_env`
- **Check Order:** 5
- **What it tests:** Parses requirements.txt and checks if "azure-functions" appears (normalized, case-insensitive, split on =<>!~)
- **Pass detail:** "Package 'azure-functions' declared in requirements.txt"
- **Fail detail:** "Package 'azure-functions' not declared in requirements.txt"
- **Source Type:** `ms_learn`
- **Source URL:** https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python
- **Why it matters:** "The azure-functions SDK is the binding between user code and the Functions host. Without it, triggers and bindings cannot be parsed and the app will not start."
- **Symptoms:** "ImportError for azure.functions; function app fails to load; no triggers are registered."
- **Fix Command:** `echo azure-functions >> requirements.txt`

### Check 7: `check_azure_functions_worker`
- **ID:** `check_azure_functions_worker`
- **Label:** "azure-functions-worker not pinned"
- **Type:** `package_forbidden`
- **Required:** `false`
- **Condition:**
  ```json
  {
    "package": "azure-functions-worker",
    "file": "requirements.txt"
  }
  ```
- **Category:** `dependencies`
- **Section:** `python_env`
- **Check Order:** 6
- **What it tests:** Ensures azure-functions-worker is NOT declared in requirements.txt
- **Pass detail:** "Package 'azure-functions-worker' not declared in requirements.txt"
- **Fail detail:** "Package 'azure-functions-worker' should not be declared in requirements.txt (managed by the platform)"
- **Hint:** "Remove azure-functions-worker from requirements.txt. The Azure Functions platform manages the worker runtime automatically."

### Check 8: `check_host_json`
- **ID:** `check_host_json`
- **Label:** "host.json"
- **Type:** `file_exists`
- **Required:** `true`
- **Condition:**
  ```json
  {
    "target": "host.json"
  }
  ```
- **Category:** `structure`
- **Section:** `project_structure`
- **Check Order:** 7
- **What it tests:** host.json exists at project root
- **Pass detail:** "/path/to/host.json exists"
- **Fail detail:** "/path/to/host.json not found"
- **Source Type:** `ms_learn`
- **Source URL:** https://learn.microsoft.com/en-us/azure/azure-functions/functions-host-json
- **Why it matters:** "host.json is required by the Azure Functions runtime to configure the host process. Without it the function app cannot start."
- **Symptoms:** "Function app fails to start locally or in Azure; 'Missing host.json' error in logs."

### Check 9: `check_host_json_version`
- **ID:** `check_host_json_version`
- **Label:** "host.json version"
- **Type:** `host_json_version`
- **Required:** `true`
- **Condition:** `{}`
- **Category:** `structure`
- **Section:** `project_structure`
- **Check Order:** 8
- **What it tests:** Reads host.json, validates JSON, checks that root["version"] == "2.0"
- **Pass detail:** 'host.json version is "2.0"'
- **Fail detail:** 'host.json version is "1.0", expected "2.0"' or "host.json is not valid JSON"
- **Source Type:** `ms_learn`
- **Source URL:** https://learn.microsoft.com/en-us/azure/azure-functions/functions-host-json
- **Why it matters:** "The runtime version field gates which host features are enabled. An incorrect or missing version causes the host to fall back to v1 behaviour or refuse to start."
- **Symptoms:** "Runtime version mismatch errors; unexpected v1-style function loading; host startup failure."

### Check 10: `check_local_settings`
- **ID:** `check_local_settings`
- **Label:** "local.settings.json"
- **Type:** `file_exists`
- **Required:** `false`
- **Condition:**
  ```json
  {
    "target": "local.settings.json"
  }
  ```
- **Category:** `structure`
- **Section:** `project_structure`
- **Check Order:** 9
- **What it tests:** local.settings.json exists
- **Pass detail:** "/path/to/local.settings.json exists"
- **Fail detail:** "/path/to/local.settings.json not found (optional)"

### Check 11: `check_func_cli`
- **ID:** `check_func_cli`
- **Label:** "Azure Functions Core Tools (func)"
- **Type:** `executable_exists`
- **Required:** `false`
- **Condition:**
  ```json
  {
    "target": "func"
  }
  ```
- **Category:** `tooling`
- **Section:** `tooling`
- **Check Order:** 19
- **What it tests:** shutil.which("func") returns a path
- **Pass detail:** "func detected"
- **Fail detail:** "func not found"

### Check 12: `check_func_core_tools_version`
- **ID:** `check_func_core_tools_version`
- **Label:** "Azure Functions Core Tools version"
- **Type:** `compare_version`
- **Required:** `false`
- **Condition:**
  ```json
  {
    "target": "func_core_tools",
    "operator": ">=",
    "value": "4.0"
  }
  ```
- **Category:** `tooling`
- **Section:** `tooling`
- **Check Order:** 20
- **What it tests:** Runs `func --version`, parses version, compares against 4.0
- **Pass detail:** "func 4.0.5455 (>=4.0)"
- **Fail detail:** "func 3.0.3904 (>=4.0)" or "func: not_installed"

### Check 13: `check_durabletask_config`
- **ID:** `check_durabletask_config`
- **Label:** "Durable Functions configuration"
- **Type:** `conditional_exists`
- **Required:** `false`
- **Condition:**
  ```json
  {
    "target": "host.json",
    "jsonpath": "$.extensions.durableTask"
  }
  ```
- **Category:** `configuration`
- **Section:** `durable`
- **Check Order:** 21
- **What it tests:** **Conditional** - first scans *.py for keywords: "durable", "DurableOrchestrationContext", "durable_functions", "orchestrator". If found, checks that host.json contains $.extensions.durableTask
- **Pass detail (no durable):** "No Durable Functions usage detected; check skipped"
- **Pass detail (with durable):** "host.json contains '$.extensions.durableTask'"
- **Fail detail:** "Required host.json property '$.extensions.durableTask' not found"

### Check 14: `check_app_insights`
- **ID:** `check_app_insights`
- **Label:** "Application Insights configuration"
- **Type:** `any_of_exists`
- **Required:** `false`
- **Condition:**
  ```json
  {
    "targets": [
      "APPLICATIONINSIGHTS_CONNECTION_STRING",
      "APPINSIGHTS_INSTRUMENTATIONKEY",
      "host.json:instrumentationKey"
    ]
  }
  ```
- **Category:** `telemetry`
- **Section:** `monitoring`
- **Check Order:** 24
- **What it tests:** Checks if any of: env var APPLICATIONINSIGHTS_CONNECTION_STRING, env var APPINSIGHTS_INSTRUMENTATIONKEY, or host.json key "instrumentationKey" exists
- **Pass detail:** "env:APPLICATIONINSIGHTS_CONNECTION_STRING set"
- **Fail detail:** "Targets not found"

### Check 15: `check_extension_bundle`
- **ID:** `check_extension_bundle`
- **Label:** "extensionBundle"
- **Type:** `host_json_property`
- **Required:** `false`
- **Condition:**
  ```json
  {
    "jsonpath": "$.extensionBundle"
  }
  ```
- **Category:** `configuration`
- **Section:** `extensions`
- **Check Order:** 25
- **What it tests:** host.json contains $.extensionBundle (any value)
- **Pass detail:** "host.json contains '$.extensionBundle'"
- **Fail detail:** "host.json property '$.extensionBundle' not found"

### Check 16: `check_asgi_wsgi_exposure`
- **ID:** `check_asgi_wsgi_exposure`
- **Label:** "ASGI/WSGI compatibility"
- **Type:** `callable_detection`
- **Required:** `false`
- **Condition:** `{}`
- **Category:** `framework`
- **Section:** `asgi_wsgi`
- **Check Order:** 26
- **What it tests:** Scans *.py for regex patterns: `\bFastAPI\s*\(|\bStarlette\s*\(|\bFlask\s*\(|\bQuart\s*\(`, `\bapp\s*=`, `ASGIApp|WSGIApp|asgi_app|wsgi_app`
- **Pass detail:** "Detected ASGI/WSGI-related patterns: [...]"
- **Fail detail:** "No ASGI/WSGI callable detected in project source"

### Check 17: `check_unused_files`
- **ID:** `check_unused_files`
- **Label:** "Detect unused or invalid files"
- **Type:** `file_glob_check`
- **Required:** `false`
- **Condition:**
  ```json
  {
    "patterns": [
      "**/__pycache__",
      "**/*.pyc",
      ".venv",
      "tests/"
    ]
  }
  ```
- **Category:** `project_health`
- **Section:** `cleanup`
- **Check Order:** 30
- **What it tests:** Runs path.rglob() for each pattern, reports first 5 matches
- **Pass detail:** "No unwanted files detected"
- **Fail detail:** "Found unwanted files: ['tests/', '.venv']"

### Check 18: `check_funcignore`
- **ID:** `check_funcignore`
- **Label:** ".funcignore"
- **Type:** `file_exists`
- **Required:** `false`
- **Condition:**
  ```json
  {
    "target": ".funcignore"
  }
  ```
- **Category:** `project_health`
- **Section:** `cleanup`
- **Check Order:** 31
- **What it tests:** .funcignore file exists
- **Pass detail:** "/path/.funcignore exists"
- **Fail detail:** "/path/.funcignore not found (optional)"

### Check 19: `check_local_settings_git_tracked`
- **ID:** `check_local_settings_git_tracked`
- **Label:** "local.settings.json not git-tracked"
- **Type:** `local_settings_security`
- **Required:** `false`
- **Condition:** `{}`
- **Category:** `project_health`
- **Section:** `security`
- **Check Order:** 32
- **What it tests:** If local.settings.json exists, runs `git ls-files --error-unmatch` to check if tracked
- **Pass detail (not exists):** "local.settings.json not present; check skipped"
- **Pass detail (not tracked):** "local.settings.json is not tracked by git"
- **Pass detail (git unavailable):** "git not available; local.settings.json git-tracking check skipped"
- **Fail detail:** "local.settings.json is tracked by git and may expose secrets — add it to .gitignore"

### Check 20: `check_extension_bundle_v4`
- **ID:** `check_extension_bundle_v4`
- **Label:** "extensionBundle v4 recommended"
- **Type:** `host_json_extension_bundle_version`
- **Required:** `false`
- **Condition:** `{}`
- **Category:** `configuration`
- **Section:** `extensions`
- **Check Order:** 33
- **What it tests:** Reads host.json, validates extensionBundle.id == "Microsoft.Azure.Functions.ExtensionBundle", checks version starts with "[4."
- **Pass detail:** "extensionBundle uses recommended v4 range: [4.*, 5.0.0)"
- **Fail detail:** "extensionBundle version '[3.*, 4.0.0)' is below recommended v4 range — upgrade to [4.*, 5.0.0)" or "extensionBundle id 'Custom.Bundle' is not the recommended 'Microsoft.Azure.Functions.ExtensionBundle'"

---

## 5. HANDLER TYPES IMPLEMENTATION

All handlers are in: `src/azure_functions_doctor/handlers.py` (722 lines)

### Implemented Handler Types (17)

| Handler Type | Used By | Implementation |
|-------------|---------|----------------|
| `compare_version` | check_python_version, check_func_core_tools_version | `_handle_compare_version()` - compares versions using `packaging.version.parse()` |
| `env_var_exists` | check_venv (legacy) | `_handle_env_var_exists()` - checks `os.getenv(target)` |
| `path_exists` | check_python_executable | `_handle_path_exists()` - checks `Path(target).exists()` or `sys.executable` |
| `file_exists` | check_requirements_txt, check_host_json, check_local_settings, check_funcignore | `_handle_file_exists()` - checks `(path / target).is_file()` |
| `package_installed` | (unused in v2.json) | `_handle_package_installed()` - uses `importlib.util.find_spec()` |
| `package_declared` | check_azure_functions_library | `_handle_package_declared()` - parses requirements.txt, splits on `[=<>!~]` |
| `package_forbidden` | check_azure_functions_worker | `_handle_package_forbidden()` - inverse of package_declared |
| `source_code_contains` | check_programming_model_v2 | `_handle_source_code_contains()` - string search OR AST mode |
| `conditional_exists` | check_durabletask_config | `_handle_conditional_exists()` - scans for durable keywords, then checks host.json |
| `callable_detection` | check_asgi_wsgi_exposure | `_handle_callable_detection()` - regex patterns for FastAPI/Flask/etc |
| `executable_exists` | check_func_cli | `_handle_executable_exists()` - uses `shutil.which()` |
| `any_of_exists` | check_venv, check_app_insights | `_handle_any_of_exists()` - checks env vars, files, or host.json keys |
| `file_glob_check` | check_unused_files | `_handle_file_glob_check()` - uses `path.rglob(pattern)` |
| `host_json_property` | check_extension_bundle | `_handle_host_json_property()` - reads host.json, walks JSONPath |
| `host_json_version` | check_host_json_version | `_handle_host_json_version()` - checks `host_data["version"] == "2.0"` |
| `local_settings_security` | check_local_settings_git_tracked | `_handle_local_settings_security()` - runs `git ls-files --error-unmatch` |
| `host_json_extension_bundle_version` | check_extension_bundle_v4 | `_handle_host_json_extension_bundle_version()` - validates bundle id and version range |

### Handler Registry Pattern
- `HandlerRegistry` class in `handlers.py` (line 169)
- All handlers registered in `__init__()` dict mapping type → method
- `generic_handler(rule, path)` is the public entry point (line 709)
- Returns `{"status": "pass"|"fail", "detail": str}`

---

## 6. CLI INTERFACE

### Command: `azure-functions doctor`

**Location:** `src/azure_functions_doctor/cli.py`

**Arguments:**
```bash
azure-functions doctor [OPTIONS]
```

**Options:**
- `path` (positional, default=".") - Path to Azure Functions app
- `--verbose / -v` - Show detailed hints for failed checks
- `--debug` - Enable debug logging to stderr
- `--format` - Output format: 'table', 'json', 'sarif', or 'junit' (default: table)
- `--output PATH` - Optional file path to save output
- `--profile` - Rule profile: 'minimal' or 'full' (default: full)
- `--rules PATH` - Optional path to custom rules file

**Exit Codes:**
- `0` - All required checks passed (optional failures allowed)
- `1` - One or more required checks failed

**Output Formats:**

1. **Table (default)** - Rich terminal output with icons (✓, ✗, !)
   ```
   Azure Functions Doctor   
   Path: /path/to/project

   Programming Model
   [✓] Programming model v2: @app. decorators found (AST)

   Python Env
   [✓] Python version: Python 3.10.13 (>=3.10)
   [!] Virtual environment: Targets not found (warn)
   [✓] Python executable: /usr/bin/python3.10 exists
   [✓] requirements.txt: /path/requirements.txt exists
   [✓] azure-functions package: Package 'azure-functions' declared in requirements.txt

   Doctor summary (to see all details, run azure-functions doctor -v):
     0 fails, 1 warning, 5 passed
   Exit code: 0
   ```

2. **JSON** - Machine-readable output
   ```json
   {
     "metadata": {
       "tool_version": "0.15.1",
       "generated_at": "2026-03-15T12:00:00Z",
       "target_path": "/path/to/project"
     },
     "results": [
       {
         "title": "Programming Model",
         "category": "programming_model",
         "status": "pass",
         "items": [
           {
             "label": "Programming model v2",
             "value": "Keyword '@app.|@bp.' found in source code (AST)",
             "status": "pass"
           }
         ]
       }
     ]
   }
   ```

3. **SARIF** - GitHub Security/CodeQL format
   - Includes `driver.rules` array with all loaded rules
   - Only includes non-passing results in `runs[0].results`
   - Maps `fail` → `level: "error"`, `warn` → `level: "warning"`
   - Includes `ruleId`, `message`, `locations`, optional `hint` in properties

4. **JUnit** - XML test report format
   - `<testsuite name="func-doctor">`
   - Each check becomes a `<testcase classname="section" name="label">`
   - Non-passing checks get `<failure message="detail">hint</failure>`

---

## 7. PROFILES

### Profile: `minimal`
**Purpose:** Required-only checks for CI gates  
**Usage:** `azure-functions doctor --profile minimal`

**Included checks (5):**
1. check_python_version
2. check_requirements_txt
3. check_azure_functions_library
4. check_host_json
5. check_host_json_version

**Excluded:** All optional checks (14 checks)

### Profile: `full` (default)
**Purpose:** Complete diagnostic suite  
**Usage:** `azure-functions doctor` or `azure-functions doctor --profile full`

**Included checks:** All 19 checks

---

## 8. PROGRAMMING MODEL DETECTION

**Location:** `src/azure_functions_doctor/doctor.py` - `_has_v2_decorators()` (line 67)

**Algorithm:**
1. Find all `*.py` files in project (excluding .venv, build, dist, .pytest_cache, __pycache__)
2. For each file, parse AST
3. Collect all variable names assigned to `FunctionApp()` calls (e.g., `app = FunctionApp()`)
4. If no assignments found, default to checking `app`
5. Walk AST and check all function/class decorators
6. If any decorator is `@<app_name>.<method>`, return True
7. Supports both `@app.route()` and Blueprint-style `@bp.route()`

**Result:** Always returns "v2" (doctor is v2-only, but detection affects check results)

---

## 9. TEST COVERAGE

### Test File Breakdown
- **test_api.py** (40 lines) - 2 tests
  - `test_run_diagnostics_minimal()` - Verifies run_diagnostics() returns expected structure
  - `test_run_diagnostics_profile_minimal()` - Verifies minimal profile filters optional rules

- **test_cli.py** (104 lines) - 5 tests
  - `test_cli_table_output()` - Verifies table format output
  - `test_cli_json_output()` - Verifies JSON output and exit code
  - `test_cli_verbose_output()` - Verifies --verbose shows hints
  - `test_cli_sarif_output()` - Verifies SARIF format
  - `test_cli_junit_output()` - Verifies JUnit XML format

- **test_config.py** (155 lines) - 13 tests
  - Tests Config class, environment variables, boolean parsing, custom rules path, singleton pattern

- **test_doctor.py** (130 lines) - 6 tests
  - `test_doctor_checks_pass()` - Full passing project
  - `test_missing_files()` - Missing required files
  - `test_custom_rules_path()` - Custom rules file
  - `test_custom_rules_path_invalid_raises()` - Invalid rules path
  - `test_profile_minimal_filters_optional_rules()` - Minimal profile
  - `test_invalid_profile_raises()` - Invalid profile name

- **test_handler.py** (615 lines) - 44 tests
  - Comprehensive coverage of all 17 handler types
  - Tests for pass/fail conditions, edge cases, error handling
  - Includes tests for:
    - `compare_version` (Python, func)
    - `env_var_exists`
    - `file_exists` / `path_exists`
    - `package_installed` / `package_declared` / `package_forbidden`
    - `source_code_contains` (string and AST modes)
    - `conditional_exists` (durable detection)
    - `callable_detection` (ASGI/WSGI)
    - `executable_exists`
    - `any_of_exists`
    - `file_glob_check`
    - `host_json_property`
    - `host_json_version`
    - `local_settings_security` (git tracking)
    - `host_json_extension_bundle_version`

- **test_examples.py** (122 lines) - Smoke tests
  - `TestPassingExamples` - 4 parametrized tests for http-trigger, timer-trigger, multi-trigger, blueprint
  - `TestBrokenExamples` - 4 tests for each broken example
  - Verifies passing examples pass all required checks
  - Verifies broken examples fail on exactly the intended check

- **test_handler_registry.py** (5861 lines) - Registry pattern tests
- **test_error_handling.py** (10577 lines) - Error handling tests
- **test_logging_config.py** (3670 lines) - Logging tests
- **test_programming_model_detection.py** (6784 lines) - AST detection tests
- **test_rule_loading.py** (4713 lines) - Rule loading/validation tests
- **test_rules_schema.py** (2153 lines) - JSON Schema validation tests
- **test_target_resolver.py** (2869 lines) - Target resolution tests
- **test_utils.py** (652 lines) - Utility tests

### Test Execution
```bash
make test       # Run all tests
make cov        # Run with coverage report
pytest -v tests  # Direct pytest
```

---

## 10. BUNDLED EXAMPLES

### Passing Examples (4)

1. **examples/v2/http-trigger/**
   - Minimal HTTP trigger
   - Files: function_app.py, host.json, requirements.txt, local.settings.sample.json
   - Passes all required checks

2. **examples/v2/timer-trigger/**
   - Timer trigger with schedule
   - Files: function_app.py, host.json, requirements.txt, local.settings.sample.json
   - Passes all required checks

3. **examples/v2/multi-trigger/**
   - Multiple triggers in one app (HTTP + Timer)
   - Files: function_app.py, host.json, requirements.txt, local.settings.sample.json
   - Passes all required checks

4. **examples/v2/blueprint/**
   - Blueprint-based modular routing
   - Files: function_app.py, http_blueprint.py, host.json, requirements.txt, local.settings.sample.json
   - Passes all required checks
   - Uses `@bp.route()` pattern (Blueprint)

### Broken Examples (4)

1. **examples/v2/broken-missing-host-json/**
   - Missing: host.json
   - Expected failure: `check_host_json`

2. **examples/v2/broken-missing-requirements/**
   - Missing: requirements.txt
   - Expected failure: `check_requirements_txt`

3. **examples/v2/broken-missing-azure-functions/**
   - Has requirements.txt but missing azure-functions package
   - Expected failure: `check_azure_functions_library`

4. **examples/v2/broken-no-v2-decorators/**
   - Has all files but no @app. decorators
   - Expected warning: `check_programming_model_v2` (status: warn)

---

## 11. RULE SCHEMA

**Location:** `src/azure_functions_doctor/schemas/rules.schema.json`

**Required Fields:**
- `id` (string) - Unique identifier
- `category` (enum) - environment, dependencies, structure, project_structure, configuration, bindings, tooling, telemetry, framework, project_health, config, tools
- `section` (string) - Grouping for output (e.g., python_env)
- `label` (string) - Display name in CLI
- `description` (string) - What the rule checks
- `type` (enum) - Handler type (17 options)
- `required` (boolean) - true = fail, false = warn
- `condition` (object) - Handler-specific parameters
- `check_order` (integer) - Display/execution order

**Optional Fields:**
- `hint` (string) - Remediation hint
- `severity` (string) - Deprecated, not used
- `fix` (string) - Natural language fix
- `fix_command` (string) - CLI command to fix
- `hint_url` (string, uri) - Documentation URL
- `tags` (array) - Searchable keywords
- `impact` (string) - Effect of failure
- `source_type` (enum) - ms_learn, derived, heuristic
- `source_title` (string) - Documentation title
- `source_url` (string, uri) - Canonical docs URL
- `why_it_matters` (string) - Production impact
- `symptoms` (string) - Observable failure symptoms

**Validation:** Rules are validated on load via `jsonschema.validate()`

---

## 12. CONFIGURATION

**Location:** `src/azure_functions_doctor/config.py`

**Environment Variables:**
- `FUNC_DOCTOR_LOG_LEVEL` - Log level (DEBUG, INFO, WARNING, ERROR)
- `FUNC_DOCTOR_LOG_FORMAT` - simple, structured
- `FUNC_DOCTOR_MAX_FILE_SIZE_MB` - Max file size (not yet wired)
- `FUNC_DOCTOR_SEARCH_TIMEOUT_SECONDS` - Search timeout (not yet wired)
- `FUNC_DOCTOR_RULES_FILE` - Custom rules file name
- `FUNC_DOCTOR_OUTPUT_WIDTH` - Output width (not yet wired)
- `FUNC_DOCTOR_ENABLE_COLORS` - Enable colors (not yet wired)
- `FUNC_DOCTOR_PARALLEL_EXECUTION` - Parallel checks (not yet wired)
- `FUNC_DOCTOR_CUSTOM_RULES` - Path to custom rules (alternative to --rules)

**Config Access:**
```python
from azure_functions_doctor.config import get_config
config = get_config()
log_level = config.get_log_level()
```

**Note:** Most config options are reserved for future use. CLI currently controls logging via `setup_logging()` directly.

---

## 13. LOGGING

**Location:** `src/azure_functions_doctor/logging_config.py`

**Logger Hierarchy:**
- Root: `azure_functions_doctor`
- Module loggers: `azure_functions_doctor.<module>`

**Setup:**
```python
from azure_functions_doctor.logging_config import setup_logging, get_logger

# Configure (called once in cli.py)
setup_logging(level="DEBUG", format_style="structured", enable_console_output=True)

# Get logger
logger = get_logger(__name__)
logger.info("Starting diagnostics")
```

**Format Styles:**
- `structured`: `%(asctime)s [%(levelname)8s] %(name)s: %(message)s`
- `simple`: `%(levelname)s: %(message)s`

**Special Functions:**
- `log_diagnostic_start(path, rules_count)` - Logs start of diagnostic session
- `log_diagnostic_complete(total, passed, failed, errors, duration_ms)` - Logs completion
- `log_rule_execution(rule_id, rule_type, status, duration_ms)` - Logs individual rule execution

**Output:** All logs go to stderr to avoid mixing with CLI stdout

---

## 14. API ENTRY POINTS

### Public API: `api.py`

```python
from azure_functions_doctor.api import run_diagnostics

results = run_diagnostics(
    path="./examples/v2/http-trigger",
    profile="minimal",  # optional
    rules_path=Path("custom_rules.json")  # optional
)

# Returns: List[SectionResult]
# [
#   {
#     "title": "Python Env",
#     "category": "python_env",
#     "status": "pass",
#     "items": [
#       {
#         "label": "Python version",
#         "value": "Python 3.10.13 (>=3.10)",
#         "status": "pass",
#         "hint": "...",  # if present
#         "hint_url": "..."  # if present
#       }
#     ]
#   }
# ]
```

### Doctor Class: `doctor.py`

```python
from azure_functions_doctor.doctor import Doctor
from pathlib import Path

doctor = Doctor(
    path="./examples/v2/http-trigger",
    profile="minimal",  # optional
    rules_path=Path("custom_rules.json")  # optional
)

# Load rules (with validation)
rules = doctor.load_rules()

# Run all checks
results = doctor.run_all_checks(rules=rules)  # rules optional

# Check programming model
model = doctor.programming_model  # "v2"
```

---

## 15. FILE READING AND SAFETY

### Excluded Directories
- `.venv`
- `build`
- `dist`
- `.pytest_cache`
- `__pycache__`

### File Reading
- UTF-8 encoding with fallback to `errors="ignore"`
- Graceful handling of:
  - PermissionError
  - UnicodeDecodeError
  - MemoryError
  - OSError
  - ValueError

### Security
- subprocess calls use `nosec B603 B607` annotations (bandit)
- subprocess.run() used with timeout (10s)
- No shell=True usage
- Git commands use explicit paths

---

## 16. STATUS MAPPING

### Handler Status → Item Status
- Handler returns: `{"status": "pass"|"fail", "detail": str}`
- Doctor maps to canonical status:
  - `handler_status == "pass"` → `item_status = "pass"`
  - `handler_status == "fail" AND required == True` → `item_status = "fail"`
  - `handler_status == "fail" AND required == False` → `item_status = "warn"`

### Exit Code Mapping
- `fail_count > 0` → exit code 1
- `fail_count == 0` → exit code 0
- Warnings do NOT affect exit code

### Output Icons (utils.py)
```python
STATUS_ICONS = {
    "pass": "✓",
    "warn": "!",
    "fail": "✗",
}
```

---

## 17. GAPS ANALYSIS PREPARATION

### Questions to Answer During Spec Comparison

1. **Missing Checks:**
   - Are there checks in the spec that are NOT in v2.json?
   - Are there handler types mentioned in spec but not implemented?

2. **Extra Checks:**
   - Are there checks in v2.json that are NOT in the spec?
   - Should these be removed or documented?

3. **Check Discrepancies:**
   - Do check IDs match between spec and implementation?
   - Do check labels match?
   - Do required/optional flags match?
   - Do handler types match?
   - Do conditions match?

4. **Handler Implementation:**
   - Are all handler types in the schema implemented?
   - Are all handler types used by rules tested?

5. **Documentation:**
   - Is every check documented in rules.md?
   - Is rule_inventory.md up to date?
   - Are all examples tested in CI?

6. **Test Coverage:**
   - Is every check tested in test_handler.py?
   - Is every example smoke-tested in test_examples.py?
   - Are all edge cases covered?

---

## 18. COMPLETE SOURCE FILE CONTENTS

### src/azure_functions_doctor/__init__.py
```python
"""Init for azure_function_doctor package.

This module initializes the Azure Functions Doctor package and defines the version string.
"""

__version__ = "0.15.1"
```

### src/azure_functions_doctor/api.py
```python
from pathlib import Path
from typing import List, Optional

from azure_functions_doctor.doctor import Doctor, SectionResult


def run_diagnostics(
    path: str,
    profile: Optional[str] = None,
    rules_path: Optional[Path] = None,
) -> List[SectionResult]:
    """
    Run diagnostics on the Azure Functions application at the specified path.

    Args:
        path: The file system path to the Azure Functions application.
        profile: Optional rule profile ('minimal' or 'full').

    Returns:
        A list of SectionResult containing the results of each diagnostic check.
    """
    return Doctor(path, profile=profile, rules_path=rules_path).run_all_checks()
```

### Complete handlers.py Summary (722 lines)
- HandlerRegistry class with 17 handler methods
- All handlers return `{"status": "pass"|"fail", "detail": str}`
- Error handling via `_handle_specific_exceptions()`
- AST parsing for decorator detection
- JSONPath navigation for host.json checks
- Git integration for security checks
- Version comparison via packaging.version

### Complete doctor.py Summary (223 lines)
- Doctor class: main diagnostic runner
- `_detect_programming_model()` - Always returns "v2"
- `_has_v2_decorators()` - AST-based decorator detection
- `load_rules()` - Load and validate rules from JSON
- `_validate_rules()` - JSON Schema validation
- `_load_v2_rules()` - Load built-in v2.json
- `run_all_checks()` - Execute all rules, group by section, return SectionResult list
- Status mapping: pass/fail/warn based on required flag

### Complete cli.py Summary (349 lines)
- Typer CLI app with `doctor` command
- Input validation: path, format, output
- 4 output formats: table, json, sarif, junit
- Profile support: minimal, full
- Verbose mode: shows hints
- Debug mode: enables debug logging
- Exit code: 1 if any fail, 0 otherwise
- Rich terminal output with icons

---

## 19. SUMMARY

**Project Maturity:** Production-ready (v0.15.1, comprehensive test suite, CI/CD, docs)

**Architecture:**
- **Rule-driven:** All checks declarative in JSON
- **Handler registry:** Extensible handler pattern
- **AST-aware:** Uses AST parsing for decorator detection
- **Multi-format output:** Table, JSON, SARIF, JUnit
- **Profile-based:** Minimal (required only) vs Full (all checks)
- **Exit-code aware:** Proper CI integration

**Current Check Count:** 19 checks (5 required, 14 optional)

**Handler Count:** 17 handler types implemented

**Test Coverage:**
- Unit tests: handlers, config, logging, doctor core
- Integration tests: CLI output formats, exit codes
- Smoke tests: All 8 example projects
- Schema validation tests

**Key Strengths:**
1. Comprehensive rule schema with validation
2. AST-based decorator detection (not regex)
3. Multiple output formats for different CI systems
4. Extensive error handling and graceful degradation
5. Well-documented with examples
6. Semantic versioning with changelog
7. Security-aware (git tracking, secrets, subprocess safety)

**Next Steps for Gap Analysis:**
1. Compare this inventory against DESIGN.md spec
2. Identify missing checks
3. Identify extra checks not in spec
4. Verify handler implementations match spec
5. Check documentation completeness
6. Verify test coverage matches spec requirements

---

**End of Codebase Analysis**
