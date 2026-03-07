# HTTP Trigger Example

Minimal single HTTP trigger for the Azure Functions Python v2 programming model.

## Run

```bash
cd examples/v2/http-trigger
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp local.settings.sample.json local.settings.json
func start
```

## Diagnose

```bash
azure-functions doctor --path .
```
