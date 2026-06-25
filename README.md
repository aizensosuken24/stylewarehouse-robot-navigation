# Speckit — Warehouse Robot System

A warehouse robot navigation and management system with:
- **A\* pathfinding** for shortest-path routing
- **TSP route optimisation** for multi-stop pick orders
- **Fleet management** for multiple robots
- **REST API** (Flask / Render)
- **Dashboard frontend** (Vanilla JS / Vercel)

---

## Project Structure

```
Speckit/
├── data/
│   ├── item_catalogue.csv       # Product inventory
│   └── warehouse_layout.json   # Grid map, shelves, zones, robots
├── src/
│   ├── navigation/
│   │   ├── pathfinder.py        # A* algorithm
│   │   └── tsp_solver.py        # TSP nearest-neighbour + 2-opt
│   ├── robot/
│   │   ├── robot.py             # Robot state & movement
│   │   └── fleet.py             # Fleet manager
│   ├── warehouse/
│   │   └── warehouse.py         # Layout loader & inventory
│   └── ui/
│       └── responses.py         # Standardised JSON responses
├── tests/
│   ├── test_pathfinder.py
│   ├── test_robot.py
│   └── test_tsp.py
├── web/
│   ├── index.html               # Frontend SPA
│   ├── style.css
│   ├── app.js
│   └── netlify.toml             # Alternative: Netlify deploy
├── config.py                    # All configuration / env vars
├── server.py                    # Flask API (Render entry point)
├── main.py                      # Local dev entry point
├── render.yaml                  # Render deployment blueprint
├── vercel.json                  # Vercel deployment config
├── requirements.txt             # Backend deps (Flask, gunicorn)
├── requirements-web.txt         # Dev/test deps
└── run_tests.sh                 # Test runner
```

---

## Local Development

```bash
# 1. Install dependencies
pip install -r requirements.txt -r requirements-web.txt

# 2. Start API server
python main.py
# → http://localhost:5000

# 3. Open frontend
open web/index.html   # or serve via any static server
```

---

## Deployment

### Backend → Render

1. Push this repo to GitHub.
2. In [Render](https://render.com), create a **New Web Service** and connect the repo.
3. Render auto-detects `render.yaml` — no extra config needed.
4. After deploy, copy the Render service URL (e.g. `https://speckit-api.onrender.com`).
5. Set the `FRONTEND_URL` environment variable in Render to your Vercel URL.

### Frontend → Vercel

1. In [Vercel](https://vercel.com), create a **New Project** and import the repo.
2. Set **Root Directory** to `web` (or leave blank — `vercel.json` handles routing).
3. Add an environment variable `ENV_API_URL` = your Render URL.
4. Deploy. Done.

> **CORS**: `config.py` reads `FRONTEND_URL` from the Render environment and adds it to `ALLOWED_ORIGINS`. Make sure the Render env var matches your Vercel URL exactly.

---

## API Reference

| Method | Endpoint               | Description                          |
|--------|------------------------|--------------------------------------|
| GET    | `/health`              | Health check                         |
| GET    | `/api/warehouse`       | Full warehouse layout                |
| GET    | `/api/items`           | List items (supports `?q=` search)   |
| GET    | `/api/items/<id>`      | Single item                          |
| GET    | `/api/items/low-stock` | Items below reorder point            |
| GET    | `/api/robots`          | All robots + fleet summary           |
| GET    | `/api/robots/<id>`     | Single robot                         |
| POST   | `/api/robots/<id>/charge` | Charge robot to 100%            |
| POST   | `/api/path`            | A\* path: `{start:[x,y], goal:[x,y]}`|
| POST   | `/api/route`           | TSP: `{start:[x,y], stops:[[x,y]…]}` |
| POST   | `/api/pick`            | Pick order: `{item_ids:["ITM001"…]}` |

---

## Tests

```bash
bash run_tests.sh
```

Or directly:

```bash
pytest tests/ -v --cov=src
```
