from __future__ import annotations

from pathlib import Path
import shutil
import tempfile

from azure_functions_doctor.doctor import Doctor

REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_DIR = REPO_ROOT / "examples" / "v2" / "http-trigger"


def _summarize(results: list[dict[str, object]]) -> tuple[int, int, int]:
    passed = 0
    warnings = 0
    failed = 0

    for section in results:
        for item in section["items"]:
            status = item.get("status")
            if status == "pass":
                passed += 1
            elif status == "warn":
                warnings += 1
            elif status == "fail":
                failed += 1

    return passed, warnings, failed


def _find_item(results: list[dict[str, object]], label: str) -> tuple[str, str]:
    for section in results:
        for item in section["items"]:
            if item.get("label") == label:
                return item.get("status", "unknown"), item.get("value", "")

    return "unknown", "not found"


def _print_case(
    title: str, path: Path, results: list[dict[str, object]], labels: list[str]
) -> None:
    passed, warnings, failed = _summarize(results)
    print(title)
    print(f"Path: {path}")
    print(f"Summary: {passed} passed, {warnings} warnings, {failed} failed")
    for label in labels:
        status, value = _find_item(results, label)
        print(f"[{status}] {label}: {value}")
    print()


def _run_doctor(path: Path) -> list[dict[str, object]]:
    doctor = Doctor(str(path), profile="minimal")
    return doctor.run_all_checks()


def main() -> None:
    good_results = _run_doctor(EXAMPLE_DIR)
    _print_case(
        "Representative example",
        EXAMPLE_DIR,
        good_results,
        ["Programming model v2", "requirements.txt", "azure-functions package", "host.json"],
    )

    with tempfile.TemporaryDirectory(prefix="doctor-demo-") as temp_dir:
        broken_dir = Path(temp_dir) / "http-trigger-broken"
        shutil.copytree(EXAMPLE_DIR, broken_dir)
        (broken_dir / "host.json").unlink()
        (broken_dir / "requirements.txt").write_text("requests==2.32.0\n", encoding="utf-8")

        broken_results = _run_doctor(broken_dir)
        _print_case(
            "Broken copy",
            broken_dir,
            broken_results,
            ["requirements.txt", "azure-functions package", "host.json"],
        )


if __name__ == "__main__":
    main()
