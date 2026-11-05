"""Hook PreToolUse: blokuje edycję chronionych plików.

Claude Code przekazuje na stdin JSON z polami tool_name i tool_input.
Kod wyjścia 2 blokuje akcję, a tekst ze stderr trafia do Claude jako wyjaśnienie.
Kod wyjścia 0 oznacza: brak sprzeciwu (dalej decydują zwykłe uprawnienia).
"""

import json
import sys

PROTECTED = [".env", "data/", ".git/"]


def main() -> int:
    payload = json.load(sys.stdin)
    path = payload.get("tool_input", {}).get("file_path", "").replace("\\", "/")
    for pattern in PROTECTED:
        if pattern in path:
            print(
                f"Zablokowano: {path} jest chroniony (reguła '{pattern}'). "
                "Dane i sekrety zmienia tylko człowiek.",
                file=sys.stderr,
            )
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
