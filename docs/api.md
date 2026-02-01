# API Reference

This project is primarily a CLI tool. The Python modules are stable enough to be imported,
but the public surface is intentionally small.

Key modules:

- `azure_functions_doctor.cli`: Typer CLI entrypoint and output formats
- `azure_functions_doctor.doctor`: orchestration and rule loading
- `azure_functions_doctor.handlers`: rule handlers / checks
- `azure_functions_doctor.target_resolver`: resolves runtime targets (Python, Core Tools)
- `azure_functions_doctor.utils`: small formatting helpers

Source:

- `src/azure_functions_doctor/`
