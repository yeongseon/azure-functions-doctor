import json
import os
import shutil
import tempfile
from importlib.resources import files

from azure_functions_doctor.doctor import Doctor


def test_doctor_checks_pass() -> None:
    """Tests that the Doctor class runs checks and returns results."""
    with tempfile.TemporaryDirectory() as tmp:
        # Copy embedded rules.json
        rules_path = files("azure_functions_doctor.assets").joinpath("rules.json")
        shutil.copy(str(rules_path), os.path.join(tmp, "rules.json"))

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
    """Tests that the Doctor class detects missing files."""
    with tempfile.TemporaryDirectory() as tmp:
        rules_path = files("azure_functions_doctor.assets").joinpath("rules.json")
        shutil.copy(str(rules_path), os.path.join(tmp, "rules.json"))

        doctor = Doctor(tmp)
        results = doctor.run_all_checks()

        item_map = {item["label"]: item["status"] for section in results for item in section["items"]}

        assert item_map.get("host.json") == "fail"
        assert item_map.get("requirements.txt") == "fail"


def test_profile_minimal_filters_optional_rules() -> None:
    """Tests that the minimal profile excludes optional rules."""
    with tempfile.TemporaryDirectory() as tmp:
        rules_path = files("azure_functions_doctor.assets").joinpath("rules.json")
        shutil.copy(str(rules_path), os.path.join(tmp, "rules.json"))

        with open(os.path.join(tmp, "host.json"), "w") as f:
            json.dump({"version": "2.0"}, f)
        with open(os.path.join(tmp, "requirements.txt"), "w") as f:
            f.write("azure-functions==1.13.0")

        doctor = Doctor(tmp, profile="minimal")
        results = doctor.run_all_checks()

        item_labels = {item["label"] for section in results for item in section["items"]}
        assert "local.settings.json" not in item_labels


def test_invalid_profile_raises() -> None:
    """Tests that an invalid profile raises a ValueError."""
    with tempfile.TemporaryDirectory() as tmp:
        rules_path = files("azure_functions_doctor.assets").joinpath("rules.json")
        shutil.copy(str(rules_path), os.path.join(tmp, "rules.json"))

        doctor = Doctor(tmp, profile="unknown")
        try:
            doctor.run_all_checks()
        except ValueError as exc:
            assert "Profile must be 'minimal' or 'full'" in str(exc)
        else:
            raise AssertionError("Expected ValueError for invalid profile")
