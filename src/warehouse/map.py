"""Warehouse map primitives."""
from __future__ import annotations

import json
import os
import sys
from typing import List, Optional, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from config import (
    CELL_AISLE,
    CELL_DEPOT,
    CELL_OBSTACLE,
    CELL_OPEN,
    CELL_SHELF,
    CELL_SYMBOLS,
    DEPOT_POSITION,
    WAREHOUSE_COLS,
    WAREHOUSE_ROWS,
)


class WarehouseMap:
    """A rectangular warehouse grid."""

    def __init__(self, rows: int = WAREHOUSE_ROWS, cols: int = WAREHOUSE_COLS):
        self.rows = rows
        self.cols = cols
        self.grid: List[List[int]] = [[CELL_OPEN] * cols for _ in range(rows)]
        depot_row, depot_col = DEPOT_POSITION
        self.grid[depot_row][depot_col] = CELL_DEPOT

    def set_cell(self, row: int, col: int, cell_type: int) -> None:
        self._check_bounds(row, col)
        self.grid[row][col] = cell_type

    def get_cell(self, row: int, col: int) -> int:
        self._check_bounds(row, col)
        return self.grid[row][col]

    def is_walkable(self, row: int, col: int) -> bool:
        if not self._in_bounds(row, col):
            return False
        return self.grid[row][col] != CELL_OBSTACLE

    def neighbours(self, row: int, col: int) -> List[Tuple[int, int]]:
        candidates = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
        ]
        return [(next_row, next_col) for next_row, next_col in candidates if self.is_walkable(next_row, next_col)]

    def load_from_json(self, filepath: str) -> "WarehouseMap":
        with open(filepath, encoding="utf-8") as handle:
            data = json.load(handle)
        self.rows = data["rows"]
        self.cols = data["cols"]
        self.grid = data["grid"]
        return self

    def save_to_json(self, filepath: str) -> None:
        with open(filepath, "w", encoding="utf-8") as handle:
            json.dump({"rows": self.rows, "cols": self.cols, "grid": self.grid}, handle, indent=2)

    def to_ascii(
        self,
        robot_pos: Optional[Tuple[int, int]] = None,
        path: Optional[List[Tuple[int, int]]] = None,
    ) -> str:
        path_set = set(path) if path else set()
        lines = ["   " + "".join(str(col % 10) for col in range(self.cols))]
        for row in range(self.rows):
            row_str = f"{row:2} "
            for col in range(self.cols):
                if robot_pos and (row, col) == robot_pos:
                    row_str += "R"
                elif (row, col) in path_set:
                    row_str += "*"
                else:
                    row_str += CELL_SYMBOLS.get(self.grid[row][col], "?")
            lines.append(row_str)
        return "\n".join(lines)

    def _in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.cols

    def _check_bounds(self, row: int, col: int) -> None:
        if not self._in_bounds(row, col):
            raise IndexError(f"Cell ({row},{col}) is out of bounds ({self.rows}x{self.cols})")

    def __repr__(self) -> str:
        return f"WarehouseMap({self.rows}x{self.cols})"


def build_default_map() -> WarehouseMap:
    """Build the default 15x25 warehouse layout."""
    warehouse_map = WarehouseMap()
    for row in range(2, warehouse_map.rows):
        for col in range(warehouse_map.cols):
            if col % 3 == 0:
                warehouse_map.grid[row][col] = CELL_AISLE
            else:
                warehouse_map.grid[row][col] = CELL_SHELF

    depot_row, depot_col = DEPOT_POSITION
    warehouse_map.grid[depot_row][depot_col] = CELL_DEPOT
    return warehouse_map
