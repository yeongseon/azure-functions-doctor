import json
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.text import Text

from azure_functions_doctor import __version__
from azure_functions_doctor.doctor import Doctor
from azure_functions_doctor.utils import format_detail, format_result, format_status_icon

cli = typer.Typer()
console = Console()


def _write_output(content: str, output: Optional[Path], label: str) -> None:
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(content, encoding="utf-8")
        console.print(f"[green]✓ {label} output saved to:[/green] {output}")
    else:
        print(content)


@cli.command()
def diagnose(
    path: str = ".",
    verbose: bool = False,
    format: Annotated[str, typer.Option(help="Output format: 'table', 'json', 'sarif', or 'junit'")] = "table",
    output: Annotated[Optional[Path], typer.Option(help="Optional path to save output result")] = None,
) -> None:
    """
    Run diagnostics on an Azure Functions application.

    Args:
        path: Path to the Azure Functions app. Defaults to current directory.
        verbose: Show detailed hints for failed checks.
        format: Output format: 'table', 'json', 'sarif', or 'junit'.
        output: Optional file path to save output result.
    """
    supported_formats = {"table", "json", "sarif", "junit"}
    if format not in supported_formats:
        raise typer.BadParameter(f"Invalid format '{format}'. Choose from: {', '.join(sorted(supported_formats))}.")

    doctor = Doctor(path)
    results = doctor.run_all_checks()

    passed = failed = 0

    if format == "json":
        json_output = json.dumps(results, indent=2)
        _write_output(json_output, output, "JSON")
        return

    if format == "sarif":
        sarif_results = []
        for section in results:
            for item in section["items"]:
                if item["status"] == "pass":
                    continue
                level = "error" if item["status"] == "fail" else "warning"
                sarif_results.append(
                    {
                        "ruleId": item["label"],
                        "message": {"text": item["value"]},
                        "level": level,
                    }
                )

        sarif_output = {
            "version": "2.1.0",
            "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": "azure-functions-doctor",
                            "version": __version__,
                        }
                    },
                    "results": sarif_results,
                }
            ],
        }
        _write_output(json.dumps(sarif_output, indent=2), output, "SARIF")
        return

    if format == "junit":
        import xml.etree.ElementTree as ET

        tests = 0
        failures = 0
        suite = ET.Element("testsuite", name="func-doctor", tests="0", failures="0", time="0")

        for section in results:
            for item in section["items"]:
                tests += 1
                case = ET.SubElement(suite, "testcase", classname=section["title"], name=item["label"])
                if item["status"] != "pass":
                    failures += 1
                    failure = ET.SubElement(case, "failure", message=item["value"])
                    failure.text = item.get("hint", "")

        suite.set("tests", str(tests))
        suite.set("failures", str(failures))
        junit_output = ET.tostring(suite, encoding="utf-8", xml_declaration=True).decode("utf-8")
        _write_output(junit_output, output, "JUnit")
        return

    # Print header only for table format
    console.print(f"[bold blue]🩺 Azure Functions Doctor for Python v{__version__}[/bold blue]")
    console.print(f"[bold]📁 Path:[/bold] {Path(path).resolve()}\n")

    # Default: table format
    for section in results:
        console.print(Text.assemble("\n", format_result(section["status"]), " ", (section["title"], "bold")))

        if section["status"] == "pass":
            passed += 1
        else:
            failed += 1

        for item in section["items"]:
            label = item["label"]
            value = item["value"]
            status = item["status"]

            line = Text.assemble(
                ("  • ", "default"),
                (label, "dim"),
                (": ", "default"),
                format_detail(status, value),
            )
            console.print(line)

            if verbose and status != "pass":
                if item.get("hint"):
                    console.print(f"    ↪ [yellow]{item['hint']}[/yellow]")
                hint_url = item.get("hint_url", "")
                if hint_url.strip():
                    console.print(f"    📚 [blue]{hint_url}[/blue]")

    # ✅ Summary section
    console.print()
    console.print("[bold]Summary[/bold]")
    summary = Text.assemble(
        (f"{format_status_icon('pass')} ", "green bold"),
        (f"{passed} Passed    ", "bold"),
        (f"{format_status_icon('fail')} ", "red bold"),
        (f"{failed} Failed", "bold"),
    )
    console.print(summary)


# Explicit command registration (test-friendly)
cli.command()(diagnose)

if __name__ == "__main__":
    cli()
