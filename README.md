# Azure Functions Doctor

[![PyPI](https://img.shields.io/pypi/v/azure-functions-doctor.svg)](https://pypi.org/project/azure-functions-doctor/)
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)](https://pypi.org/project/azure-functions-doctor/)
[![CI](https://github.com/yeongseon/azure-functions-doctor/actions/workflows/ci-test.yml/badge.svg)](https://github.com/yeongseon/azure-functions-doctor/actions/workflows/ci-test.yml)
[![Release](https://github.com/yeongseon/azure-functions-doctor/actions/workflows/release.yml/badge.svg)](https://github.com/yeongseon/azure-functions-doctor/actions/workflows/release.yml)
[![Security Scans](https://github.com/yeongseon/azure-functions-doctor/actions/workflows/security.yml/badge.svg)](https://github.com/yeongseon/azure-functions-doctor/actions/workflows/security.yml)
[![codecov](https://codecov.io/gh/yeongseon/azure-functions-doctor/branch/main/graph/badge.svg)](https://codecov.io/gh/yeongseon/azure-functions-doctor)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://pre-commit.com/)
[![Docs](https://img.shields.io/badge/docs-gh--pages-blue)](https://yeongseon.github.io/azure-functions-doctor/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Read this in: [한국어](README.ko.md) | [日本語](README.ja.md) | [简体中文](README.zh-CN.md)


Azure Functions Doctor is a diagnostic CLI for projects built on the **Azure Functions Python v2 programming model**.

It checks a local project for common issues such as:

- unsupported Python versions
- missing `host.json` or `requirements.txt`
- missing `azure-functions` dependency
- missing virtual environments
- missing Azure Functions Core Tools
- incomplete local development setup

## Why Use It

Setting up an Azure Functions Python project involves multiple configuration files, dependencies, and tooling. Missing any one of them leads to confusing runtime errors. `azure-functions-doctor` checks your project against a curated ruleset and reports issues before they reach production.

## Scope

This repository targets the decorator-based Azure Functions Python v2 programming model only.

- Supported model: `func.FunctionApp()` with decorators such as `@app.route()`
- Unsupported model: legacy `function.json`-based Python v1 projects

## Installation

From PyPI:

```bash
pip install azure-functions-doctor
```

From source:

```bash
git clone https://github.com/yeongseon/azure-functions-doctor.git
cd azure-functions-doctor
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Quick Start

Run the doctor in the current project:

```bash
azure-functions doctor
```

Run against a specific project:

```bash
azure-functions doctor --path ./examples/v2/http-trigger
```

Use a required-only profile:

```bash
azure-functions doctor --profile minimal
```

Output JSON for CI:

```bash
azure-functions doctor --format json
```

## Demo

The demo below is generated from [`demo/doctor-demo.tape`](demo/doctor-demo.tape) with VHS.
It runs the real `azure-functions doctor` CLI against the representative example
and then against an intentionally broken copy to show the pass/fail contrast.

![Doctor demo](docs/assets/doctor-demo.gif)

The final terminal state is also captured as a static image for quick inspection.

![Doctor final output](docs/assets/doctor-demo-final.png)

## Features

The default ruleset includes checks for:

- Azure Functions Python v2 decorator usage
- Python version
- virtual environment activation
- Python executable availability
- `requirements.txt`
- `azure-functions` dependency declaration
- `host.json`
- `local.settings.json` (optional)
- Azure Functions Core Tools presence and version (optional)
- Durable Functions host configuration (optional)
- Application Insights configuration (optional)
- `extensionBundle` configuration (optional)
- ASGI/WSGI callable exposure (optional)
- common unwanted files in the project tree (optional)

## Examples

- [examples/v2/http-trigger/README.md](examples/v2/http-trigger/README.md)
- [examples/v2/multi-trigger/README.md](examples/v2/multi-trigger/README.md)

## Requirements

- Python 3.10+
- Hatch for development workflows
- Azure Functions Core Tools v4+ recommended for local runs

## Documentation

- [docs/index.md](docs/index.md)
- [docs/usage.md](docs/usage.md)
- [docs/rules.md](docs/rules.md)
- [docs/diagnostics.md](docs/diagnostics.md)
- [docs/development.md](docs/development.md)

## Ecosystem

- [azure-functions-validation](https://github.com/yeongseon/azure-functions-validation) — Request and response validation
- [azure-functions-openapi](https://github.com/yeongseon/azure-functions-openapi) — OpenAPI and Swagger UI
- [azure-functions-logging](https://github.com/yeongseon/azure-functions-logging) — Structured logging
- [azure-functions-scaffold](https://github.com/yeongseon/azure-functions-scaffold) — Project scaffolding
- [azure-functions-python-cookbook](https://github.com/yeongseon/azure-functions-python-cookbook) — Recipes and examples

## Disclaimer

This project is an independent community project and is not affiliated with,
endorsed by, or maintained by Microsoft.

Azure and Azure Functions are trademarks of Microsoft Corporation.

## License

MIT
