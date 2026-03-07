# Multi Trigger Example

Single project demonstrating multiple triggers in the Azure Functions Python v2 programming model.

## Run

```bash
cd examples/v2/multi-trigger
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
func start
```

## Diagnose

```bash
azure-functions doctor --path .
```
