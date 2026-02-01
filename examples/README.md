# Examples

| Model | Path | Description |
|-------|------|-------------|
| v1 (function.json) | `examples/http_trigger_v1` | Legacy single HTTP trigger function folder. |
| v1 (multi) | `examples/multi_trigger_v1` | Multiple triggers (HTTP, timer, queue) function.json model. |
| v2 (decorators) | `examples/http_trigger_v2` | Minimal single HTTP trigger using decorator API. |
| v2 (multi) | `examples/multi_trigger_v2` | Multiple triggers (HTTP, timer, queue placeholder). |

## Install (one time)
```bash
pip install azure-functions-doctor
# or from source
pip install -e .
```

## Run Diagnostics (examples)

v1 (single):
```bash
azure-functions doctor --path examples/http_trigger_v1
```

v1 (multi):
```bash
azure-functions doctor --path examples/multi_trigger_v1
```

v2 (single):
```bash
azure-functions doctor --path examples/http_trigger_v2
```

v2 (multi):
```bash
azure-functions doctor --path examples/multi_trigger_v2
```
