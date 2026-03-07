from pathlib import Path

from azure_functions_doctor.doctor import Doctor

EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "examples" / "v2"


def test_doctor_examples_are_detected_as_v2_projects() -> None:
    for example_name in ("http-trigger", "multi-trigger"):
        project_path = EXAMPLES_DIR / example_name
        doctor = Doctor(str(project_path))
        results = doctor.run_all_checks()
        item_map = {
            item["label"]: item["status"] for section in results for item in section["items"]
        }

        assert doctor.programming_model == "v2"
        assert item_map.get("host.json") == "pass"
        assert item_map.get("requirements.txt") == "pass"
