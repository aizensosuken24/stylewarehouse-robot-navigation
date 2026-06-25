"""
Speckit Warehouse Robot API Server
Deployed on Render (backend).
"""
import os
import sys
from pathlib import Path

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
layout    = WarehouseLayout(config.WAREHOUSE_LAYOUT_PATH)
inventory = InventoryManager(config.ITEM_CATALOGUE_PATH)

# Pathfinder
pathfinder = AStarPathfinder(
    grid_width=layout.width,
    grid_height=layout.height,
    obstacles=layout.obstacles
)

# Fleet
fleet = FleetManager()
for rb in layout.robots_initial:
    fleet.add_robot(Robot(
        robot_id=rb["id"],
        name=rb["name"],
        x=rb["x"],
        y=rb["y"],
        battery=rb.get("battery", 100.0)
    ))


# ── Health ─────────────────────────────────────────────────────────────────────
@app.route("/", methods=["GET"])
@app.route("/health", methods=["GET"])
def health():
    return success_response({"status": "ok", "version": "1.0.0"}, "Speckit API running")


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
    query   = request.args.get("q", "")
    page    = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 20))

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
    return success_response({
        "robots": fleet.all_robots_status(),
        "summary": fleet.fleet_summary()
    })


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
    start = body.get("start")
    goal  = body.get("goal")

    if not start or not goal or len(start) != 2 or len(goal) != 2:
        return error_response("Provide 'start' and 'goal' as [x, y] arrays")

    sx, sy = int(start[0]), int(start[1])
    gx, gy = int(goal[0]),  int(goal[1])

    path = pathfinder.find_path((sx, sy), (gx, gy))
    if path is None:
        return error_response("No path found between the given positions", 404)

    return success_response({
        "path": path,
        "length": pathfinder.path_length(path),
        "steps": len(path)
    })


# ── Route optimisation (TSP) ───────────────────────────────────────────────────
@app.route("/api/route", methods=["POST"])
def optimise_route():
    """
    POST /api/route
    Body: { "start": [x, y], "stops": [[x1,y1], [x2,y2], ...] }
    """
    body  = request.get_json(silent=True) or {}
    start = body.get("start")
    stops = body.get("stops", [])

    if not start or len(start) != 2:
        return error_response("Provide 'start' as [x, y]")

    start_t = (int(start[0]), int(start[1]))
    stops_t = [(int(s[0]), int(s[1])) for s in stops]

    result = solve_tsp(start_t, stops_t, improve=True)
    return success_response(result)


# ── Pick order ─────────────────────────────────────────────────────────────────
@app.route("/api/pick", methods=["POST"])
def create_pick_order():
    """
    POST /api/pick
    Body: { "item_ids": ["ITM001", "ITM002"], "robot_id": "R1" (optional) }
    Resolves item locations, optimises route, assigns nearest robot.
    """
    body     = request.get_json(silent=True) or {}
    item_ids = body.get("item_ids", [])

    if not item_ids:
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

    if missing:
        return error_response(f"Items not found: {missing}", 404)

    # Choose robot
    robot_id = body.get("robot_id")
    if robot_id:
        robot = fleet.get_robot(robot_id)
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
    tsp     = solve_tsp(start_t, stops_t, improve=True)

    return success_response({
        "robot": robot.to_dict(),
        "stops": stops,
        "optimised_route": tsp,
        "total_distance": tsp["total_distance"]
    })


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
