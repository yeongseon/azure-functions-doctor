from typing import List, Optional

from azure_functions_doctor.doctor import Doctor, SectionResult


def run_diagnostics(path: str, profile: Optional[str] = None) -> List[SectionResult]:
    """
    Run diagnostics on the Azure Functions application at the specified path.

    Args:
        path: The file system path to the Azure Functions application.
        profile: Optional rule profile ('minimal' or 'full').

    Returns:
        A list of SectionResult containing the results of each diagnostic check.
    """
    return Doctor(path, profile=profile).run_all_checks()
