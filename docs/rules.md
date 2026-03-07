# Rules

Azure Functions Doctor uses a declarative JSON ruleset for the **Azure Functions Python v2 programming model**.

The built-in rules live in:

```text
src/azure_functions_doctor/assets/rules/v2.json
```

You can also pass a custom rules file with `--rules`.

## Rule Format

Each rule is a JSON object with these core fields:

```json
{
  "id": "check_python_version",
  "category": "environment",
  "section": "python_env",
  "label": "Python version",
  "description": "Checks if the current Python version is 3.10 or higher.",
  "type": "compare_version",
  "required": true,
  "condition": {
    "target": "python",
    "operator": ">=",
    "value": "3.10"
  },
  "check_order": 1
}
```

## Supported Rule Types

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

## Built-in Selection

The doctor always loads the built-in v2 ruleset unless you provide a custom rules file.

## Extending the Rules

To add or adjust a built-in rule:

1. Edit `src/azure_functions_doctor/assets/rules/v2.json`
2. Update or add tests
3. Run `make check-all`

## Safety Note

Only load custom rules from trusted sources. Some rule types execute imports or inspect the local environment directly.
