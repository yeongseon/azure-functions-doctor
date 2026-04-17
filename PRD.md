# PRD - azure-functions-doctor-python

## Overview

`azure-functions-doctor-python` is a diagnostic CLI for projects built on the Azure Functions Python v2
programming model.

It inspects a local project and reports common configuration, dependency, and environment issues
before they surface during local runs or deployment.

## Problem Statement

Azure Functions Python projects can fail for routine reasons that are easy to miss:

- missing `host.json`
- missing or incorrect `azure-functions` dependency
- unsupported Python configuration
- incomplete local development setup
- inconsistent project layout

These failures are often discovered late, through confusing runtime errors or deployment issues.

## Goals

- Provide fast, readable diagnostics for Azure Functions Python v2 projects.
- Surface required and optional checks with clear pass/fail output.
- Support both local CLI use and CI integration.
- Keep checks aligned with representative example projects.

## Non-Goals

- Fixing project issues automatically
- Replacing Azure Functions Core Tools
- Managing deployment workflows
- Supporting the legacy `function.json`-based Python v1 model

## Primary Users

- Maintainers of Azure Functions Python repositories
- Developers setting up local Azure Functions projects
- Teams that want lightweight CI diagnostics for Functions projects

## Core Use Cases

- Run diagnostics against the current project directory
- Run diagnostics against a specific example or target path
- Use a smaller profile for required-only checks
- Consume human-readable or machine-readable output in automation

## Success Criteria

- Representative examples pass diagnostic smoke tests in CI
- Broken example copies fail in predictable ways
- CLI output remains stable enough for user troubleshooting and automation

## Example-First Design

### Philosophy

A diagnostic CLI earns trust by showing exactly what it does. `azure-functions-doctor-python`
ships runnable example projects — both healthy and intentionally broken — so developers
can see real pass/fail output before pointing the tool at their own code.

### Quick Start (Hello World)

Run diagnostics against the representative example:

```bash
pip install azure-functions-doctor-python
azure-functions doctor --path examples/v2/http-trigger
```

Expected output shows a clean diagnostic pass:

```text
Azure Functions Doctor

  [PASS] HOST_JSON_EXISTS
  [PASS] REQUIREMENTS_TXT_EXISTS
  [PASS] AZURE_FUNCTIONS_DEPENDENCY
  [PASS] V2_DECORATORS_USED
  ...

Result: All checks passed
```

Run against a broken example to see clear failure output:

```bash
azure-functions doctor --path examples/v2/broken-missing-host-json
```

### Why Examples Matter

1. **Lower entry barrier.** Developers can run the CLI against bundled examples before
   applying it to their own project. The pass/fail contrast builds confidence.
2. **AI agent discoverability.** Tools like GitHub Copilot, Cursor, and Claude Code recommend
   libraries based on README, PRD, and example content. CLI output samples in documentation
   help AI agents understand what `azure-functions-doctor-python` does and when to suggest it.
3. **Cookbook role.** For niche ecosystems, `examples/` and `docs/` often serve as the primary
   learning material. Both healthy and broken examples teach diagnostic patterns.
4. **Proven approach.** FastAPI, LangChain, SQLAlchemy, and Pandas all achieved early adoption
   through extensive, copy-paste-friendly examples and clear output samples.

### Examples Inventory

| Role | Path | Pattern |
|---|---|---|
| Representative | `examples/v2/http-trigger` | Minimal HTTP trigger (passes all checks) |
| Representative | `examples/v2/timer-trigger` | Timer trigger (passes all checks) |
| Complex | `examples/v2/multi-trigger` | Multiple triggers in one app |
| Complex | `examples/v2/blueprint` | Blueprint-based modular routing |
| Broken | `examples/v2/broken-missing-host-json` | Missing host.json |
| Broken | `examples/v2/broken-missing-requirements` | Missing requirements.txt |
| Broken | `examples/v2/broken-missing-azure-functions` | Missing azure-functions dep |
| Broken | `examples/v2/broken-no-v2-decorators` | No v2 decorators |

All examples are smoke-tested in CI. New diagnostic rules should ship with a corresponding
broken example that demonstrates the failure.
