"""
Configuration for Speckit Warehouse Robot System.
All environment-sensitive settings are loaded from environment variables
with safe defaults for local development.
"""
import os
from pathlib import Path

# ── Project root ───────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent

# ── Data paths ─────────────────────────────────────────────────────────────────
DATA_DIR = BASE_DIR / "data"
WAREHOUSE_LAYOUT_PATH = str(DATA_DIR / "warehouse_layout.json")
ITEM_CATALOGUE_PATH   = str(DATA_DIR / "item_catalogue.csv")

# ── Server ─────────────────────────────────────────────────────────────────────
HOST  = os.getenv("HOST", "0.0.0.0")
PORT  = int(os.getenv("PORT", 5000))
DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"

# ── CORS ───────────────────────────────────────────────────────────────────────
# In production, set FRONTEND_URL to your Vercel deployment URL
FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:3000"          # local dev default
)

# Comma-separated list of allowed origins (overrides FRONTEND_URL if set)
_extra_origins = os.getenv("ALLOWED_ORIGINS", "")
ALLOWED_ORIGINS = (
    [o.strip() for o in _extra_origins.split(",") if o.strip()]
    if _extra_origins
    else [FRONTEND_URL, "http://localhost:5173", "http://127.0.0.1:5000"]
)

# ── Grid defaults ──────────────────────────────────────────────────────────────
GRID_WIDTH  = int(os.getenv("GRID_WIDTH",  20))
GRID_HEIGHT = int(os.getenv("GRID_HEIGHT", 20))

# ── Robot defaults ─────────────────────────────────────────────────────────────
LOW_BATTERY_THRESHOLD = float(os.getenv("LOW_BATTERY_THRESHOLD", 20.0))
