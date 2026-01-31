from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from azure_functions_doctor.logging_config import get_logger

logger = get_logger(__name__)


def iter_project_py_contents(path: Path) -> Iterator[tuple[Path, str]]:
    """Yield (py_file, content) for each .py file under path, skipping excluded dirs."""
    excluded_dirs = {".venv", "build", "dist", ".pytest_cache", "__pycache__"}
    for py_file in path.rglob("*.py"):
        if any(part in excluded_dirs for part in py_file.parts):
            continue
        try:
            content = py_file.read_text(encoding="utf-8")
        except PermissionError:
            logger.warning(f"Permission denied reading {py_file}")
            continue
        except UnicodeDecodeError:
            try:
                content = py_file.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
        except (MemoryError, OSError):
            continue
        except Exception as exc:
            logger.debug(f"Skip {py_file}: {exc}")
            continue
        yield py_file, content
