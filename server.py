"""
StyleWarehouse Robot Navigation — FastAPI Backend
Deploy on Render / Railway / any Python host.
This wraps your existing src/ navigation logic.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Tuple, Optional
import time, sys, os

# ── Make sure src/ is importable ──────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Try to import your actual pathfinder.
# If it doesn't exist yet, a built-in fallback is used.
try:
    from pathfinder import find_path          # your module
    USING_BUILTIN = False
except ImportError:
    USING_BUILTIN = True

app = FastAPI(title="StyleWarehouse Robot Navigation API", version="1.0.0")

# ── CORS — allow any origin (fine for Vercel/Netlify) ─
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── SCHEMAS ────────────────────────────────────────────
class GridSchema(BaseModel):
    rows: int
    cols: int
    obstacles: List[List[int]] = []

class NavigateRequest(BaseModel):
    grid: GridSchema
    start: List[int]
    end: List[int]
    algorithm: str = "astar"
    allow_diagonal: bool = False

class NavigateResponse(BaseModel):
    path: List[List[int]]
    cost: float
    algorithm: str
    compute_ms: float

# ── HEALTH ─────────────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok", "builtin_pathfinder": USING_BUILTIN}

# ── NAVIGATE ───────────────────────────────────────────
@app.post("/navigate", response_model=NavigateResponse)
def navigate(req: NavigateRequest):
    t0 = time.perf_counter()

    grid_data = {
        "rows":      req.grid.rows,
        "cols":      req.grid.cols,
        "obstacles": [tuple(o) for o in req.grid.obstacles],
    }

    if not USING_BUILTIN:
        # ── Delegate to your existing module ──────────
        try:
            path = find_path(
                grid=grid_data,
                start=tuple(req.start),
                end=tuple(req.end),
                algorithm=req.algorithm,
                allow_diagonal=req.allow_diagonal,
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        # ── Built-in BFS / A* fallback ────────────────
        path = _builtin_find_path(
            grid_data,
            tuple(req.start),
            tuple(req.end),
            req.algorithm,
            req.allow_diagonal,
        )

    ms = round((time.perf_counter() - t0) * 1000, 2)
    cost = len(path) - 1 if path else -1

    return NavigateResponse(
        path=path,
        cost=cost,
        algorithm=req.algorithm + ("-builtin" if USING_BUILTIN else ""),
        compute_ms=ms,
    )

# ── BUILT-IN PATHFINDER (BFS + A*) ────────────────────
from heapq import heappush, heappop
from collections import deque

def _builtin_find_path(grid, start, end, algorithm="astar", allow_diagonal=False):
    rows, cols = grid["rows"], grid["cols"]
    obs = set(map(tuple, grid["obstacles"]))

    dirs = [(-1,0),(1,0),(0,-1),(0,1)]
    if allow_diagonal:
        dirs += [(-1,-1),(-1,1),(1,-1),(1,1)]

    def neighbours(r, c):
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr,nc) not in obs:
                yield nr, nc

    def reconstruct(parent, node):
        path = []
        while node is not None:
            path.append(list(node))
            node = parent[node]
        return path[::-1]

    if algorithm in ("astar",):
        def h(r, c):
            return abs(r-end[0]) + abs(c-end[1])
        heap = [(h(*start), 0, start)]
        g = {start: 0}
        parent = {start: None}
        while heap:
            _, cost, cur = heappop(heap)
            if cur == end:
                return reconstruct(parent, end)
            if cost > g.get(cur, float("inf")):
                continue
            for nb in neighbours(*cur):
                nc = cost + 1
                if nc < g.get(nb, float("inf")):
                    g[nb] = nc
                    parent[nb] = cur
                    heappush(heap, (nc + h(*nb), nc, nb))
        return []

    elif algorithm == "dijkstra":
        heap = [(0, start)]
        dist = {start: 0}
        parent = {start: None}
        while heap:
            cost, cur = heappop(heap)
            if cur == end:
                return reconstruct(parent, end)
            for nb in neighbours(*cur):
                nc = cost + 1
                if nc < dist.get(nb, float("inf")):
                    dist[nb] = nc
                    parent[nb] = cur
                    heappush(heap, (nc, nb))
        return []

    else:  # bfs
        queue = deque([start])
        parent = {start: None}
        while queue:
            cur = queue.popleft()
            if cur == end:
                return reconstruct(parent, end)
            for nb in neighbours(*cur):
                if nb not in parent:
                    parent[nb] = cur
                    queue.append(nb)
        return []
