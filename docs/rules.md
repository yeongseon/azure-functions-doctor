# 📘 `rules.json` Documentation

The `rules.json` file defines diagnostic checks declaratively for **Azure Functions Doctor**. Each rule specifies what to validate, how to validate it, and what to show when the check passes or fails — without modifying the core Python code.

This makes the tool extensible and customizable.

---

## 📁 Location

The file is located under the **assets/** directory:

```
src/
└── azure_functions_doctor/
    └── assets/
        └── rules.json  👈
```

---

## ⌐ Structure of a Rule

Each rule is a JSON object with the following fields:

```json
{
  "id": "check_python_version",
  "section": "python_env",
  "label": "Python version",
  "type": "compare_version",
  "condition": {
    "target": "python",
    "operator": ">=",
    "value": "3.9"
  },
  "hint": "Install Python 3.9 or higher."
}
```

### 🔑 Fields Explained

| Field       | Type   | Description                                       |
| ----------- | ------ | ------------------------------------------------- |
| `id`        | string | Unique identifier for the rule                    |
| `section`   | string | Logical group (e.g. `python_env`, `config_files`) |
| `label`     | string | Human-readable label for the check                |
| `type`      | string | Rule type (see below)                             |
| `condition` | object | Parameters for the rule type (see below)          |
| `hint`      | string | Suggestion if the rule fails                      |

### 🔑 `condition` Fields

| Field      | Type   | Used by                       | Description                             |
| ---------- | ------ | ----------------------------- | --------------------------------------- |
| `target`   | string | compare_version, file/path, env, package | Subject to evaluate           |
| `operator` | string | compare_version               | Comparison operator (e.g. `==`, `>=`)  |
| `value`    | any    | compare_version               | Expected value to compare              |
| `keyword`  | string | source_code_contains          | Keyword to search for in `.py` files  |
| `pypi`     | string | package_installed (optional)  | Package name for display/documentation |

---

## 🔍 Supported Rule Types

### 1. `compare_version`

Compare semantic versions.

```json
{
  "type": "compare_version",
  "condition": {
    "target": "python",
    "operator": ">=",
    "value": "3.9"
  }
}
```

* Valid `target`: `"python"`

---

### 2. `file_exists`

Check whether a file exists.

```json
{
  "type": "file_exists",
  "condition": {
    "target": "host.json"
  }
}
```

---

### 3. `env_var_exists`

Check whether an environment variable is set.

```json
{
  "type": "env_var_exists",
  "condition": {
    "target": "VIRTUAL_ENV"
  }
}
```

---

### 4. `path_exists`

Check whether a path exists.

```json
{
  "type": "path_exists",
  "condition": {
    "target": "sys.executable"
  }
}
```

---

### 5. `package_installed`

Check whether a Python package is importable.

```json
{
  "type": "package_installed",
  "condition": {
    "target": "azure.functions",
    "pypi": "azure-functions-python-library"
  }
}
```

---

### 6. `source_code_contains`

Check whether a keyword appears in any `.py` files.

```json
{
  "type": "source_code_contains",
  "condition": {
    "keyword": "@app."
  }
}
```

---

## 📁 Grouping by `section`

Sections allow grouping related checks together for better readability in the CLI output:

Example:

```json
{
  "section": "python_env",
  "label": "Python Version",
  ...
}
```

Predefined sections might include:

* `python_env`
* `core_tools`
* `config_files`
* `dependencies`
* `network`

You can create your own section names if desired.

---

## 🧹 Extending the Rules

To add a new rule:

1. Open `src/azure_functions_doctor/assets/rules.json`
2. Append your rule object to the array
3. Save and rerun `func-doctor`

Example:

```json
{
  "id": "check_requirements_txt_exists",
  "section": "dependencies",
  "label": "requirements.txt exists",
  "type": "file_exists",
  "condition": {
    "target": "requirements.txt"
  },
  "hint": "Create a requirements.txt file to declare Python dependencies."
}
```

---

## 🛠️ Tips

* Use `hint` to provide helpful, actionable suggestions.
* Use consistent `section` names for better CLI grouping.
* If you're writing new rule types, update `handlers.py` and `rules.schema.json`.

---

## 🥪 Testing Your Changes

After editing `rules.json`, you can run:

```bash
func-doctor diagnose --verbose
```

To see grouped results and hints.

---

## 📟 Example `rules.json` (simplified)

```json
[
  {
    "id": "check_python_version",
    "section": "python_env",
    "label": "Python version",
    "type": "compare_version",
    "condition": {
      "target": "python",
      "operator": ">=",
      "value": "3.9"
    },
    "hint": "Install Python 3.9 or higher."
  },
  {
    "id": "check_host_json_exists",
    "section": "config_files",
    "label": "host.json exists",
    "type": "file_exists",
    "condition": {
      "target": "host.json"
    }
  }
]
```

---

## 📬 Contribute New Rules

Want to improve the default rules? Feel free to open a PR or discussion on  
👉 [GitHub Repository](https://github.com/yeongseon/azure-functions-doctor-for-python)
