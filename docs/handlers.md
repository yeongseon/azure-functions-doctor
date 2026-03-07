# Handlers

Handlers execute rule definitions from `src/azure_functions_doctor/assets/rules/v2.json`.

## Contract

- Input: `rule` and project `path`
- Output: a dictionary with `status` and `detail`
- Status values: `pass` or `fail`

Optional rules are converted to `warn` later in the aggregation layer.

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

## Notes

- `source_code_contains` supports a simple string mode and an AST-based mode.
- `conditional_exists` is used for checks that only matter when a related feature is detected.
- Handler implementations live in `src/azure_functions_doctor/handlers.py`.

## Development

When adding a new handler:

1. Extend the `Rule["type"]` literal
2. Register the handler in `HandlerRegistry`
3. Update `rules.schema.json`
4. Add tests in `tests/test_handler.py`
