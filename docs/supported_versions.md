# Supported Python Versions and Deprecation Policy

## Current Support

Azure Functions Doctor supports **Python 3.10 and above**, consistent with the [Azure Functions Python runtime support](https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python#supported-python-versions).

- **Minimum version**: Python 3.10
- **Tested / supported**: 3.10+ (as reflected in CI)

## Deprecation Policy

- **Alignment with Azure**: Supported Python versions and deprecation timelines follow **Microsoft’s Azure Functions Python runtime support**. When a Python version is no longer supported by the Azure Functions runtime, we will drop support for that version in this tool and update the minimum accordingly.
- **Python 3.10**: We will drop support when Microsoft ends Azure Functions support for Python 3.10.
- **Version checks and docs**: When we change the minimum supported version, we will:
  - Update `requires-python` in `pyproject.toml`
  - Update the version check rules in `src/azure_functions_doctor/assets/rules/` (e.g. `check_python_version`)
  - Update this document and the [README](https://github.com/yeongseon/azure-functions-doctor-for-python/blob/main/README.md) Requirements section
  - Bump the project version per [Release Process](release_process.md)

## References

- [Azure Functions – Supported Python versions](https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python#supported-python-versions)
- [Python release schedule](https://devguide.python.org/versions/)
