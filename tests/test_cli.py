import json
import xml.etree.ElementTree as ET

from typer.testing import CliRunner

from azure_functions_doctor.cli import cli as app

runner = CliRunner()


def test_cli_table_output() -> None:
    """Test CLI outputs result in table format."""
    result = runner.invoke(app, ["diagnose", "--format", "table"])
    assert result.exit_code == 0
    assert "Azure Functions Doctor" in result.output
    assert any(icon in result.output for icon in ["✔", "✖", "⚠"])


def test_cli_json_output() -> None:
    """Test CLI outputs result in JSON format without extra text."""
    result = runner.invoke(app, ["diagnose", "--format", "json"])
    assert result.exit_code == 0

    # Try to isolate the first JSON array in output
    output_text = result.output.strip()
    try:
        data = json.loads(output_text)
        assert isinstance(data, list)
        assert all("title" in section and "items" in section for section in data)
    except json.JSONDecodeError as err:
        raise AssertionError("Output is not valid JSON") from err


def test_cli_verbose_output() -> None:
    """Test CLI outputs verbose hints when enabled."""
    result = runner.invoke(app, ["diagnose", "--format", "table", "--verbose"])
    assert result.exit_code == 0
    assert "↪" in result.output  # hint indicator


def test_cli_sarif_output() -> None:
    """Test CLI outputs SARIF format."""
    result = runner.invoke(app, ["diagnose", "--format", "sarif"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data.get("version") == "2.1.0"
    assert isinstance(data.get("runs"), list)
    run = data["runs"][0]
    tool = run["tool"]["driver"]
    assert tool["name"] == "azure-functions-doctor"
    assert tool["version"]


def test_cli_junit_output() -> None:
    """Test CLI outputs JUnit format."""
    result = runner.invoke(app, ["diagnose", "--format", "junit"])
    assert result.exit_code == 0
    assert result.output.startswith("<?xml")
    root = ET.fromstring(result.output)
    assert root.tag == "testsuite"
    assert root.attrib.get("name") == "func-doctor"
    tests = int(root.attrib.get("tests", "0"))
    failures = int(root.attrib.get("failures", "0"))
    testcases = root.findall("testcase")
    assert tests == len(testcases)
    assert failures <= tests
    assert all(case.attrib.get("classname") for case in testcases)
    assert all(case.attrib.get("name") for case in testcases)
