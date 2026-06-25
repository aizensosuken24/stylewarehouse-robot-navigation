"""
Smart-Robo Nav API Server
Deployed on Render (backend).
"""

import math
import sys
from pathlib import Path
from typing import Optional

# Ensure project root is on path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from flask import Flask, request
from flask_cors import CORS

import config
from src.navigation.pathfinder import AStarPathfinder
from src.navigation.tsp_solver import solve_tsp
from src.robot.robot import Robot
from src.robot.fleet import FleetManager
from src.warehouse.warehouse import WarehouseLayout, InventoryManager
from src.ui.responses import success_response, error_response, paginate

# ── App setup ──────────────────────────────────────────────────────────────────
app = Flask(__name__)
CORS(app, origins=config.ALLOWED_ORIGINS, supports_credentials=True)

# ── Initialise warehouse ───────────────────────────────────────────────────────
layout = WarehouseLayout(config.WAREHOUSE_LAYOUT_PATH)
inventory = InventoryManager(config.ITEM_CATALOGUE_PATH)

# Pathfinder
pathfinder = AStarPathfinder(
    grid_width=layout.width,
    grid_height=layout.height,
    obstacles=layout.obstacles,
    can_move=layout.is_transition_allowed,
)

# Fleet
fleet = FleetManager()
for rb in layout.robots_initial:
    fleet.add_robot(
        Robot(
            robot_id=rb["id"],
            name=rb["name"],
            x=rb["x"],
            y=rb["y"],
            battery=rb.get("battery", 100.0),
        )
    )


def _parse_int_arg(name: str, default: int, minimum: Optional[int] = None):
    raw_value = request.args.get(name, default)
    try:
        value = int(raw_value)
    except (TypeError, ValueError):
        return None, error_response(f"Query parameter '{name}' must be an integer")

    if minimum is not None and value < minimum:
        return None, error_response(
            f"Query parameter '{name}' must be greater than or equal to {minimum}"
        )

    return value, None


def _parse_point(value, field_name: str):
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        return None, error_response(f"Provide '{field_name}' as a [x, y] array")

    try:
        x = int(value[0])
        y = int(value[1])
    except (TypeError, ValueError):
        return None, error_response(f"Coordinates in '{field_name}' must be integers")

    return (x, y), None


def _build_path_distance_fn():
    cache = {}

    def distance(a, b):
        key = (a, b)
        if key in cache:
            return cache[key]

        path = pathfinder.find_path(a, b)
        value = float("inf") if path is None else pathfinder.path_length(path)
        cache[key] = value
        return value

    return distance


def _solve_route(start, stops):
    distance_fn = _build_path_distance_fn()
    result = solve_tsp(start, stops, improve=True, distance_fn=distance_fn)
    if not math.isfinite(result["total_distance"]):
        return None, error_response(
            (
                "At least one stop is unreachable with the current "
                "zone gates and obstacles"
            ),
            409,
        )
    return result, None


# ── Health ─────────────────────────────────────────────────────────────────────
@app.route("/", methods=["GET"])
@app.route("/health", methods=["GET"])
def health():
    return success_response(
        {"status": "ok", "version": "1.1.0"},
        "Smart-Robo Nav API running",
    )


# ── Warehouse ──────────────────────────────────────────────────────────────────
@app.route("/api/warehouse", methods=["GET"])
def get_warehouse():
    """Return full warehouse layout with live robot status."""
    data = layout.to_dict()
    data["robots"] = fleet.all_robots_status()
    return success_response(data)


# ── Inventory ──────────────────────────────────────────────────────────────────
@app.route("/api/items", methods=["GET"])
def get_items():
    query = request.args.get("q", "")
    page, error = _parse_int_arg("page", 1, minimum=1)
    if error:
        return error

    per_page, error = _parse_int_arg("per_page", 20, minimum=1)
    if error:
        return error

    items = inventory.search_items(query) if query else inventory.all_items()
    return success_response(paginate(items, page, per_page))


@app.route("/api/items/<item_id>", methods=["GET"])
def get_item(item_id: str):
    item = inventory.get_item(item_id)
    if not item:
        return error_response(f"Item '{item_id}' not found", 404)
    return success_response(item)


@app.route("/api/items/low-stock", methods=["GET"])
def get_low_stock():
    return success_response(inventory.get_low_stock_items())


# ── Robots ─────────────────────────────────────────────────────────────────────
@app.route("/api/robots", methods=["GET"])
def get_robots():
    return success_response(
        {"robots": fleet.all_robots_status(), "summary": fleet.fleet_summary()}
    )


@app.route("/api/robots/<robot_id>", methods=["GET"])
def get_robot(robot_id: str):
    robot = fleet.get_robot(robot_id)
    if not robot:
        return error_response(f"Robot '{robot_id}' not found", 404)
    return success_response(robot.to_dict())


@app.route("/api/robots/<robot_id>/charge", methods=["POST"])
def charge_robot(robot_id: str):
    robot = fleet.get_robot(robot_id)
    if not robot:
        return error_response(f"Robot '{robot_id}' not found", 404)
    robot.charge(100.0)
    return success_response(robot.to_dict(), "Robot charged to 100%")


# ── Pathfinding ────────────────────────────────────────────────────────────────
@app.route("/api/path", methods=["POST"])
def find_path():
    """
    POST /api/path
    Body: { "start": [x, y], "goal": [x, y] }
    """
    body = request.get_json(silent=True) or {}
    start, error = _parse_point(body.get("start"), "start")
    if error:
        return error

    goal, error = _parse_point(body.get("goal"), "goal")
    if error:
        return error

    path = pathfinder.find_path(start, goal)
    if path is None:
        return error_response("No path found between the given positions", 404)

    return success_response(
        {
            "path": path,
            "length": pathfinder.path_length(path),
            "steps": max(0, len(path) - 1),
        }
    )


# ── Route optimisation (TSP) ───────────────────────────────────────────────────
@app.route("/api/route", methods=["POST"])
def optimise_route():
    """
    POST /api/route
    Body: { "start": [x, y], "stops": [[x1,y1], [x2,y2], ...] }
    """
    body = request.get_json(silent=True) or {}
    start_t, error = _parse_point(body.get("start"), "start")
    if error:
        return error

    stops = body.get("stops", [])
    if not isinstance(stops, list):
        return error_response("Provide 'stops' as a list of [x, y] arrays")

    stops_t = []
    for index, stop in enumerate(stops):
        parsed_stop, error = _parse_point(stop, f"stops[{index}]")
        if error:
            return error
        stops_t.append(parsed_stop)

    result, error = _solve_route(start_t, stops_t)
    if error:
        return error

    return success_response(result)


# ── Pick order ─────────────────────────────────────────────────────────────────
@app.route("/api/pick", methods=["POST"])
def create_pick_order():
    """
    POST /api/pick
    Body: { "item_ids": ["ITM001", "ITM002"], "robot_id": "R1" (optional) }
    Resolves item locations, optimises route, assigns nearest robot.
    """
    body = request.get_json(silent=True) or {}
    item_ids = body.get("item_ids", [])

    if not isinstance(item_ids, list) or not item_ids:
        return error_response("Provide at least one item_id in 'item_ids'")

    # Resolve locations
    stops = []
    missing = []
    for iid in item_ids:
        shelf_id = inventory.get_item_location(iid)
        if not shelf_id:
            missing.append(iid)
            continue
        pos = layout.get_shelf_position(shelf_id)
        if pos:
            stops.append({"item_id": iid, "shelf_id": shelf_id, "position": list(pos)})
        else:
            missing.append(iid)

    if missing:
        return error_response(f"Items not found: {missing}", 404)

    # Choose robot
    robot_id = body.get("robot_id")
    if robot_id:
        robot = fleet.get_robot(robot_id)
        if not robot:
            return error_response(f"Robot '{robot_id}' not found", 404)
        if not robot.is_available:
            return error_response(f"Robot '{robot_id}' is not available", 409)
    else:
        stop_positions = [s["position"] for s in stops]
        cx = int(sum(p[0] for p in stop_positions) / len(stop_positions))
        cy = int(sum(p[1] for p in stop_positions) / len(stop_positions))
        robot = fleet.get_nearest_available_robot(cx, cy)

    if not robot:
        return error_response("No available robot", 503)

    # Optimise route
    start_t = robot.position
    stops_t = [tuple(s["position"]) for s in stops]
    tsp, error = _solve_route(start_t, stops_t)
    if error:
        return error

    return success_response(
        {
            "robot": robot.to_dict(),
            "stops": stops,
            "optimised_route": tsp,
            "total_distance": tsp["total_distance"],
        }
    )


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
