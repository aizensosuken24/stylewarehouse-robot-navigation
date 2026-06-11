"""Simple i18n loader for the project.

This minimal implementation loads JSON translation files from
`src/i18n/translations/{lang}.json` and provides a `translate` helper.
Supports: 'en' (default), 'hi' (Hindi), 'te' (Telugu).
"""
from __future__ import annotations
import json
import os
from typing import Dict

_CACHE: Dict[str, Dict[str, str]] = {}


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
    """Return the translated string for `key` or the key itself as fallback."""
    if lang == "en":
        return key
    data = _load_lang(lang)
    return data.get(key, key)
