"""Smoke tests for the bundled v2 example projects.

Each passing example must satisfy all *required* rule checks.
Each broken example must fail on exactly the one rule it intentionally violates.
"""

from pathlib import Path

import pytest

from azure_functions_doctor.doctor import Doctor

EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "examples" / "v2"

# Required-rule labels (required=True in v2.json) that must pass for every
# healthy example.  Environment-dependent checks (venv, python exe, func CLI)
# are excluded because they depend on the CI machine's setup.
_ALWAYS_PASS_LABELS = {
    "host.json",
    "host.json version",
    "requirements.txt",
    "azure-functions package",
}


def _run_example(example_name: str) -> tuple[Doctor, dict[str, str]]:
    project_path = EXAMPLES_DIR / example_name
    doctor = Doctor(str(project_path))
    results = doctor.run_all_checks()
    item_map = {item["label"]: item["status"] for section in results for item in section["items"]}
    return doctor, item_map


# ---------------------------------------------------------------------------
# Passing examples
# ---------------------------------------------------------------------------


class TestPassingExamples:
    """All four healthy examples must pass every structural required check."""

    @pytest.mark.parametrize(
        "example_name",
        ["http-trigger", "timer-trigger", "multi-trigger", "blueprint"],
    )
    def test_required_checks_pass(self, example_name: str) -> None:
        doctor, item_map = _run_example(example_name)
        assert doctor.programming_model == "v2", (
            f"{example_name}: expected programming_model='v2', got {doctor.programming_model!r}"
        )
        for label in _ALWAYS_PASS_LABELS:
            assert item_map.get(label) == "pass", (
                f"{example_name}: expected '{label}' == 'pass', got {item_map.get(label)!r}"
            )

    def test_http_trigger_is_v2_project(self) -> None:
        doctor, item_map = _run_example("http-trigger")
        assert doctor.programming_model == "v2"
        assert item_map.get("host.json") == "pass"
        assert item_map.get("requirements.txt") == "pass"
        assert item_map.get("azure-functions package") == "pass"
        assert item_map.get("Programming model v2") == "pass"

    def test_timer_trigger_is_v2_project(self) -> None:
        doctor, item_map = _run_example("timer-trigger")
        assert doctor.programming_model == "v2"
        assert item_map.get("host.json") == "pass"
        assert item_map.get("requirements.txt") == "pass"
        assert item_map.get("azure-functions package") == "pass"
        assert item_map.get("Programming model v2") == "pass"

    def test_multi_trigger_is_v2_project(self) -> None:
        doctor, item_map = _run_example("multi-trigger")
        assert doctor.programming_model == "v2"
        assert item_map.get("host.json") == "pass"
        assert item_map.get("requirements.txt") == "pass"
        assert item_map.get("azure-functions package") == "pass"
        assert item_map.get("Programming model v2") == "pass"

    def test_blueprint_is_v2_project(self) -> None:
        doctor, item_map = _run_example("blueprint")
        assert doctor.programming_model == "v2"
        assert item_map.get("host.json") == "pass"
        assert item_map.get("requirements.txt") == "pass"
        assert item_map.get("azure-functions package") == "pass"
        assert item_map.get("Programming model v2") == "pass"


# ---------------------------------------------------------------------------
# Broken examples — each must fail on exactly the intended rule
# ---------------------------------------------------------------------------


class TestBrokenExamples:
    """Broken examples must surface exactly the defect they were designed for."""

    def test_broken_missing_host_json_fails_host_json_check(self) -> None:
        _, item_map = _run_example("broken-missing-host-json")
        assert item_map.get("host.json") == "fail", (
            "broken-missing-host-json: expected 'host.json' == 'fail', "
            f"got {item_map.get('host.json')!r}"
        )

    def test_broken_missing_requirements_fails_requirements_check(self) -> None:
        _, item_map = _run_example("broken-missing-requirements")
        assert item_map.get("requirements.txt") == "fail", (
            "broken-missing-requirements: expected 'requirements.txt' == 'fail', "
            f"got {item_map.get('requirements.txt')!r}"
        )

    def test_broken_missing_azure_functions_fails_package_check(self) -> None:
        _, item_map = _run_example("broken-missing-azure-functions")
        assert item_map.get("azure-functions package") == "fail", (
            "broken-missing-azure-functions: expected 'azure-functions package' == 'fail', "
            f"got {item_map.get('azure-functions package')!r}"
        )

    def test_broken_no_v2_decorators_fails_programming_model_detection(self) -> None:
        _, item_map = _run_example("broken-no-v2-decorators")
        assert item_map.get("Python v2 programming model was not detected") == "fail", (
            "broken-no-v2-decorators: expected undetected v2 programming model failure, "
            f"got {item_map!r}"
        )
