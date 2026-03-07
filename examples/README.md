# Examples

Azure Functions Doctor ships with examples for the **Azure Functions Python v2 programming model**.

| Example | Path | Description |
| --- | --- | --- |
| HTTP trigger | `examples/v2/http-trigger` | Minimal single HTTP trigger app. |
| Multi trigger | `examples/v2/multi-trigger` | Single app with multiple decorator-based triggers. |

## Run Diagnostics

```bash
azure-functions doctor --path examples/v2/http-trigger
azure-functions doctor --path examples/v2/multi-trigger
```
