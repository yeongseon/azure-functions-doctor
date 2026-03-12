# JSON Output Contract

The `--format json` flag produces machine-readable output designed for CI/CD pipelines, automated gates, and integration with other tooling.

## Schema Structure

The JSON output consists of a `metadata` object and a `results` array.

```json
{
  "metadata": {
    "tool_version": "string",
    "generated_at": "ISO 8601 UTC timestamp",
    "target_path": "absolute path string"
  },
  "results": [
    {
      "title": "section title (title-cased)",
      "category": "section key",
      "status": "pass | fail",
      "items": [
        {
          "label": "human-readable check name",
          "value": "detail string",
          "status": "pass | warn | fail",
          "hint": "optional fix suggestion",
          "hint_url": "optional documentation URL"
        }
      ]
    }
  ]
}
```

## Stability Levels

To ensure reliable automation, fields are categorized by their stability.

| Field | Stability | Notes |
| --- | --- | --- |
| `metadata.tool_version` | Stable | Version of the doctor tool. |
| `metadata.generated_at` | Stable | UTC timestamp of the execution. |
| `metadata.target_path` | Stable | Resolved absolute path of the target directory. |
| `results[].category` | Stable | Machine-readable identifier for the check section. |
| `results[].status` | Stable | Aggregated status: `fail` if any required check in the section failed. |
| `results[].items[].label` | Stable | Canonical name of the check. |
| `results[].items[].status` | Stable | Check result: `pass`, `warn` (optional failed), or `fail` (required failed). |
| `results[].items[].value` | Stable | The diagnostic message or detail string. |
| `results[].title` | Detail | For display only; formatting or casing may change. |
| `results[].items[].hint` | Detail | Human-readable fix suggestion. |
| `results[].items[].hint_url` | Detail | External documentation link. |

Breaking changes to stable fields require a major version release.

## Exit Codes

Automated pipelines should rely on the process exit code:

- `0`: Success. All required checks passed.
- `1`: Failure. One or more required checks failed.

## Other Formats

While this contract covers the primary JSON format, Azure Functions Doctor also supports SARIF and JUnit outputs. These follow their respective industry-standard schemas and are not governed by this specific JSON contract.
