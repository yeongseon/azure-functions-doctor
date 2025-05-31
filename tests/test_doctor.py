import json
import os
import tempfile

from azure_functions_doctor.doctor import Doctor


def test_doctor_checks_pass() -> None:
    """Checks that the Doctor runs all checks and returns results."""
    with tempfile.TemporaryDirectory() as tmp:
        # Create required files
        with open(os.path.join(tmp, "host.json"), "w") as f:
            json.dump({"version": "2.0"}, f)
        with open(os.path.join(tmp, "requirements.txt"), "w") as f:
            f.write("azure-functions==1.13.0")

        doctor = Doctor(tmp)
        results = doctor.run_all_checks()

        assert isinstance(results, list)
        assert all("title" in section and "items" in section for section in results)

        item_map = {item["label"]: item["status"] for section in results for item in section["items"]}

        assert "Python version" in item_map
        assert item_map.get("host.json") == "pass"
        assert item_map.get("requirements.txt") == "pass"


def test_missing_files() -> None:
    """Checks that missing files are detected as failures."""
    with tempfile.TemporaryDirectory() as tmp:
        doctor = Doctor(tmp)
        results = doctor.run_all_checks()

        item_map = {item["label"]: item["status"] for section in results for item in section["items"]}

        assert item_map.get("host.json") == "fail"
        assert item_map.get("requirements.txt") == "fail"
