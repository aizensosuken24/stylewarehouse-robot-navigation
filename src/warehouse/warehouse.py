"""
Warehouse module: Loads and manages warehouse layout, shelves, and inventory.
"""
import csv
import json
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


class Shelf:
    def __init__(self, shelf_id: str, zone: str, x: int, y: int, capacity: int = 200):
        self.id = shelf_id
        self.zone = zone
        self.x = x
        self.y = y
        self.capacity = capacity
        self.items: Dict[str, int] = {}  # item_id -> quantity

    @property
    def position(self) -> Tuple[int, int]:
        return (self.x, self.y)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "zone": self.zone,
            "x": self.x,
            "y": self.y,
            "capacity": self.capacity,
            "item_count": len(self.items)
        }


class WarehouseLayout:
    """
    Loads warehouse layout from JSON and provides spatial queries.
    """

    def __init__(self, layout_path: str):
        self.layout_path = Path(layout_path)
        self.width: int = 20
        self.height: int = 20
        self.shelves: Dict[str, Shelf] = {}
        self.obstacles: Set[Tuple[int, int]] = set()
        self.zones: List[dict] = []
        self.robots_initial: List[dict] = []
        self.charging_stations: List[dict] = []
        self._load()

    def _load(self):
        """Parse warehouse_layout.json."""
        if not self.layout_path.exists():
            return

        with open(self.layout_path) as f:
            data = json.load(f)

        wh = data.get("warehouse", {})
        dims = wh.get("dimensions", {})
        self.width = dims.get("width", 20)
        self.height = dims.get("height", 20)

        self.zones = [self._normalise_zone(zone) for zone in data.get("zones", [])]
        self.charging_stations = data.get("charging_stations", [])
        self.robots_initial = data.get("robots", [])

        for s in data.get("shelves", []):
            shelf = Shelf(
                shelf_id=s["id"],
                zone=s["zone"],
                x=s["x"],
                y=s["y"],
                capacity=s.get("capacity", 200)
            )
            self.shelves[s["id"]] = shelf

        # Convert obstacle rectangles to individual cells
        for obs in data.get("obstacles", []):
            for dx in range(obs.get("width", 1)):
                for dy in range(obs.get("height", 1)):
                    self.obstacles.add((obs["x"] + dx, obs["y"] + dy))

    def _normalise_zone(self, zone: dict) -> dict:
        normalised = dict(zone)
        normalised["entry"] = tuple(zone.get("entry", (zone["x"], zone["y"])))
        normalised["exit"] = tuple(
            zone.get(
                "exit",
                (zone["x"] + zone["width"] - 1, zone["y"] + zone["height"] - 1),
            )
        )
        return normalised

    def get_zone_at(self, x: int, y: int) -> Optional[dict]:
        for zone in self.zones:
            if (
                zone["x"] <= x < zone["x"] + zone["width"]
                and zone["y"] <= y < zone["y"] + zone["height"]
            ):
                return zone
        return None

    def is_transition_allowed(
        self, current: Tuple[int, int], nxt: Tuple[int, int]
    ) -> bool:
        current_zone = self.get_zone_at(*current)
        next_zone = self.get_zone_at(*nxt)

        if current_zone == next_zone:
            return True

        if current_zone is None and next_zone is None:
            return True

        if current_zone is None and next_zone is not None:
            return nxt == next_zone["entry"]

        if current_zone is not None and next_zone is None:
            return current == current_zone["exit"]

        return False

    def get_shelf(self, shelf_id: str) -> Optional[Shelf]:
        return self.shelves.get(shelf_id)

    def get_shelf_position(self, shelf_id: str) -> Optional[Tuple[int, int]]:
        shelf = self.shelves.get(shelf_id)
        return shelf.position if shelf else None

    def get_all_shelf_positions(self) -> List[Tuple[int, int]]:
        return [s.position for s in self.shelves.values()]

    def to_dict(self) -> dict:
        return {
            "width": self.width,
            "height": self.height,
            "zones": [
                {
                    **zone,
                    "entry": list(zone["entry"]),
                    "exit": list(zone["exit"]),
                }
                for zone in self.zones
            ],
            "shelves": [s.to_dict() for s in self.shelves.values()],
            "obstacles": [{"x": x, "y": y} for x, y in self.obstacles],
            "charging_stations": self.charging_stations,
            "robots": self.robots_initial
        }


class InventoryManager:
    """Manages item inventory loaded from item_catalogue.csv."""

    def __init__(self, catalogue_path: str):
        self.catalogue_path = Path(catalogue_path)
        self.items: Dict[str, dict] = {}
        self._load()

    def _load(self):
        if not self.catalogue_path.exists():
            return
        with open(self.catalogue_path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.items[row["item_id"]] = {
                    "id": row["item_id"],
                    "name": row["name"],
                    "category": row["category"],
                    "weight_kg": float(row["weight_kg"]),
                    "location_id": row["location_id"],
                    "quantity": int(row["quantity"]),
                    "reorder_point": int(row["reorder_point"]),
                    "supplier": row["supplier"]
                }

    def get_item(self, item_id: str) -> Optional[dict]:
        return self.items.get(item_id)

    def get_item_location(self, item_id: str) -> Optional[str]:
        item = self.items.get(item_id)
        return item["location_id"] if item else None

    def search_items(self, query: str) -> List[dict]:
        q = query.lower()
        return [
            item for item in self.items.values()
            if q in item["name"].lower() or q in item["category"].lower()
        ]

    def get_low_stock_items(self) -> List[dict]:
        return [
            item for item in self.items.values()
            if item["quantity"] <= item["reorder_point"]
        ]

    def all_items(self) -> List[dict]:
        return list(self.items.values())
