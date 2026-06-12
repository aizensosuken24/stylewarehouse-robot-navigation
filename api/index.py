"""
api/index.py — Vercel serverless entry point.

Vercel looks for a callable named `app` (or `handler`) in this file.
We add the project root to sys.path so that src/, config.py, data/ etc.
are all importable, then re-export the WSGI app from app.py.
"""
import sys, os

# ── Make the project root importable ──────────────────────────────────────────
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# ── Import the WSGI callable ───────────────────────────────────────────────────
from app import app  # noqa: E402  (app is the WSGI callable defined in app.py)
