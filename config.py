# config.py — StyleWarehouse Robot Navigation
# Central configuration for the simulation.

# ── Warehouse Layout ──────────────────────────────────────────────────────────
WAREHOUSE_ROWS = 15          # number of rows in the grid
WAREHOUSE_COLS = 25          # number of columns in the grid
DEPOT_POSITION = (0, 0)      # (row, col) — robot starts and ends here

# ── Cell Type Constants ───────────────────────────────────────────────────────
CELL_OPEN     = 0
CELL_SHELF    = 1
CELL_DEPOT    = 2
CELL_OBSTACLE = 3
CELL_AISLE    = 4

CELL_SYMBOLS = {
    CELL_OPEN:     ".",
    CELL_SHELF:    "S",
    CELL_DEPOT:    "D",
    CELL_OBSTACLE: "#",
    CELL_AISLE:    " ",
}

# ── Robot ─────────────────────────────────────────────────────────────────────
ROBOT_BATTERY_CAPACITY = 500   # steps before recharge needed
ROBOT_SPEED = 1                # cells per tick (for animation)

# ── Pathfinding ───────────────────────────────────────────────────────────────
ALGORITHM = "astar"            # "astar" | "dijkstra"

# ── Files ─────────────────────────────────────────────────────────────────────
LAYOUT_FILE    = "data/warehouse_layout.json"
CATALOGUE_FILE = "data/item_catalogue.csv"
