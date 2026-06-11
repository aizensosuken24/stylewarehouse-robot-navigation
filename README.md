# StyleWarehouse Robot Navigation

An autonomous robot navigation simulation for a fashion/clothing warehouse.
The robot receives pick orders, plans the shortest route across shelves using
**A\*** pathfinding and a **Nearest-Neighbour TSP** sequencer, then executes
(or animates) the route.

---

## Project Structure

```
stylewarehouse-robot-navigation/
├── Speckit/
│   ├── Clarify.md       ← Problem definition & scope
│   ├── Research.md      ← Algorithm research & decisions
│   ├── Spec.md          ← Module specifications & architecture
│   ├── Plan.md          ← Sprint plan & milestones
│   └── Tasks.md         ← Task tracker
│
├── src/
│   ├── warehouse/
│   │   ├── map.py       ← WarehouseMap (grid representation)
│   │   └── catalogue.py ← ItemCatalogue (SKU → grid location)
│   ├── navigation/
│   │   ├── pathfinder.py ← A* and Dijkstra algorithms
│   │   └── tsp.py        ← Multi-stop TSP sequencer
│   ├── robot/
│   │   ├── robot.py     ← Robot class (navigate + pick)
│   │   └── order.py     ← Order class
│   └── ui/
│       └── visualiser.py ← Terminal ASCII + optional pygame
│
├── tests/
│   ├── test_pathfinder.py
│   ├── test_robot.py
│   └── test_tsp.py
│
├── data/
│   ├── warehouse_layout.json  ← 15 × 25 grid definition
│   └── item_catalogue.csv     ← 50 sample fashion SKUs
│
├── config.py            ← Global settings
├── main.py              ← Entry point (interactive + auto demo)
├── requirements.txt
└── run_tests.sh
```

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://code.swecha.org/Anirudh24/stylewarehouse-robot-navigation.git
cd stylewarehouse-robot-navigation

# 2. (Optional) Install pygame for animated GUI
pip install pygame

# 3. Run the interactive simulation
python main.py

# 4. Or run the auto demo (no interaction needed)
python main.py --auto

# 5. Animated pygame version
python main.py --auto --pygame
```

---

## Running Tests

```bash
bash run_tests.sh
# or
python -m pytest tests/ -v
```

---

## How It Works

### Warehouse Map
A 15 × 25 grid where each cell is one of:

| Symbol | Type | Meaning |
|--------|------|---------|
| `D` | Depot | Robot start/end |
| `S` | Shelf | Item storage |
| ` ` | Aisle | Walkable corridor |
| `.` | Open | Walkable floor |
| `#` | Obstacle | Blocked |

### Order Execution Flow

```
Order received
    ↓
Resolve SKU → grid positions (ItemCatalogue)
    ↓
Sequence stops (TSP Nearest-Neighbour + 2-opt)
    ↓
For each stop: A* pathfind → navigate → pick item
    ↓
Return to Depot
    ↓
Order complete ✓
```

### Algorithms

| Problem | Algorithm | Complexity |
|---------|-----------|------------|
| Single-pair shortest path | A\* (Manhattan heuristic) | O((V+E) log V) |
| Multi-stop ordering | Nearest-Neighbour + 2-opt | O(n²) |
| Fallback pathfinding | Dijkstra | O((V+E) log V) |

---

## Configuration (`config.py`)

| Setting | Default | Description |
|---------|---------|-------------|
| `WAREHOUSE_ROWS` | 15 | Grid rows |
| `WAREHOUSE_COLS` | 25 | Grid columns |
| `DEPOT_POSITION` | (0, 0) | Robot home |
| `ROBOT_BATTERY_CAPACITY` | 500 | Steps before recharge |
| `ALGORITHM` | `"astar"` | `"astar"` or `"dijkstra"` |

---

## Extending

- **Add items**: edit `data/item_catalogue.csv`
- **Change layout**: edit `data/warehouse_layout.json`
- **Swap pathfinder**: set `ALGORITHM = "dijkstra"` in `config.py`
- **Multi-robot**: subclass `Robot` and add reservation logic in `tsp.py`
- **REST API**: add FastAPI routes that call `robot.execute_order()`

---

## Author
Anirudh R Rao — Swecha GitLab

---

## AI Features & i18n

This project includes optional AI-powered helpers and basic internationalisation (i18n) support.

- Local inference: the project can call a local Ollama-like HTTP API running on `http://localhost:11434`.
- Remote (BYOK): set `REMOTE_AI_URL` and provide a bearer token via the env var `AI_BEARER_TOKEN` (or `BYOK_TOKEN`) to use a remote service.
- Language support: UI strings are available in English (default), Hindi (`hi`) and Telugu (`te`).

Quick examples:

1. Local inference (Ollama):

```bash
# run a local Ollama server, then in Python:
python -c "from src.ai.inference import generate_text; print(generate_text('Hello from the warehouse', backend='local'))"
```

2. Remote BYOK (example):

```bash
export REMOTE_AI_URL=https://api.example.com/generate
export AI_BEARER_TOKEN="<your-token>"
python -c "from src.ai.inference import generate_text; print(generate_text('Summarise the order flow', backend='remote'))"
```

3. Use Hindi/Telugu UI strings in code:

```python
from src.ui.visualiser import print_map
print_map(warehouse_map, title='', lang='hi')  # Hindi
print_map(warehouse_map, title='', lang='te')  # Telugu
```

Notes:
- The `requests` package is required for remote/local HTTP calls. Install via `pip install -r requirements.txt`.
- The AI helpers are optional and designed to be non-invasive — existing functionality remains unchanged unless you explicitly call the new helpers.
