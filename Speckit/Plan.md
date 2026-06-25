# Plan

## Milestones

### M1 — Core Algorithms (done)
- A* pathfinder with obstacle support
- TSP nearest-neighbour + 2-opt solver
- Unit tests for both (38 tests passing)

### M2 — Data Layer (done)
- warehouse_layout.json — zones, shelves, obstacles, robots, charging stations
- item_catalogue.csv — 10 SKUs with location, quantity, reorder point
- WarehouseLayout loader
- InventoryManager CSV reader

### M3 — Robot Layer (done)
- Robot class — state, battery, movement, pick, charge
- FleetManager — assignment, nearest-available, fleet summary

### M4 — API (done)
- Flask server with 10 REST endpoints
- Standardised JSON responses
- CORS configured for Vercel frontend
- render.yaml deployment blueprint

### M5 — Frontend (done)
- 4-panel dashboard (Overview, Pathfinder, Inventory, Robots)
- Canvas warehouse map renderer
- Path visualisation
- Pick route optimiser UI
- vercel.json deployment config

### M6 — CI/CD (next)
- GitHub Actions pipeline for test + lint on push
- Auto-deploy to Render on main branch merge
- Auto-deploy to Vercel on main branch merge
