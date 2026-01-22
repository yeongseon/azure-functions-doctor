import json
import os
import shutil
import tempfile
from importlib.resources import files
from pathlib import Path

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


def test_custom_rules_path() -> None:
    """Tests that a custom rules.json path is honored."""
    with tempfile.TemporaryDirectory() as tmp:
        rules = [
            {
                "id": "check_custom_env",
                "category": "environment",
                "section": "custom",
                "label": "Custom env",
                "description": "Checks if CUSTOM_ENV is set.",
                "type": "env_var_exists",
                "required": True,
                "severity": "error",
                "condition": {"target": "CUSTOM_ENV"},
                "hint": "Set CUSTOM_ENV for this check.",
                "check_order": 1,
            }
        ]
        rules_path = Path(tmp) / "rules.json"
        rules_path.write_text(json.dumps(rules), encoding="utf-8")

        results = Doctor(tmp, rules_path=rules_path).run_all_checks()

        assert len(results) == 1
        assert results[0]["items"][0]["label"] == "Custom env"
