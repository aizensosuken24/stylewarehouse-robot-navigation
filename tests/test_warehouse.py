"""Tests for warehouse zone gate rules."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.navigation.pathfinder import AStarPathfinder
from src.warehouse.warehouse import WarehouseLayout


def build_layout(tmp_path):
    layout_data = {
        "warehouse": {"dimensions": {"width": 6, "height": 6}},
        "zones": [
            {
                "id": "A",
                "name": "Assembly",
                "x": 1,
                "y": 1,
                "width": 3,
                "height": 3,
                "entry": [2, 1],
                "exit": [3, 3],
                "color": "#3B82F6",
            }
        ],
        "shelves": [],
        "obstacles": [{"x": 2, "y": 2, "width": 1, "height": 1}],
        "charging_stations": [],
        "robots": [],
    }
    path = tmp_path / "layout.json"
    path.write_text(json.dumps(layout_data), encoding="utf-8")
    return WarehouseLayout(str(path))


def build_pathfinder(layout):
    return AStarPathfinder(
        layout.width,
        layout.height,
        obstacles=layout.obstacles,
        can_move=layout.is_transition_allowed,
    )


def test_zone_entry_is_required(tmp_path):
    layout = build_layout(tmp_path)
    pf = build_pathfinder(layout)

    path = pf.find_path((2, 0), (1, 3))

    assert path is not None
    inside_steps = [step for step in path if layout.get_zone_at(*step) is not None]
    assert inside_steps[0] == (2, 1)


def test_zone_exit_is_required(tmp_path):
    layout = build_layout(tmp_path)
    pf = build_pathfinder(layout)

    path = pf.find_path((1, 3), (4, 3))

    assert path is not None
    inside_steps = [step for step in path if layout.get_zone_at(*step) is not None]
    assert inside_steps[-1] == (3, 3)


def test_internal_obstacle_is_respected(tmp_path):
    layout = build_layout(tmp_path)
    pf = build_pathfinder(layout)

    path = pf.find_path((2, 0), (3, 3))

    assert path is not None
    assert (2, 2) not in path
