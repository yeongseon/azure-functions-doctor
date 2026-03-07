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


def _normalize_value(value: str, path_aliases: dict[str, str]) -> str:
    normalized = value.replace(str(REPO_ROOT), ".")
    for source, alias in path_aliases.items():
        normalized = normalized.replace(source, alias)
    return normalized


def _find_item(
    results: list[dict[str, object]], label: str, path_aliases: dict[str, str]
) -> tuple[str, str]:
    for section in results:
        for item in section["items"]:
            if item.get("label") == label:
                return item.get("status", "unknown"), _normalize_value(
                    item.get("value", ""), path_aliases
                )

    return "unknown", "not found"


def _print_case(
    title: str,
    path_label: str,
    results: list[dict[str, object]],
    labels: list[str],
    path_aliases: dict[str, str],
) -> None:
    passed, warnings, failed = _summarize(results)
    print(title)
    print(f"Target: {path_label}")
    print(f"Summary: {passed} passed, {warnings} warnings, {failed} failed")
    for label in labels:
        status, value = _find_item(results, label, path_aliases)
        print(f"[{status}] {label}: {value}")
    print()


def _run_doctor(path: Path) -> list[dict[str, object]]:
    doctor = Doctor(str(path), profile="minimal")
    return doctor.run_all_checks()


def main() -> None:
    good_results = _run_doctor(EXAMPLE_DIR)
    _print_case(
        "Representative example",
        "examples/v2/http-trigger",
        good_results,
        ["Programming model v2", "requirements.txt", "azure-functions package", "host.json"],
        {},
    )

    with tempfile.TemporaryDirectory(prefix="doctor-demo-") as temp_dir:
        broken_dir = Path(temp_dir) / "http-trigger-broken"
        shutil.copytree(EXAMPLE_DIR, broken_dir)
        (broken_dir / "host.json").unlink()
        (broken_dir / "requirements.txt").write_text("requests==2.32.0\n", encoding="utf-8")

        broken_results = _run_doctor(broken_dir)
        _print_case(
            "Broken copy",
            "broken-http-trigger",
            broken_results,
            ["requirements.txt", "azure-functions package", "host.json"],
            {str(broken_dir): "broken-http-trigger"},
        )


if __name__ == "__main__":
    main()
