# Broken Fixture: No v2 Decorators

This fixture is intentionally broken by omitting v2 decorator usage (`@app.*`).

The project has valid `host.json`, `requirements.txt`, and `azure-functions` declared,
but `function_app.py` does not use `func.FunctionApp()` or any `@app.*` decorators.

## Expected rule failure

- `check_programming_model_v2`

## Expected doctor output

When running `azure-functions doctor --path examples/v2/broken-no-v2-decorators`, the report
should include a failed `Programming model v2` check because no `@app.` decorator usage is found.
