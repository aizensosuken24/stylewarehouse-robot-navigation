# Research — StyleWarehouse Robot Navigation

## Pathfinding Algorithms Considered

### 1. Dijkstra's Algorithm
- Guarantees shortest path in weighted graphs
- O((V + E) log V) with a priority queue
- Best when all edge weights differ significantly
- **Chosen for baseline implementation**

### 2. A* (A-Star)
- Dijkstra + heuristic (Manhattan distance for grids)
- Faster in practice because it is goal-directed
- Same optimality guarantee when heuristic is admissible
- **Chosen for primary pathfinding** (faster on large maps)

### 3. D* Lite
- Incremental replanning — handles dynamic obstacles
- More complex to implement
- **Stretch goal for obstacle-aware navigation**

### 4. Travelling Salesman (TSP) approximation
- Required when an order has many items (multi-stop)
- Nearest-neighbour heuristic gives good-enough routes fast
- Google OR-Tools gives optimal but needs extra dependency
- **Chosen: Nearest-neighbour TSP for order sequencing**

## Warehouse Representation

| Approach | Pros | Cons |
|----------|------|------|
| Grid (2-D array) | Simple, fast lookup | Coarse resolution |
| Graph (nodes/edges) | Flexible topology | More complex |
| Occupancy map (bitmap) | Real-sensor ready | Overkill for MVP |

**Chosen:** Grid with cell types: `OPEN`, `SHELF`, `AISLE`, `DEPOT`, `OBSTACLE`.

## References
- Dijkstra (1959) — "A note on two problems in connexion with graphs"
- Hart et al. (1968) — "A Formal Basis for the Heuristic Determination of Minimum Cost Paths"
- Smaoui, F. (2024) — "Smart Navigation in Warehouses: Dijkstra's Algorithm" (Medium)
- Dapke, A. — "Path Planning for Autonomous Robots" (GitHub)
