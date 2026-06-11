# Tasks — StyleWarehouse Robot Navigation

## Backlog

### 🔴 High Priority
- [x] Define warehouse grid schema (JSON)
- [x] Define item catalogue schema (CSV)
- [x] Implement `WarehouseMap` class
- [x] Implement `ItemCatalogue` class
- [x] Implement A* pathfinder
- [x] Implement TSP nearest-neighbour sequencer
- [x] Implement `Robot` class
- [x] Implement `Order` class
- [x] Write ASCII visualiser
- [x] Write `main.py` demo

### 🟡 Medium Priority
- [x] Unit tests for pathfinder (edge cases: no path, same start/end)
- [x] Unit tests for robot (pick, move, battery)
- [ ] pygame animated visualiser
- [ ] Multi-order queue support

### 🟢 Low Priority / Stretch
- [ ] D* Lite for dynamic obstacle avoidance
- [ ] REST API for order submission (`FastAPI`)
- [ ] Web dashboard (React)
- [ ] Multi-robot support with collision reservation

## Assigned
| Task | Owner | Status |
|------|-------|--------|
| A* algorithm | Anirudh | ✅ Done |
| TSP sequencer | Anirudh | ✅ Done |
| Warehouse map | Anirudh | ✅ Done |
| Catalogue CSV loader | Anirudh | ✅ Done |
| Robot class | Anirudh | ✅ Done |
| main.py integration | Anirudh | ✅ Done |
| Tests | Anirudh | ✅ Done |
| README | Anirudh | ✅ Done |
