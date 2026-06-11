# Spec — StyleWarehouse Robot Navigation

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Order Manager                    │
│  receive_order() → sequence_stops() → dispatch()   │
└────────────────────┬────────────────────────────────┘
                     │
          ┌──────────▼──────────┐
          │   Navigation Engine  │
          │  A* pathfinder       │
          │  TSP sequencer       │
          └──────────┬──────────┘
                     │
     ┌───────────────▼───────────────┐
     │         Warehouse Map          │
     │  Grid: rows × cols             │
     │  Cell types: OPEN/SHELF/DEPOT  │
     └───────────────┬───────────────┘
                     │
          ┌──────────▼──────────┐
          │       Robot          │
          │  position, battery   │
          │  move(), pick()      │
          └──────────┬──────────┘
                     │
          ┌──────────▼──────────┐
          │    Visualiser        │
          │  Terminal / pygame   │
          └─────────────────────┘
```

## Module Specifications

### `warehouse/map.py`
- Class `WarehouseMap(rows, cols)`
- Methods: `load_from_json()`, `get_cell()`, `set_cell()`, `neighbours()`
- Cell values: `0=OPEN`, `1=SHELF`, `2=DEPOT`, `3=OBSTACLE`, `4=AISLE`

### `warehouse/catalogue.py`
- Class `ItemCatalogue`
- Methods: `add_item(sku, name, aisle, shelf, bin)`, `find_item(sku)`, `load_from_csv()`

### `navigation/pathfinder.py`
- Function `astar(grid, start, goal) → List[Tuple]`
- Function `dijkstra(grid, start, goal) → List[Tuple]`
- Heuristic: Manhattan distance

### `navigation/tsp.py`
- Function `nearest_neighbour(stops, dist_fn) → List`
- Function `total_distance(path, dist_fn) → float`

### `robot/robot.py`
- Class `Robot(name, start_pos, map)`
- Methods: `navigate_to(pos)`, `pick_item(sku)`, `return_to_depot()`
- Attributes: `position`, `battery`, `carrying`

### `robot/order.py`
- Class `Order(order_id, items)`
- Methods: `add_item()`, `is_complete()`, `summary()`

### `ui/visualiser.py`
- Function `print_map(warehouse_map, robot, path)`  — terminal ASCII
- Function `animate(warehouse_map, robot, path_steps)` — pygame (optional)

## Data Files
- `data/warehouse_layout.json` — grid definition
- `data/item_catalogue.csv` — SKU, name, aisle, shelf, bin

## Configuration
- `config.py` — grid size, depot position, robot speed, battery capacity
