"""Deployment-friendly WSGI app for local, Vercel, and Render use."""
from __future__ import annotations

import json
import os
from http import HTTPStatus
from io import BytesIO
from pathlib import Path
from typing import Dict, Iterable, List, Tuple
from urllib.parse import parse_qs

from config import ALGORITHM, CATALOGUE_FILE
from main import DEMO_ORDER
from src.robot.order import Order
from src.robot.robot import Robot
from src.warehouse.catalogue import Item, ItemCatalogue
from src.warehouse.map import build_default_map

Headers = List[Tuple[str, str]]
PUBLIC_DIR = Path(__file__).parent / "public"


def _build_catalogue() -> ItemCatalogue:
    catalogue = ItemCatalogue()
    catalogue.load_from_csv(CATALOGUE_FILE)
    return catalogue


def _build_robot() -> Tuple[Robot, ItemCatalogue]:
    warehouse_map = build_default_map()
    catalogue = _build_catalogue()
    robot = Robot("DeployBot", warehouse_map, catalogue)
    return robot, catalogue


def _item_to_dict(item: Item) -> Dict[str, object]:
    # Convert grid coordinates to location string (e.g., "A1")
    row_char = chr(65 + int(item.grid_row)) if isinstance(item.grid_row, int) else str(item.grid_row)
    col_num = int(item.grid_col) if isinstance(item.grid_col, int) else item.grid_col
    location = f"{row_char}{col_num}"
    
    return {
        "id": item.sku,
        "sku": item.sku,
        "name": item.name,
        "category": item.category,
        "brand": item.brand,
        "size": item.size,
        "colour": item.colour,
        "location": location,
        "quantity": item.quantity,
    }


def _json_response(start_response, status: HTTPStatus, payload: Dict[str, object]) -> Iterable[bytes]:
    body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
    headers: Headers = [
        ("Content-Type", "application/json; charset=utf-8"),
        ("Content-Length", str(len(body))),
        ("Access-Control-Allow-Origin", "*"),
    ]
    start_response(f"{status.value} {status.phrase}", headers)
    return [body]


def _text_response(start_response, status: HTTPStatus, body: str) -> Iterable[bytes]:
    encoded = body.encode("utf-8")
    headers: Headers = [
        ("Content-Type", "text/html; charset=utf-8"),
        ("Content-Length", str(len(encoded))),
        ("Access-Control-Allow-Origin", "*"),
    ]
    start_response(f"{status.value} {status.phrase}", headers)
    return [encoded]


def _serve_static_file(start_response, file_path: Path) -> Iterable[bytes]:
    """Serve a static file from the public directory."""
    if not file_path.exists() or not file_path.is_file():
        return _json_response(
            start_response,
            HTTPStatus.NOT_FOUND,
            {"ok": False, "error": "File not found"},
        )

    try:
        content = file_path.read_bytes()
        # Determine content type
        suffix = file_path.suffix.lower()
        content_type = {
            ".html": "text/html; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
            ".json": "application/json; charset=utf-8",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".svg": "image/svg+xml",
            ".ico": "image/x-icon",
        }.get(suffix, "application/octet-stream")

        headers: Headers = [
            ("Content-Type", content_type),
            ("Content-Length", str(len(content))),
            ("Cache-Control", "public, max-age=3600"),
        ]
        start_response("200 OK", headers)
        return [content]
    except Exception as e:
        return _json_response(
            start_response,
            HTTPStatus.INTERNAL_SERVER_ERROR,
            {"ok": False, "error": str(e)},
        )


def _read_json_body(environ) -> Dict[str, object]:
    raw_length = environ.get("CONTENT_LENGTH", "").strip()
    length = int(raw_length) if raw_length.isdigit() else 0
    body = environ.get("wsgi.input", BytesIO()).read(length) if length else b""
    if not body:
        return {}
    return json.loads(body.decode("utf-8"))


def _simulate_order(order_id: str, lines: List[Tuple[str, int]]) -> Dict[str, object]:
    robot, catalogue = _build_robot()
    order = Order(order_id, lines)
    success = robot.execute_order(order, verbose=False)
    
    # Format location from coordinates
    start_pos = robot.position if hasattr(robot, 'position') else (0, 0)
    start_row_char = chr(65 + int(start_pos[0])) if isinstance(start_pos[0], int) else "A"
    start_col = int(start_pos[1]) if isinstance(start_pos[1], int) else 0
    start_location = f"{start_row_char}{start_col}"
    
    # Format items with location strings
    items = []
    for sku in order.picked_skus():
        item = catalogue.find(sku)
        if item:
            row_char = chr(65 + int(item.grid_row)) if isinstance(item.grid_row, int) else str(item.grid_row)
            col_num = int(item.grid_col) if isinstance(item.grid_col, int) else item.grid_col
            location = f"{row_char}{col_num}"
            items.append({
                "id": sku,
                "sku": sku,
                "name": item.name,
                "location": location,
            })
    
    # Format path as coordinates
    path = []
    if hasattr(robot, 'log') and robot.log:
        # Extract positions from the log if available
        for log_entry in robot.log:
            if isinstance(log_entry, str) and '->' in log_entry:
                # Parse something like "A0 -> A1"
                parts = log_entry.split('->')
                if len(parts) == 2:
                    start_str = parts[0].strip()
                    if start_str and len(start_str) >= 2:
                        try:
                            row = ord(start_str[0]) - 65
                            col = int(start_str[1:])
                            path.append({"x": col, "y": row})
                        except (ValueError, IndexError):
                            pass
    
    return {
        "ok": success,
        "order_id": order.order_id,
        "algorithm": "A* Pathfinding + TSP",
        "requested_lines": [{"sku": sku, "quantity": quantity} for sku, quantity in lines],
        "items": items,
        "start_position": start_location,
        "end_position": start_location,
        "total_distance": float(robot.total_steps) if hasattr(robot, 'total_steps') else 0,
        "path": path,
        "robot": {
            "name": robot.name,
            "position": list(robot.position) if hasattr(robot, 'position') else [0, 0],
            "battery": robot.battery if hasattr(robot, 'battery') else 100,
            "total_steps": robot.total_steps if hasattr(robot, 'total_steps') else 0,
            "carrying": robot.carrying if hasattr(robot, 'carrying') else 0,
        },
        "catalogue_size": len(catalogue),
        "execution_time": 0.0,
    }


def _normalise_lines(payload: Dict[str, object]) -> List[Tuple[str, int]]:
    if isinstance(payload.get("items"), list):
        lines: List[Tuple[str, int]] = []
        for item in payload["items"]:
            if not isinstance(item, dict) or "sku" not in item:
                continue
            sku = str(item["sku"]).upper()
            quantity = int(item.get("quantity", 1))
            lines.append((sku, max(quantity, 1)))
        return lines

    if isinstance(payload.get("skus"), list):
        return [(str(sku).upper(), 1) for sku in payload["skus"]]

    return []


def _homepage() -> str:
    return """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>StyleWarehouse Robot Navigation</title>
    <style>
      :root {
        color-scheme: light;
        --bg: #f4efe7;
        --card: #fffaf3;
        --ink: #17313b;
        --accent: #d15a39;
      }
      body {
        margin: 0;
        font-family: Georgia, "Times New Roman", serif;
        background: radial-gradient(circle at top, #fff8ef 0, var(--bg) 60%);
        color: var(--ink);
      }
      main {
        max-width: 760px;
        margin: 0 auto;
        padding: 48px 24px;
      }
      .card {
        background: var(--card);
        border: 1px solid rgba(23, 49, 59, 0.12);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 18px 48px rgba(23, 49, 59, 0.08);
      }
      h1 {
        margin-top: 0;
        font-size: clamp(2rem, 6vw, 3.4rem);
        line-height: 1;
      }
      p, li {
        font-size: 1.05rem;
        line-height: 1.6;
      }
      code {
        color: var(--accent);
        font-weight: 700;
      }
    </style>
  </head>
  <body>
    <main>
      <section class="card">
        <h1>StyleWarehouse Robot Navigation</h1>
        <p>A deployable warehouse robot demo powered by A* pathfinding and route sequencing.</p>
        <p>Useful endpoints:</p>
        <ul>
          <li><code>/api/health</code></li>
          <li><code>/api/catalogue</code></li>
          <li><code>/api/catalogue?search=tee</code></li>
          <li><code>/api/catalogue/SW001</code></li>
          <li><code>/api/demo-order</code></li>
          <li><code>POST /api/simulate-order</code></li>
        </ul>
      </section>
    </main>
  </body>
</html>
"""


def app(environ, start_response):
    """WSGI application entrypoint."""
    method = environ.get("REQUEST_METHOD", "GET").upper()
    path = environ.get("PATH_INFO", "/") or "/"
    query = parse_qs(environ.get("QUERY_STRING", ""), keep_blank_values=False)

    if method == "OPTIONS":
        start_response(
            "204 No Content",
            [
                ("Access-Control-Allow-Origin", "*"),
                ("Access-Control-Allow-Methods", "GET,POST,OPTIONS"),
                ("Access-Control-Allow-Headers", "Content-Type"),
                ("Content-Length", "0"),
            ],
        )
        return [b""]

    # Serve static files
    if path.startswith("/css/") or path.startswith("/js/"):
        file_path = PUBLIC_DIR / path.lstrip("/")
        return _serve_static_file(start_response, file_path)

    # Serve index.html for root and HTML requests
    if path == "/" or path == "/index.html":
        file_path = PUBLIC_DIR / "index.html"
        if file_path.exists():
            return _serve_static_file(start_response, file_path)
        # Fallback to legacy homepage
        return _text_response(start_response, HTTPStatus.OK, _homepage())

    if path in {"/health", "/api/health"}:
        return _json_response(
            start_response,
            HTTPStatus.OK,
            {"ok": True, "service": "stylewarehouse-robot-navigation", "algorithm": ALGORITHM},
        )

    if path in {"/api", "/api/catalogue"} and method == "GET":
        catalogue = _build_catalogue()
        search = query.get("search", [""])[0].strip()
        raw_limit = query.get("limit", ["20"])[0]
        limit = int(raw_limit) if raw_limit.isdigit() else 20
        items = catalogue.search_by_name(search) if search else catalogue.all_items()
        serialised = [_item_to_dict(item) for item in items[: max(limit, 1)]]
        return _json_response(
            start_response,
            HTTPStatus.OK,
            {
                "ok": True,
                "count": len(serialised),
                "total_catalogue_items": len(catalogue),
                "items": serialised,
            },
        )

    if path.startswith("/api/catalogue/") and method == "GET":
        sku = path.rsplit("/", 1)[-1].upper()
        catalogue = _build_catalogue()
        item = catalogue.find(sku)
        if item is None:
            return _json_response(
                start_response,
                HTTPStatus.NOT_FOUND,
                {"ok": False, "error": f"SKU {sku} was not found."},
            )
        return _json_response(start_response, HTTPStatus.OK, {"ok": True, "item": _item_to_dict(item)})

    if path == "/api/demo-order" and method == "GET":
        return _json_response(start_response, HTTPStatus.OK, _simulate_order("DEMO-API", DEMO_ORDER))

    if path == "/api/simulate-order" and method == "POST":
        try:
            payload = _read_json_body(environ)
        except json.JSONDecodeError:
            return _json_response(
                start_response,
                HTTPStatus.BAD_REQUEST,
                {"ok": False, "error": "Request body must be valid JSON."},
            )

        lines = _normalise_lines(payload)
        if not lines:
            return _json_response(
                start_response,
                HTTPStatus.BAD_REQUEST,
                {
                    "ok": False,
                    "error": "Provide either an 'items' list or a 'skus' list in the JSON body.",
                },
            )

        order_id = str(payload.get("order_id", "API-ORDER"))
        return _json_response(start_response, HTTPStatus.OK, _simulate_order(order_id, lines))

    return _json_response(
        start_response,
        HTTPStatus.NOT_FOUND,
        {"ok": False, "error": f"No route matches {method} {path}."},
    )
