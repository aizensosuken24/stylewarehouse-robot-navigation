# StyleWarehouse Robot Navigation — Web App

A warehouse path-planning dashboard with an interactive grid, obstacle editor, and A* / Dijkstra / BFS support.

## File Structure

```
stylewarehouse-web/
├── index.html          ← Frontend (deploy to Vercel / Netlify)
├── style.css
├── app.js
├── server.py           ← FastAPI backend (deploy to Render / Railway)
├── requirements-web.txt
├── vercel.json         ← Vercel config
├── netlify.toml        ← Netlify config
└── render.yaml         ← Render.com config
```

---

## Step 1 — Deploy the Python Backend (Render.com — free tier)

1. Push **all files** (including your existing `src/`, `data/`, etc.) to your GitLab repo.
2. Go to [render.com](https://render.com) → **New Web Service** → connect your GitLab repo.
3. Render auto-detects `render.yaml`. Click **Deploy**.
4. Wait ~2 min. Copy the live URL, e.g. `https://stylewarehouse-robot-api.onrender.com`

> **Connecting your own pathfinder:**  
> `server.py` tries `from pathfinder import find_path` first.  
> Make sure `src/pathfinder.py` exports `find_path(grid, start, end, algorithm, allow_diagonal) → List[List[int]]`.  
> If it can't import, the built-in A*/BFS/Dijkstra fallback is used automatically.

---

## Step 2 — Deploy the Frontend (Vercel)

1. Go to [vercel.com](https://vercel.com) → **Add New Project** → import your repo.
2. Set **Root Directory** to `stylewarehouse-web` (or wherever you put these files).
3. Framework preset: **Other** (it's plain HTML/CSS/JS).
4. Click **Deploy**. Done.

### Or deploy to Netlify

Drag and drop the `stylewarehouse-web/` folder onto [netlify.com/drop](https://app.netlify.com/drop).

---

## Step 3 — Connect Frontend to Backend

1. Open your deployed frontend URL.
2. In the **Backend API** section, paste your Render URL.
3. Click **Ping** — you should see "Backend online ✓".
4. Now **Find Path** sends requests to your real Python backend.

> **No backend yet?** The frontend has a built-in local BFS that runs in the browser — you can use the app immediately without a backend.

---

## API Contract

### `GET /health`
```json
{ "status": "ok", "builtin_pathfinder": false }
```

### `POST /navigate`
**Request:**
```json
{
  "grid": {
    "rows": 10,
    "cols": 10,
    "obstacles": [[2,3],[2,4],[2,5]]
  },
  "start": [0, 0],
  "end": [9, 9],
  "algorithm": "astar",
  "allow_diagonal": false
}
```

**Response:**
```json
{
  "path": [[0,0],[1,0],[2,0],...,[9,9]],
  "cost": 18,
  "algorithm": "astar",
  "compute_ms": 0.42
}
```

Return `path: []` when no path exists.

---

## Local Development

```bash
# Backend
pip install -r requirements-web.txt
uvicorn server:app --reload --port 8000

# Frontend — just open index.html in a browser
# Or use: npx serve .
```
