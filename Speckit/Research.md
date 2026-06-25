# Research

## Pathfinding Algorithms Considered

### A* (chosen)
- Optimal and complete for weighted grids
- Heuristic: Manhattan distance (no diagonal movement default)
- Time complexity: O(E log V) where E = edges, V = vertices
- Well-suited for sparse warehouse grids with wall obstacles

### Dijkstra
- Optimal but no heuristic — slower than A* in practice
- Considered and rejected in favour of A*

### BFS
- Optimal only for uniform-cost grids
- Fast but no heuristic; acceptable fallback if no weights needed

## TSP Heuristics Considered

### Nearest-Neighbour (chosen as base)
- O(n²) greedy construction
- Gets within ~20-25% of optimal on average
- Simple to implement; good enough for warehouse pick orders (n < 50 stops)

### 2-opt Improvement (applied on top)
- Iteratively reverses sub-routes to eliminate crossings
- Reduces NN tour length by ~5-10% in practice
- O(n²) per iteration, fast for small n

### Exact TSP (rejected for MVP)
- Optimal but exponential; impractical for n > 20 stops without specialised solver

## Deployment Research

### Backend: Render
- Free tier supports Python web services
- Auto-detects render.yaml blueprint
- Injects PORT environment variable automatically
- Supports gunicorn WSGI out of the box

### Frontend: Vercel
- Zero-config static deploy from vercel.json
- CDN-backed globally; ideal for dashboard SPA
- Environment variables set per-project in dashboard

## CORS Strategy
- Flask-CORS reads allowed origins from config.ALLOWED_ORIGINS
- FRONTEND_URL env var set on Render to Vercel deployment URL
- Supports multiple origins (local dev + production) via comma-separated ALLOWED_ORIGINS
