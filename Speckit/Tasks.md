# Tasks

## Backlog

### High Priority
- GitHub Actions CI: run pytest on every push to main
- Add POST /api/robots endpoint to register new robots dynamically
- Persist robot state to a lightweight database (SQLite or Render's free Postgres)

### Medium Priority
- WebSocket support for real-time robot position streaming
- Multi-robot collision detection in fleet manager
- Batch pick order endpoint (multiple orders at once)
- Add zone capacity limits and overflow handling

### Low Priority
- Heat map visualisation of most-visited cells
- Robot task history log endpoint
- Export pick orders as PDF report
- Mobile-responsive improvements to dashboard

## Completed
- A* pathfinder
- TSP solver (NN + 2-opt)
- Robot + Fleet classes
- Warehouse layout loader
- Inventory manager (CSV)
- Flask REST API (10 endpoints)
- CORS setup for Render to Vercel
- Frontend dashboard (4 panels)
- Canvas map renderer
- render.yaml deployment config
- vercel.json deployment config
- 38 unit tests (100% passing)
