# CLI Usage

`azure-functions doctor` validates a local Azure Functions project that uses the **Python v2 programming model**.

## Basic Usage

```bash
azure-functions doctor
```

Run against a specific directory:

```bash
azure-functions doctor --path ./my-function-app
```

## Options

| Option | Description |
| --- | --- |
| `--path` | Target directory. Defaults to the current directory. |
| `--format` | Output format: `table`, `json`, `sarif`, or `junit`. |
| `--output` | Optional file path for the selected output format. |
| `--verbose` | Show fix hints for non-passing checks. |
| `--debug` | Enable debug logging. |
| `--profile` | Rule profile: `minimal` or `full`. |
| `--rules` | Optional path to a custom rules file. |

## Model Support

Azure Functions Doctor expects the decorator-based Python v2 model:

- `func.FunctionApp()`
- decorators such as `@app.route()`, `@app.timer_trigger()`, and `@app.schedule()`

If a project does not expose v2 decorators, the built-in `Programming model v2` check fails.

## Output Semantics

Each check produces one of three statuses:

- `pass`: the required condition is satisfied
- `warn`: an optional check failed
- `fail`: a required check failed

Exit codes:

- `0`: no failed required checks
- `1`: one or more failed required checks

## Examples

Human-readable output:

```bash
azure-functions doctor --path ./examples/v2/http-trigger
```

JSON output for CI:

```bash
azure-functions doctor --format json --output doctor-report.json
```

Required-only profile:

```bash
azure-functions doctor --profile minimal
```
