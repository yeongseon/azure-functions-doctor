from pathlib import Path
from typing import List, Optional

from azure_functions_doctor.doctor import Doctor, SectionResult


def run_diagnostics(path: str, rules_path: Optional[Path] = None) -> List[SectionResult]:
    """
    Run diagnostics on the Azure Functions application at the specified path.

    Args:
        path: The file system path to the Azure Functions application.

    Returns:
        A list of SectionResult containing the results of each diagnostic check.
    """
    return Doctor(path, rules_path=rules_path).run_all_checks()
