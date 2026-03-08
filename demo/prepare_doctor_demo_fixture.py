from __future__ import annotations

from pathlib import Path
import shutil

REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_DIR = REPO_ROOT / "examples" / "v2" / "http-trigger"
PREVIEW_DIR = REPO_ROOT / "demo" / ".preview"
BROKEN_DIR = PREVIEW_DIR / "broken-http-trigger"


def main() -> None:
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    if BROKEN_DIR.exists():
        shutil.rmtree(BROKEN_DIR)

    shutil.copytree(EXAMPLE_DIR, BROKEN_DIR)
    (BROKEN_DIR / "host.json").unlink()
    (BROKEN_DIR / "requirements.txt").write_text("requests==2.32.0\n", encoding="utf-8")

    print(BROKEN_DIR)


if __name__ == "__main__":
    main()
