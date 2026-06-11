"""Simple i18n loader for the project."""
from __future__ import annotations
import json
import os
from typing import Dict

_CACHE: Dict[str, Dict[str, str]] = {}
_EN_TRANSLATIONS: Dict[str, str] = {
    "app_title": "StyleWarehouse Robot Navigation",
    "pygame_missing": "pygame is not installed: pip install pygame",
    "step_info": "Step {step}/{total}  position={pos}",
    "terminal_fallback": "Falling back to terminal mode.",
    "generate_error_no_ai": "No AI backend is available.",
}


def _load_lang(lang: str) -> Dict[str, str]:
    if lang in _CACHE:
        return _CACHE[lang]
    base = os.path.dirname(__file__)
    path = os.path.join(base, "translations", f"{lang}.json")
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        data = {}
    _CACHE[lang] = data
    return data


def translate(key: str, lang: str = "en") -> str:
    """Return the translated string for ``key`` with English fallback."""
    if lang == "en":
        return _EN_TRANSLATIONS.get(key, key)
    data = _load_lang(lang)
    return data.get(key, _EN_TRANSLATIONS.get(key, key))
