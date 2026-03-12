# Examples

Azure Functions Doctor ships with examples for the **Azure Functions Python v2 programming model**.

| Role | Example | Path | Description |
| --- | --- | --- | --- |
| Representative | HTTP trigger | `examples/v2/http-trigger` | Minimal single HTTP trigger app. |
| Representative | Timer trigger | `examples/v2/timer-trigger` | Timer-triggered function with CRON schedule. |
| Complex | Multi trigger | `examples/v2/multi-trigger` | Single app with multiple decorator-based triggers. |
| Complex | Blueprint | `examples/v2/blueprint` | HTTP trigger using `func.Blueprint` for modular routing. |
| Broken | Missing host.json | `examples/v2/broken-missing-host-json` | No `host.json` — triggers HOST_JSON_EXISTS. |
| Broken | Missing requirements | `examples/v2/broken-missing-requirements` | No `requirements.txt` — triggers REQUIREMENTS_TXT_EXISTS. |
| Broken | Missing azure-functions | `examples/v2/broken-missing-azure-functions` | `azure-functions` absent from deps — triggers AZURE_FUNCTIONS_DEPENDENCY. |
| Broken | No v2 decorators | `examples/v2/broken-no-v2-decorators` | Plain Python with no `@app.*` decorators — triggers V2_DECORATORS_USED. |

## Run Diagnostics

```bash
# Passing examples
azure-functions doctor --path examples/v2/http-trigger
azure-functions doctor --path examples/v2/timer-trigger
azure-functions doctor --path examples/v2/multi-trigger
azure-functions doctor --path examples/v2/blueprint

# Broken examples (expect failures)
azure-functions doctor --path examples/v2/broken-missing-host-json
azure-functions doctor --path examples/v2/broken-missing-requirements
azure-functions doctor --path examples/v2/broken-missing-azure-functions
azure-functions doctor --path examples/v2/broken-no-v2-decorators
```
