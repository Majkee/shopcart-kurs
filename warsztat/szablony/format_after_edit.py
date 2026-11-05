"""Hook PostToolUse: formatuje edytowany plik .py ruffem.

Działa po każdym Edit/Write. Nigdy nie blokuje (zawsze kod wyjścia 0).
"""

import importlib.util
import json
import shutil
import subprocess
import sys


def ruff_command() -> list[str] | None:
    if importlib.util.find_spec("ruff") is not None:
        return [sys.executable, "-m", "ruff"]
    binary = shutil.which("ruff")
    return [binary] if binary else None


def main() -> int:
    payload = json.load(sys.stdin)
    path = payload.get("tool_input", {}).get("file_path", "")
    ruff = ruff_command()
    if path.endswith(".py") and ruff:
        subprocess.run([*ruff, "format", path], capture_output=True)
        subprocess.run([*ruff, "check", "--fix", path], capture_output=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
