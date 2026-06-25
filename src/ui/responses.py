"""
UI helpers: standardized API response formatting.
"""

from typing import Any
from flask import jsonify


def success_response(data: Any = None, message: str = "OK", status: int = 200):
    """Return a standardised JSON success response."""
    payload = {"success": True, "message": message}
    if data is not None:
        payload["data"] = data
    return jsonify(payload), status


def error_response(message: str, status: int = 400, details: Any = None):
    """Return a standardised JSON error response."""
    payload = {"success": False, "error": message}
    if details is not None:
        payload["details"] = details
    return jsonify(payload), status


def paginate(items: list, page: int = 1, per_page: int = 20) -> dict:
    """Simple pagination helper."""
    page = max(1, page)
    per_page = max(1, per_page)
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    return {
        "items": items[start:end],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": max(1, (total + per_page - 1) // per_page),
    }
