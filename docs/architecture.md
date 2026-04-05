# Architecture

This document explains how `azure-functions-doctor` is structured internally and why key design choices support deterministic, actionable diagnostics.

## Design Objectives

The package is intentionally focused:

- Keep diagnostics rule-driven and data-defined (JSON rule assets, not hardcoded checks).
- Preserve exit-code-based CI integration as a first-class concern.
- Add invocation context without requiring heavy runtime dependencies.
- Stay dependency-light and operationally predictable.

## High-Level Components

Core modules and responsibilities:

- `__init__.py`: public exports and version string.
- `cli.py`: Typer-based CLI entrypoint; maps flags to `Doctor` options.
- `doctor.py`: `Doctor` runner — loads rules, executes handlers, aggregates results.
- `handlers.py`: `Rule` type, `generic_handler`, type-based rule dispatch via `HandlerRegistry`.
- `config.py`: configuration management (reserved for future use; not yet in the runtime path).
- `target_resolver.py`: resolves runtime values (Python version, Core Tools version) for version-comparison checks.
- `logging_config.py`: internal logging setup.
- `schemas/`: JSON schema definitions for rule assets and output contracts.
- `assets/`: built-in rule inventory (e.g. `rules/v2.json`).

## Public API Boundary

Public symbols intentionally kept small:

- `Doctor`
- `__version__`
- `run_diagnostics()` (from `api.py` — programmatic entrypoint)

CLI is the primary consumer. Python import use is for programmatic embedding only.

## Diagnostic Pipeline

`Doctor.run_all_checks()` is the entrypoint for a full diagnostic scan.

Execution flow:

1. Load rule asset (`assets/rules/v2.json`) or custom `rules_path`.
2. Validate rule asset against JSON schema.
3. Apply profile filter if `--profile` is given.
4. Dispatch each rule to its handler by the rule's `type` field.
5. Aggregate `SectionResult` list with per-item `CheckResult` entries.
6. Return structured result dict with overall pass/fail status.

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant CLI as cli.py
    participant DOC as Doctor
    participant RULES as assets/v2.json
    participant HDLR as handlers.py
    participant TR as target_resolver.py

    Dev->>CLI: fdoctor doctor ./my-project
    CLI->>DOC: Doctor(path, profile, rules_path)
    DOC->>RULES: load + schema-validate rules
    DOC->>DOC: apply profile filter
    loop each rule
        DOC->>HDLR: dispatch rule by type
        HDLR->>TR: resolve version targets (if needed)
        TR-->>HDLR: resolved value
        HDLR-->>DOC: CheckResult
    end
    DOC-->>CLI: SectionResult[] + pass/fail status
    CLI-->>Dev: formatted output (table/json/sarif/junit)
```

## Rule Asset Design

Rules are data, not code:

- Each rule is a JSON object with `id`, `category`, `label`, `check`, and optional `hint`.
- Handlers interpret the `check` field against the target project.
- New checks can be added without touching Python logic.

See [Rule Inventory](rule_inventory.md) and [RULE_POLICY](RULE_POLICY.md) for the full rule catalogue.

## Exit Code Contract

The CLI follows a strict exit code contract:

| Exit code | Meaning |
|---|---|
| `0` | All checks passed |
| `1` | One or more checks failed |
| `2` | Usage error (bad arguments) |

CI pipelines can rely on these codes directly. See [JSON Output Contract](json_output_contract.md) for structured output.

## Profile System

Profiles allow subsets of rules:

- Profiles are TOML files that list rule IDs to include or exclude.
- `--minimal` selects the built-in minimal profile.
- Custom profiles enable per-team or per-environment gate configurations.

See [Configuration](configuration.md) and [Minimal Profile](minimal_profile.md).

## Related Documents

- [Usage Guide](usage.md)
- [Configuration](configuration.md)
- [Rules](rules.md)
- [Diagnostics](diagnostics.md)
- [Troubleshooting](troubleshooting.md)

## Module Boundaries

```mermaid
flowchart TD
    CLI["cli.py\nTyper CLI"]
    DOC["doctor.py\nDoctor runner"]
    HDLR["handlers.py\nRule dispatch + generic_handler"]
    TR["target_resolver.py\nVersion resolution"]
    RULES[("assets/\nRule inventory")]
    SCHEMAS[("schemas/\nJSON schemas")]
    LOG["logging_config.py\nInternal logging"]

    CLI --> DOC
    DOC --> HDLR
    DOC --> RULES
    DOC --> SCHEMAS
    HDLR --> TR
    CLI --> LOG
    DOC --> LOG
```

## Sources

- [Azure Functions Python developer reference](https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python)
- [Azure Functions host.json reference](https://learn.microsoft.com/en-us/azure/azure-functions/functions-host-json)
- [Supported languages in Azure Functions](https://learn.microsoft.com/en-us/azure/azure-functions/supported-languages)

## See Also

- [azure-functions-validation — Architecture](https://github.com/yeongseon/azure-functions-validation) — Request/response validation pipeline
- [azure-functions-openapi — Architecture](https://github.com/yeongseon/azure-functions-openapi) — OpenAPI spec generation
- [azure-functions-logging — Architecture](https://github.com/yeongseon/azure-functions-logging) — Structured logging with contextvars
- [azure-functions-scaffold — Architecture](https://github.com/yeongseon/azure-functions-scaffold) — Project scaffolding CLI
- [azure-functions-langgraph — Architecture](https://github.com/yeongseon/azure-functions-langgraph) — LangGraph agent deployment
