from pathlib import Path

from azure_functions_doctor.doctor import Doctor

EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "examples" / "v2"


def _run_example(example_name: str) -> tuple[Doctor, dict[str, str]]:
    project_path = EXAMPLES_DIR / example_name
    doctor = Doctor(str(project_path))
    results = doctor.run_all_checks()
    item_map = {item["label"]: item["status"] for section in results for item in section["items"]}
    return doctor, item_map


def test_representative_example_is_detected_as_v2_project() -> None:
    doctor, item_map = _run_example("http-trigger")

    assert doctor.programming_model == "v2"
    assert item_map.get("host.json") == "pass"
    assert item_map.get("requirements.txt") == "pass"


def test_complex_example_is_detected_as_v2_project() -> None:
    doctor, item_map = _run_example("multi-trigger")

    assert doctor.programming_model == "v2"
    assert item_map.get("host.json") == "pass"
    assert item_map.get("requirements.txt") == "pass"
