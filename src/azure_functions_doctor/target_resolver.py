import shutil
import subprocess  # nosec B404
import sys
from typing import Optional

from azure_functions_doctor.logging_config import get_logger

logger = get_logger(__name__)


def resolve_target_value(target: str, override: Optional[str] = None) -> str:
    """
    Resolve the current value of a target used in version comparison or diagnostics.

    Args:
        target: The name of the target to resolve. Examples include "python" or "func_core_tools".

    Returns:
        A string representing the resolved version or value.

    Raises:
        ValueError: If the target is not recognized.
    """
    if target == "python":
        return override if override is not None else sys.version.split()[0]
    if target == "func_core_tools":
        func_path = shutil.which("func")
        if not func_path:
            logger.debug("Azure Functions Core Tools not found in PATH")
            return "not_installed"
        try:
            output = subprocess.check_output([func_path, "--version"], text=True, timeout=10)  # nosec B603
            return output.strip()
        except FileNotFoundError:
            logger.debug("Azure Functions Core Tools executable disappeared before execution")
            return "not_installed"
        except subprocess.TimeoutExpired:
            logger.warning("Timeout getting func version")
            return "timeout"
        except TimeoutError:
            logger.warning("Timeout getting func version")
            return "timeout"
        except subprocess.CalledProcessError as e:
            logger.warning(f"func command failed with code {e.returncode}")
            return f"error_{e.returncode}"
        except Exception as exc:
            logger.error(f"Unexpected error getting func version: {exc}")
            return "unknown_error"
    raise ValueError(f"Unknown target: {target}")
