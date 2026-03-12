# Azure Functions Doctor

Azure Functions Doctor validates local projects built on the **Azure Functions Python v2 programming model**.

Use it to catch common setup and configuration issues before running locally or shipping through CI.

## Quick Start

```bash
pip install azure-functions-doctor
azure-functions doctor
```

## What it checks

- Python 3.10+
- v2 decorator usage
- `requirements.txt`
- `azure-functions`
- `host.json`
- optional local tooling and host configuration

## Documentation

- [Usage Guide](usage.md)
- [Rules Reference](rules.md)
- [Rule Inventory](rule_inventory.md)
- [Minimal Profile](minimal_profile.md)
- [JSON Output Contract](json_output_contract.md)
- [Semver Policy](semver_policy.md)
- [Diagnostics Reference](diagnostics.md)
- [Supported Versions](supported_versions.md)
- [Development Guide](development.md)
- [Release Process](release_process.md)

## Examples

- [Representative example](https://github.com/yeongseon/azure-functions-doctor/blob/main/examples/v2/http-trigger/README.md)
- [Complex example](https://github.com/yeongseon/azure-functions-doctor/blob/main/examples/v2/multi-trigger/README.md)
