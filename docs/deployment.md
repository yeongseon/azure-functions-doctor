# Deployment Guide
This guide follows the LangGraph deployment-guide style, but for `azure-functions-doctor` the sequence is diagnostics first, deployment second. You will run doctor on healthy and broken examples, generate machine-readable reports, then deploy the healthy Azure Functions app. Outputs are representative examples, not guaranteed byte-for-byte.

## Prerequisites
| Requirement | Minimum | Notes |
|---|---|---|
| Azure subscription | Active | Use `<YOUR_SUBSCRIPTION_ID>` |
| Azure CLI (`az`) | Current | `az --version` |
| Azure Functions Core Tools (`func`) | v4 | `func --version` |
| Python | 3.10+ | Runtime shown is Python 3.11 |
| Azure Functions Doctor | 0.16.2 | Install from PyPI |

## Install CLI
```bash
python -m pip install --upgrade pip
pip install azure-functions-doctor==0.16.2
```
Representative output:
```bash
Requirement already satisfied: pip in ./.venv/lib/python3.11/site-packages (25.0)
Collecting azure-functions-doctor==0.16.2
Downloading azure_functions_doctor-0.16.2-py3-none-any.whl
Installing collected packages: azure-functions-doctor
Successfully installed azure-functions-doctor-0.16.2
```

## Section 1: Pre-deploy diagnostics on healthy project
Use `--profile minimal` for canonical deterministic pass output.
```bash
azure-functions doctor examples/v2/http-trigger --profile minimal
```
Representative output:
```text
Azure Functions Doctor
Path: /data/GitHub/azure-functions-doctor/examples/v2/http-trigger

Python Env
[PASS] Python version: Python 3.11.11
[PASS] requirements.txt: found
[PASS] azure-functions package: declared in requirements.txt

Project Structure
[PASS] host.json: found
[PASS] host.json version: "2.0"

Doctor summary (to see all details, run azure-functions doctor -v):
  0 fails, 0 warnings, 5 passed
Exit code: 0
```
Summary format is `{fail_count} fails, {warning_count} warnings, {passed_count} passed`. Exit code is `0` when there are no failures.

## Section 2: Diagnostics on broken projects
Run diagnostics against the broken sample missing `host.json`.
```bash
azure-functions doctor examples/v2/broken-missing-host-json
```
Representative output:
```text
Azure Functions Doctor
Path: /data/GitHub/azure-functions-doctor/examples/v2/broken-missing-host-json

Python Env
[PASS] Python version: Python 3.11.11
[PASS] requirements.txt: found
[PASS] azure-functions package: declared in requirements.txt

Project Structure
[FAIL] host.json: file not found (fail)
[FAIL] host.json version: host.json missing or invalid (fail)

Doctor summary (to see all details, run azure-functions doctor -v):
  2 fails, 0 warnings, 3 passed
Exit code: 1
```
Exit code is `1` when one or more required checks fail.

## Section 3: Machine-readable output formats
### JSON
```bash
azure-functions doctor examples/v2/http-trigger --format json --profile minimal
```
Representative output:
```json
{
  "metadata": {
    "tool_version": "0.16.2",
    "generated_at": "2025-01-15T10:30:00Z",
    "target_path": "/path/to/examples/v2/http-trigger"
  },
  "results": [
    {
      "title": "...",
      "category": "...",
      "status": "pass",
      "items": [
        {
          "label": "...",
          "value": "...",
          "status": "pass",
          "hint": "...",
          "hint_url": "..."
        }
      ]
    }
  ]
}
```

### SARIF
```bash
azure-functions doctor examples/v2/http-trigger --format sarif --profile minimal
```
Representative output:
```json
{
  "version": "2.1.0",
  "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
  "runs": [
    {
      "tool": {
        "driver": {
          "name": "azure-functions-doctor",
          "version": "0.16.2",
          "informationUri": "https://github.com/yeongseon/azure-functions-doctor",
          "rules": [
            {
              "id": "check_python_version",
              "name": "Python version"
            },
            {
              "id": "check_host_json",
              "name": "host.json"
            }
          ]
        }
      },
      "results": []
    }
  ]
}
```
When all checks pass, SARIF `results` is empty because doctor includes only non-pass items in SARIF output.

### JUnit
```bash
azure-functions doctor examples/v2/http-trigger --format junit --profile minimal
```
Representative output:
```xml
<?xml version="1.0" encoding="utf-8"?>
<testsuite name="func-doctor" tests="5" failures="0" skipped="0" time="0.021">
  <testcase classname="Python Env" name="Python version" />
  <testcase classname="Python Env" name="requirements.txt" />
  <testcase classname="Python Env" name="azure-functions package" />
  <testcase classname="Project Structure" name="host.json" />
  <testcase classname="Project Structure" name="host.json version" />
</testsuite>
```
JUnit root element is `<testsuite name="func-doctor" ...>`.

### Summary JSON sidecar
```bash
azure-functions doctor examples/v2/http-trigger --profile minimal --summary-json doctor-summary.json
```
Representative output file:
```json
{"passed":5,"warned":0,"failed":0}
```

## Section 4: Deploy the healthy example
Deploy `examples/v2/http-trigger` after diagnostics are clean.

### Prepare dependencies
```bash
python -m pip install --upgrade pip
pip install -r examples/v2/http-trigger/requirements.txt
```
Representative output:
```bash
Requirement already satisfied: pip in ./.venv/lib/python3.11/site-packages (25.0)
Collecting azure-functions
Successfully installed azure-functions-1.21.0
```

### Provision Azure resources
```bash
az account set --subscription <YOUR_SUBSCRIPTION_ID>
az group create --name <YOUR_RESOURCE_GROUP> --location eastus
```
Representative output:
```json
{"name":"<YOUR_RESOURCE_GROUP>","location":"eastus","properties":{"provisioningState":"Succeeded"}}
```

```bash
az storage account create \
  --name <YOUR_STORAGE_ACCOUNT> \
  --resource-group <YOUR_RESOURCE_GROUP> \
  --location eastus \
  --sku Standard_LRS \
  --kind StorageV2
```
Representative output:
```json
{"name":"<YOUR_STORAGE_ACCOUNT>","kind":"StorageV2","provisioningState":"Succeeded"}
```

```bash
az functionapp create \
  --name <YOUR_FUNCTION_APP_NAME> \
  --resource-group <YOUR_RESOURCE_GROUP> \
  --storage-account <YOUR_STORAGE_ACCOUNT> \
  --consumption-plan-location eastus \
  --runtime python \
  --runtime-version 3.11 \
  --functions-version 4
```
Representative output:
```json
{"name":"<YOUR_FUNCTION_APP_NAME>","defaultHostName":"<YOUR_FUNCTION_APP_NAME>.azurewebsites.net","state":"Running"}
```

### Publish
From `examples/v2/http-trigger`:
```bash
func azure functionapp publish <YOUR_FUNCTION_APP_NAME> --python
```
Representative output:
```text
Getting site publishing info...
Starting the function app deployment...
Uploading package...
Deployment completed successfully.
Syncing triggers...
Functions in <YOUR_FUNCTION_APP_NAME>:
    HttpExample - [httpTrigger]
        Invoke url: https://<YOUR_FUNCTION_APP_NAME>.azurewebsites.net/api/HttpExample
Deployment successful.
```

### Verify endpoint behavior
```bash
export BASE_URL="https://<YOUR_FUNCTION_APP_NAME>.azurewebsites.net"
```
`GET /api/HttpExample?name=Azure`:
```bash
curl -i "$BASE_URL/api/HttpExample?name=Azure"
```
Representative response:
```text
HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8

Hello, Azure. This v2 HTTP triggered function executed successfully.
```

`GET /api/HttpExample`:
```bash
curl -i "$BASE_URL/api/HttpExample"
```
Representative response:
```text
HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8

This v2 HTTP triggered function executed successfully. Pass a name in the query string or request body for a personalized response.
```
Both responses are plain text with HTTP `200`.

## CI integration
Run doctor before publish in CI:
```bash
azure-functions doctor . --format junit --output doctor-results.xml --profile minimal
```
Representative CI sequence:
```bash
azure-functions doctor . --format junit --output doctor-results.xml --profile minimal
func azure functionapp publish <YOUR_FUNCTION_APP_NAME> --python
```
If required checks fail, doctor exits `1` and deployment should not continue.

## Cleanup
```bash
az group delete --name <YOUR_RESOURCE_GROUP> --yes --no-wait
```
Representative output:
```text
{"status":"Accepted"}
```

## Sources
- [Azure Functions Python quickstart](https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-python)
- [Azure Functions Core Tools publish reference](https://learn.microsoft.com/en-us/azure/azure-functions/functions-core-tools-reference#func-azure-functionapp-publish)
- [SARIF specification reference](https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html)

## See Also
- [`azure-functions-scaffold`](https://github.com/yeongseon/azure-functions-scaffold)
- [`azure-functions-logging`](https://github.com/yeongseon/azure-functions-logging)
