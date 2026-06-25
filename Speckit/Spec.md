# Spec

## API Specification

### Base URL
- Local: http://localhost:5000
- Production: https://speckit-api.onrender.com

### Response Format
All endpoints return:
  success: true or false
  message: string
  data: object

### Endpoints

GET  /health                 — API health check
GET  /api/warehouse          — Full warehouse layout
GET  /api/items              — List items (q, page, per_page params)
GET  /api/items/:id          — Single item
GET  /api/items/low-stock    — Items below reorder point
GET  /api/robots             — All robots + fleet summary
GET  /api/robots/:id         — Single robot state
POST /api/robots/:id/charge  — Charge robot to 100%
POST /api/path               — A* path: {start:[x,y], goal:[x,y]}
POST /api/route              — TSP route: {start:[x,y], stops:[[x,y]...]}
POST /api/pick               — Pick order: {item_ids:["ITM001"...]}

## Data Models

### Robot fields
  id, name, x, y, battery, status, is_low_battery,
  is_available, total_distance, total_picks,
  error_message, current_task

### Status values
  idle, moving, picking, charging, error, returning

### Item fields
  id, name, category, weight_kg, location_id,
  quantity, reorder_point, supplier
