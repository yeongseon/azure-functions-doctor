# 🩺 Azure Functions Doctor

**Azure Functions Doctor** is a Python-based CLI tool designed to diagnose and validate your local Azure Functions environment. This tool helps identify configuration issues, missing dependencies, or version mismatches commonly found in Python-based Azure Functions.

## 🚀 Features

* ✅ Diagnose common issues in Azure Functions (`host.json`, `function.json`, directory structure, etc.)
* ✅ Check Python version compatibility and venv usage
* ✅ Validate if Azure Function Core Tools are installed and correctly configured
* ✅ Ensure best practice configurations for Python-based Azure Functions
* ✅ Developer-friendly CLI interface with rich terminal output
* ✅ Built-in linting, type-checking, coverage, and release automation tools

---

## 🪠 Requirements

* Python 3.9+
* Git
* Optional: Azure Function Core Tools v4 (`npm i -g azure-functions-core-tools@4`)
* Recommended: Unix-like shell or PowerShell for Makefile support

---

## 📦 Installation

1. Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/yeongseon/azure-functions-doctor.git
cd azure-functions-doctor
```

2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install the tool:

```bash
pip install -e .
```

Alternatively, install from PyPI (when published):

```bash
pip install azure-functions-doctor
```

---

## 🚀 Usage

Navigate to your Azure Functions project directory, then run:

```bash
$ azfunc-doctor diagnose
```

To see all available commands:

```bash
$ azfunc-doctor --help
```

### ✅ Sample Output

```bash
$ azfunc-doctor diagnose

✖ Python Environment
  • Python version: Current: 3.12.3, Expected: >=3.9
  • Virtual environment: VIRTUAL_ENV is set
  • Python executable: /root/.local/share/hatch/env/virtual/azure-function-doctor/qaLwoID5/azure-function-doctor/bin/python exists
  • requirements.txt: /root/Github/azure-functions-doctor/examples/basic-hello/requirements.txt exists
  • azure-functions package: azure_functions is not installed

✖ Project Structure
  • host.json: /root/Github/azure-functions-doctor/examples/basic-hello/host.json exists
  • local.settings.json: /root/Github/azure-functions-doctor/examples/basic-hello/local.settings.json is missing
  • main.py: /root/Github/azure-functions-doctor/examples/basic-hello/main.py is missing

─────────────────────────────────────────────────────────────────────────────── Summary ────────────────────────────────────────────────────────────────────────────────
✔ 0 Passed    ✖ 2 Failed
```
---

## 💡 Example

A full example is available under [`examples/basic-hello`](examples/basic-hello), showing how to:

* Initialize an Azure Function locally
* Use `azure-functions-doctor` to verify configuration

---

## 📋 Documentation

For advanced usage and developer guides, visit the [project repository](https://github.com/yeongseon/azure-functions-doctor).

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
