# PRD - azure-functions-doctor

## Overview

`azure-functions-doctor` is a diagnostic CLI for projects built on the Azure Functions Python v2
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
