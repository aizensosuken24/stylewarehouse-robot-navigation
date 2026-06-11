"""
warehouse/map.py
Represents the warehouse as a 2-D grid of cells.
"""
from __future__ import annotations
import json
from typing import List, Tuple, Optional
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from config import (
    CELL_OPEN, CELL_SHELF, CELL_DEPOT, CELL_OBSTACLE, CELL_AISLE,
    CELL_SYMBOLS, WAREHOUSE_ROWS, WAREHOUSE_COLS, DEPOT_POSITION,
)


class WarehouseMap:
    """A rectangular grid warehouse map."""

    def __init__(self, rows: int = WAREHOUSE_ROWS, cols: int = WAREHOUSE_COLS):
        self.rows = rows
        self.cols = cols
        # Default: everything is OPEN
        self.grid: List[List[int]] = [
            [CELL_OPEN] * cols for _ in range(rows)
        ]
        # Mark depot
        dr, dc = DEPOT_POSITION
        self.grid[dr][dc] = CELL_DEPOT

    # ── Construction helpers ──────────────────────────────────────────────────

    def set_cell(self, row: int, col: int, cell_type: int) -> None:
        self._check_bounds(row, col)
        self.grid[row][col] = cell_type

    def get_cell(self, row: int, col: int) -> int:
        self._check_bounds(row, col)
        return self.grid[row][col]

    def is_walkable(self, row: int, col: int) -> bool:
        """A cell is walkable if it is not an obstacle or solid shelf."""
        if not self._in_bounds(row, col):
            return False
        return self.grid[row][col] != CELL_OBSTACLE

    def neighbours(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Return the 4-directional walkable neighbours of a cell."""
        candidates = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
        ]
        return [(r, c) for r, c in candidates if self.is_walkable(r, c)]

    # ── I/O ───────────────────────────────────────────────────────────────────

    def load_from_json(self, filepath: str) -> "WarehouseMap":
        """Load grid from a JSON file (see data/warehouse_layout.json)."""
        with open(filepath) as f:
            data = json.load(f)
        self.rows = data["rows"]
        self.cols = data["cols"]
        self.grid = data["grid"]
        return self

    def save_to_json(self, filepath: str) -> None:
        with open(filepath, "w") as f:
            json.dump({"rows": self.rows, "cols": self.cols, "grid": self.grid}, f, indent=2)

    # ── Display ───────────────────────────────────────────────────────────────

    def to_ascii(
        self,
        robot_pos: Optional[Tuple[int, int]] = None,
        path: Optional[List[Tuple[int, int]]] = None,
    ) -> str:
        path_set = set(path) if path else set()
        lines = []
        # Column header
        header = "   " + "".join(str(c % 10) for c in range(self.cols))
        lines.append(header)
        for r in range(self.rows):
            row_str = f"{r:2} "
            for c in range(self.cols):
                if robot_pos and (r, c) == robot_pos:
                    row_str += "R"
                elif (r, c) in path_set:
                    row_str += "·"
                else:
                    row_str += CELL_SYMBOLS.get(self.grid[r][c], "?")
            lines.append(row_str)
        return "\n".join(lines)

    # ── Internals ─────────────────────────────────────────────────────────────

    def _in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.cols

    def _check_bounds(self, row: int, col: int) -> None:
        if not self._in_bounds(row, col):
            raise IndexError(f"Cell ({row},{col}) is out of bounds ({self.rows}×{self.cols})")

    def __repr__(self) -> str:
        return f"WarehouseMap({self.rows}×{self.cols})"


# ── Factory: build the default 15×25 style warehouse ─────────────────────────

def build_default_map() -> WarehouseMap:
    """
    Creates a realistic clothing-warehouse layout:
      - Aisles every 3 columns
      - Shelf blocks between aisles
      - Depot at (0, 0)
    """
    wm = WarehouseMap()
    for r in range(2, wm.rows):          # leave row 0-1 as main aisle
        for c in range(wm.cols):
            col_in_block = c % 3
            if col_in_block == 0:         # aisle column
                wm.grid[r][c] = CELL_AISLE
            else:
                wm.grid[r][c] = CELL_SHELF
    # restore depot
    dr, dc = DEPOT_POSITION
    wm.grid[dr][dc] = CELL_DEPOT
    return wm
