# Security

The azure-functions-doctor-python project maintains a commitment to providing a secure tool for diagnosing Azure Functions local development environments. This document outlines the security policies, reporting processes, and the trust model for using and extending the tool.

## Reporting Vulnerabilities

We take security issues seriously. If you discover a vulnerability, please report it through the following channels:

### Preferred: GitHub Security Advisory
The most secure and efficient way to report a vulnerability is through the GitHub Security Advisory system at:
https://github.com/yeongseon/azure-functions-doctor-python/security/advisories/new

### Alternative: Email
You can also report security concerns via email to:
yeongseon.choe@gmail.com

### What to Include
When reporting a vulnerability, please include:
- A clear description of the vulnerability and its potential impact.
- Detailed reproduction steps, including any sample code or configuration files.
- An assessment of the impact on users or environments.
- A suggested fix or mitigation, if you have one.

### Response Timeline
- Initial acknowledgment: Within 48 hours.
- Status updates and triage: Within 7 days.
- Full resolution: We aim to provide a fix or public disclosure within a reasonable timeframe, depending on the severity and complexity of the issue.

### Responsible Disclosure
We ask that you follow responsible disclosure practices. Please do not share information about the vulnerability publicly until we have had a chance to address it and notify affected users.

## Supported Versions

| Version | Supported |
| :--- | :--- |
| Latest release | Yes |
| Older releases | No |

Security fixes are only applied to the most recent stable release. Users are encouraged to stay updated with the latest version.

## Security Scanning

To ensure the integrity of our codebase, we employ several automated security scanning tools:

- **Bandit (1.9.4)**: A static analysis security scanner that identifies common security issues in Python code.
- **Scope**: Scans all files in the `src/` directory while excluding the `tests/` directory to focus on production code.
- **Local Execution**: You can run the security scan locally using `make security` or `hatch run security`.
- **CI Integration**: The `security.yml` workflow runs Bandit on every push and pull request to the main repository.
- **Pre-commit**: Bandit is integrated as a pre-commit hook, ensuring that potential issues are caught before code is committed.

## Security Scope

### Within Scope
- **Diagnostic Rule Integrity**: Rules must not execute arbitrary code. The core logic of the doctor is designed to evaluate state, not provide a platform for execution.
- **Custom Rules Trust Boundary**: When a user specifies a custom `rules.json` path, that file is treated as a trusted input.
- **Network Requests**: The tool makes outbound HTTP requests exclusively to check for updates to Azure Functions Core Tools using the `requests` library.
- **Input Validation**: Path arguments and user-provided inputs are validated to prevent common vulnerabilities like path traversal.
- **Dependency Security**: We monitor our five runtime dependencies (jsonschema, packaging, requests, rich, typer) for known vulnerabilities.

### Out of Scope
- **Diagnosed Project Security**: The security posture of the Azure Functions projects being analyzed is the responsibility of the project owner.
- **Azure Functions Runtime Security**: Issues related to the Azure Functions runtime or platform are managed by Microsoft.
- **Build-time Security**: Security during the build or deployment phase of the projects being checked is outside the scope of this tool.

## Network Behavior

- **Update Checks**: The doctor makes outbound HTTP requests to official registries to compare local Azure Functions Core Tools versions with the latest available releases.
- **Privacy**: No telemetry, analytics, or user data is collected or sent to any remote servers.
- **Resilience**: Network requests are designed to fail gracefully. If a connection cannot be established, the corresponding check will show a "skip" status rather than crashing the tool.

## Custom Rules Trust Model

- **Assumption of Trust**: Custom `rules.json` files provided via the `--rules` flag are assumed to be from a trusted source.
- **User Responsibility**: Users should only load custom rules from sources they trust.
- **Execution Limits**: Custom rules define metadata for checks and cannot execute arbitrary scripts or binary code.
- **Handler Types**: Rule execution is limited to a pre-defined set of built-in handlers (such as `file_exists`, `path_exists`, etc.), which provides a controlled environment for diagnostic logic.

## Security Best Practices for Users

- **Update Frequently**: Keep your installation of `azure-functions-doctor-python` updated to benefit from the latest security patches and rule improvements.
- **Review Custom Rules**: Always review the contents of a custom rules file before using it with the doctor.
- **Automation**: Use the `--format json` output for integration into automated CI/CD pipelines for consistent security and environment checks.
- **GitHub Integration**: Use the SARIF output format to integrate results directly with GitHub Code Scanning.

## Dependency Security

The project relies on a minimal set of five runtime dependencies:
- **jsonschema**: For validating rule files and configurations.
- **packaging**: For handling version comparisons.
- **requests**: For secure outbound HTTP communication.
- **rich**: For formatted terminal output.
- **typer**: For building the command-line interface.

We use Dependabot to monitor these dependencies and provide automated updates for security vulnerabilities and version upgrades. All chosen dependencies are widely-used and actively maintained packages.