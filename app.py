"""Deployment-friendly WSGI app for local, Vercel, and Render use."""
from __future__ import annotations

import json
from http import HTTPStatus
from io import BytesIO
from typing import Dict, Iterable, List, Tuple
from urllib.parse import parse_qs

from config import ALGORITHM, CATALOGUE_FILE
from main import DEMO_ORDER
from src.robot.order import Order
from src.robot.robot import Robot
from src.warehouse.catalogue import Item, ItemCatalogue
from src.warehouse.map import build_default_map

Headers = List[Tuple[str, str]]


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
    return {
        "sku": item.sku,
        "name": item.name,
        "category": item.category,
        "brand": item.brand,
        "size": item.size,
        "colour": item.colour,
        "location": [item.grid_row, item.grid_col],
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
    return {
        "ok": success,
        "order_id": order.order_id,
        "requested_lines": [{"sku": sku, "quantity": quantity} for sku, quantity in lines],
        "picked_skus": order.picked_skus(),
        "remaining_skus": order.pending_skus(),
        "robot": {
            "name": robot.name,
            "position": list(robot.position),
            "battery": robot.battery,
            "total_steps": robot.total_steps,
            "carrying": robot.carrying,
        },
        "catalogue_size": len(catalogue),
        "log": robot.log,
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

    if path == "/":
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
