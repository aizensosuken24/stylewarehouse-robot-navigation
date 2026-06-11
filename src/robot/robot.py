"""Warehouse navigation robot implementation."""
from __future__ import annotations

import os
import sys
from typing import List, Optional, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from config import ALGORITHM, DEPOT_POSITION, ROBOT_BATTERY_CAPACITY
from src.navigation.pathfinder import find_path
from src.navigation.tsp import sequence_order
from src.robot.order import Order
from src.utils.output import safe_print

Pos = Tuple[int, int]


class BatteryError(Exception):
    """Raised when the robot cannot complete a route with the current battery."""


class Robot:
    """Autonomous warehouse robot."""

    def __init__(self, name: str, warehouse_map, catalogue, depot: Pos = DEPOT_POSITION):
        self.name = name
        self.map = warehouse_map
        self.catalogue = catalogue
        self.depot: Pos = depot
        self.position: Pos = depot
        self.battery: int = ROBOT_BATTERY_CAPACITY
        self.carrying: List[str] = []
        self.total_steps: int = 0
        self.log: List[str] = []

    def execute_order(self, order: Order, verbose: bool = True) -> bool:
        """Execute a full order and return ``True`` if every line was picked."""
        self._log(f"> Starting order {order.order_id}", verbose)

        stops: List[Tuple[Pos, str]] = []
        for sku in order.pending_skus():
            item = self.catalogue.find(sku)
            if item is None:
                self._log(f"  [!] SKU {sku} not in catalogue - skipping", verbose)
                continue
            stops.append((item.location, sku))

        if not stops:
            self._log("  No valid stops found.", verbose)
            return False

        positions = [pos for pos, _ in stops]
        sku_map = {pos: sku for pos, sku in stops}
        sequenced = sequence_order(positions, self.position)

        for target in sequenced:
            sku = sku_map.get(target, "?")
            path = self._navigate_to(target, verbose)
            if path is None:
                self._log(f"  [X] No path to {target} for {sku}", verbose)
                continue
            self._pick(sku, order, verbose)

        self._navigate_to(self.depot, verbose)
        self._log(f"[OK] Order {order.order_id} complete. Steps: {self.total_steps}", verbose)
        self._log(order.summary(), verbose)
        return order.is_complete()

    def navigate_to(self, target: Pos, verbose: bool = True) -> Optional[List[Pos]]:
        """Navigate to a target position and return the path if one exists."""
        return self._navigate_to(target, verbose)

    def recharge(self) -> None:
        """Refill the battery to full capacity."""
        self.battery = ROBOT_BATTERY_CAPACITY
        self._log("[BAT] Battery recharged.")

    def _navigate_to(self, target: Pos, verbose: bool = True) -> Optional[List[Pos]]:
        if self.position == target:
            return [self.position]

        path = find_path(self.map, self.position, target, ALGORITHM)
        if path is None:
            self._log(f"  [X] No path from {self.position} -> {target}", verbose)
            return None

        steps = len(path) - 1
        if steps > self.battery:
            self._log(f"  [!] Low battery ({self.battery} steps left, need {steps})", verbose)
            self.recharge()

        self._log(f"  -> Moving {self.position} -> {target}  ({steps} steps)", verbose)
        self.position = target
        self.battery -= steps
        self.total_steps += steps
        return path

    def _pick(self, sku: str, order: Order, verbose: bool = True) -> bool:
        if order.mark_picked(sku):
            self.carrying.append(sku)
            self._log(f"  [OK] Picked {sku}", verbose)
            return True
        self._log(f"  [!] Could not pick {sku}", verbose)
        return False

    def _log(self, msg: str, verbose: bool = True) -> None:
        self.log.append(msg)
        if verbose:
            safe_print(msg)

    def status(self) -> str:
        return (
            f"Robot '{self.name}' | pos={self.position} | "
            f"battery={self.battery}/{ROBOT_BATTERY_CAPACITY} | "
            f"carrying={self.carrying}"
        )

    def __repr__(self) -> str:
        return f"Robot({self.name!r}, pos={self.position})"
