# Plan — StyleWarehouse Robot Navigation

## Milestones

| Sprint | Goal | Deliverables |
|--------|------|--------------|
| 1 | Core data structures | `WarehouseMap`, `ItemCatalogue`, JSON/CSV loaders |
| 2 | Pathfinding | A* algorithm, TSP sequencer, unit tests |
| 3 | Robot + Order | `Robot` class, `Order` class, order execution loop |
| 4 | Visualisation | ASCII terminal display, optional pygame renderer |
| 5 | Integration | `main.py` demo, README, full test suite |

## Sprint 1 — Core Data Structures
- [ ] `warehouse/map.py` — WarehouseMap class
- [ ] `warehouse/catalogue.py` — ItemCatalogue class
- [ ] `data/warehouse_layout.json` — sample 10×20 grid
- [ ] `data/item_catalogue.csv` — 50 sample SKUs
- [ ] `config.py` — global settings

## Sprint 2 — Pathfinding
- [ ] `navigation/pathfinder.py` — A* implementation
- [ ] `navigation/pathfinder.py` — Dijkstra fallback
- [ ] `navigation/tsp.py` — Nearest-neighbour TSP
- [ ] `tests/test_pathfinder.py` — unit tests

## Sprint 3 — Robot & Order Management
- [ ] `robot/robot.py` — Robot class
- [ ] `robot/order.py` — Order class
- [ ] `tests/test_robot.py` — unit tests

## Sprint 4 — Visualisation
- [ ] `ui/visualiser.py` — ASCII map renderer
- [ ] `ui/visualiser.py` — pygame renderer (optional)

## Sprint 5 — Integration & Polish
- [ ] `main.py` — interactive demo
- [ ] `README.md` — setup & usage guide
- [ ] CI: `requirements.txt`, `run_tests.sh`

## Risk Register

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| pygame not available | Medium | Graceful fallback to ASCII |
| Very large warehouse slows A* | Low | Add early-exit and grid chunking |
| TSP grows slow with many items | Low | Cap order size or use 2-opt |
