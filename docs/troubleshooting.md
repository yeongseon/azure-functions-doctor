# Troubleshooting

This guide provides comprehensive solutions for common issues encountered when installing, using, or developing Azure Functions Doctor. It is designed to help you quickly identify problems and apply the correct fixes.

## Introduction to Troubleshooting

When you encounter an issue, the first step is to identify the specific component or step where the problem occurs. Azure Functions Doctor is designed to provide clear diagnostic information, but some environment-specific configurations may still cause unexpected behavior. This document covers common scenarios and their resolutions.

## Installation Issues

**Problem: Command not found after installation**
**Cause:** The CLI entry points are not in your system PATH.
**Solution:** Check the pip install location for your Python environment. The package registers three entry points: `azure-functions`, `azure-functions-doctor`, and `fdoctor`. If these commands still fail, you can run the tool as a module using `python -m azure_functions_doctor.cli` as a fallback.

**Problem: Python version incompatible**
**Cause:** Azure Functions Doctor requires Python 3.10 or higher.
**Solution:** Verify your current version with `python --version`. If it is below 3.10, install a supported version of Python.

## Diagnostic Issues

**Problem: All checks show "skip"**
**Cause:** You are running the doctor command outside of a valid Azure Functions project directory.
**Solution:** Navigate to your project root or use the `--path` flag to point to the correct directory. The tool looks for specific markers like host.json, requirements.txt, and function_app.py to identify a project.

**Problem: Python version check fails**
**Cause:** The active Python version is not within the supported range for the target runtime.
**Solution:** Azure Functions Python v2 officially supports versions 3.8 through 3.12. Ensure you have activated the correct virtual environment with a compatible Python version.

**Problem: "azure-functions not declared" despite being installed**
**Cause:** The tool checks your requirements.txt file for dependencies rather than checking your installed packages.
**Solution:** Add `azure-functions` to your requirements.txt file to satisfy this check.

**Problem: Virtual environment check warns**
**Cause:** No active virtual environment was detected in the current shell.
**Solution:** Create and activate a virtual environment to isolate your dependencies: `python -m venv .venv && source .venv/bin/activate`.

**Problem: Core Tools check fails**
**Cause:** Azure Functions Core Tools (the func CLI) is either not installed or not available in your PATH.
**Solution:** Install the tools via npm with `npm i -g azure-functions-core-tools@4` or via Homebrew on macOS using `brew tap azure/functions && brew install azure-functions-core-tools@4`. Note that this check is optional.

**Problem: host.json check fails**
**Cause:** Your project is missing a host.json file or the file is malformed.
**Solution:** Ensure a valid host.json exists in your project root. A minimal configuration would be: `{"version": "2.0"}`.

## Output and Format Issues

**Problem: JSON output is not valid JSON**
**Cause:** You are using `--format json` while verbose or debug logging is enabled, which writes additional text to stdout.
**Solution:** Redirect standard error to null or use a shell redirection like `--format json 2>/dev/null` to ensure only the JSON payload is captured.

**Problem: SARIF output errors**
**Cause:** Required fields are missing from the rule definitions used to generate the report.
**Solution:** Verify that all rules include the necessary metadata: id, label, description, hint, and hint_url.

## Custom Rules Issues

**Problem: Custom rules file not loaded**
**Cause:** The rules file contains invalid JSON syntax or does not follow the expected schema.
**Solution:** Validate your JSON file using `python -m json.tool rules.json`. Custom rules must adhere to the same structure as the built-in v2.json configuration.

**Problem: Custom handler not found**
**Cause:** The "type" field in your rule does not match any registered handler in the system.
**Solution:** Check that your rule uses one of the eight supported handler types:
- file_exists
- path_exists
- package_declared
- source_code_contains
- executable_exists
- compare_version
- conditional_exists
- callable_detection

## Profile Issues

**Problem: "Unknown profile" error**
**Cause:** You provided an invalid value to the `--profile` argument.
**Solution:** Use one of the supported profiles: `default` (runs all available rules) or `minimal` (runs only strictly required checks).

## Development Issues

**Problem: make install fails**
**Cause:** Python or pip is not correctly installed or available in your environment.
**Solution:** Ensure you have Python 3.10+ and pip properly configured on your system.

**Problem: Pre-commit hooks fail**
**Cause:** Your changes do not comply with the formatting, linting, or type-checking requirements.
**Solution:** Run `make format` to fix style issues, then execute `make check-all` to verify the codebase before committing.

**Problem: mypy errors on handler functions**
**Cause:** Your handler functions are missing type annotations or have incorrect return types.
**Solution:** All rule handlers must return a dictionary containing "status" and "detail" keys. It is recommended to use the `_create_result()` helper function to ensure consistency.

## CI Issues

**Problem: CI test matrix fails on a specific Python version**
**Cause:** There are behavior differences between Python versions in the test environment.
**Solution:** Investigate if the failure involves deprecated features like `datetime.utcnow()`. You should use `datetime.now(UTC)` instead. Also, verify that your typing syntax is compatible across all versions in the matrix.

## Additional Resources and Support

If you continue to experience problems that are not covered in this guide, please consider the following options:

1. Review the logs for more detailed error messages that may indicate environmental variables or permissions issues.
2. Search through existing GitHub issues for similar reports that may already have community-driven solutions.
3. Check the official Azure Functions documentation for environment-specific guidance related to your operating system or deployment model.
4. Ensure all dependencies listed in your package configuration are up to date and compatible with the latest version of the tool.
5. If you are working in a restricted environment, verify that your network allows access to the necessary package repositories and Azure endpoints.
6. For complex configuration scenarios, consult with your infrastructure or devops team to ensure the runtime environment matches expectations.
7. Use the help command to see all available CLI options and arguments.

## Final Summary and Best Practices

By following these troubleshooting steps, you can resolve most common configuration and execution issues independently. If a bug is suspected, please provide a detailed description of the problem along with the steps required to reproduce it in a new issue report. Providing your project structure and relevant configuration files will help the maintenance team diagnose the problem more efficiently.

This guide is updated periodically as new issues are reported and addressed. If you find a new problem and its solution, please consider contributing to this documentation via a pull request. Maintaining an accurate and helpful troubleshooting guide is a community effort that benefits all users of the tool.

We hope this information helps you get back to productive development with Azure Functions Doctor. For more information, please refer to the main documentation page or the official project repository. Every update to this document helps build a more robust troubleshooting resource for everyone involved.

Thank you for using Azure Functions Doctor and for your commitment to keeping the community documentation accurate and helpful for all developers. Your feedback and contributions are vital to the project.
