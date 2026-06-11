"""Output helpers that keep terminal rendering safe on Windows consoles."""
from __future__ import annotations

import sys
from typing import Any

_ASCII_REPLACEMENTS = str.maketrans(
    {
        "—": "-",
        "–": "-",
        "→": "->",
        "×": "x",
        "✓": "[OK]",
        "✔": "[OK]",
        "✗": "[X]",
        "⚠": "[!]",
        "🔋": "[BAT]",
        "🤖": "[BOT]",
        "👋": "",
        "·": "*",
    }
)


def safe_text(value: Any) -> str:
    """Return text that can be printed even on limited terminal encodings."""
    text = str(value).translate(_ASCII_REPLACEMENTS)
    encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
    try:
        text.encode(encoding)
    except UnicodeEncodeError:
        text = text.encode(encoding, errors="replace").decode(encoding)
    return text


def safe_print(*args: Any, sep: str = " ", end: str = "\n") -> None:
    """Print text after normalising unsafe characters for the active console."""
    text = sep.join(safe_text(arg) for arg in args)
    sys.stdout.write(text + end)
