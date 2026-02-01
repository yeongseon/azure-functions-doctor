# http-trigger (Programming Model v2)

Minimal single HTTP trigger for the Python v2 programming model.

## Structure
```
v2/http-trigger/
├── function_app.py
├── host.json
├── requirements.txt
├── local.settings.sample.json
└── README.md
```

## Key Points
- Uses the decorator-based programming model.
- Single HTTP route returning a greeting.
- Mirrors the v1 example structure for comparison (see `examples/http_trigger_v1`).

## Run
```bash
cd examples/http_trigger_v2
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp local.settings.sample.json local.settings.json
func start
```

## Diagnostics
```bash
azure-functions doctor --path .
```

* Compare with the v1 example in `examples/http_trigger_v1` for structural differences.
