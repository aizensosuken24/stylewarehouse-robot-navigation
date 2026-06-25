"""
main.py - CLI entry point for local development.
Run: python main.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from server import app
import config

if __name__ == "__main__":
    print(f"Starting Smart-Robo Nav API on http://{config.HOST}:{config.PORT}")
    app.run(host=config.HOST, port=config.PORT, debug=True)
