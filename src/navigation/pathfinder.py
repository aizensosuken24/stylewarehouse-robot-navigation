"""
navigation/pathfinder.py
Provides A* and Dijkstra pathfinding on a WarehouseMap grid.
"""
from __future__ import annotations
import heapq
import math
from typing import Dict, List, Optional, Tuple

# Type alias
Pos = Tuple[int, int]


# ── Heuristics ────────────────────────────────────────────────────────────────

def manhattan(a: Pos, b: Pos) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def euclidean(a: Pos, b: Pos) -> float:
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


# ── A* ────────────────────────────────────────────────────────────────────────

def astar(grid_map, start: Pos, goal: Pos) -> Optional[List[Pos]]:
    """
    Find the shortest path from `start` to `goal` on `grid_map` using A*.

    Args:
        grid_map: a WarehouseMap instance (must implement .neighbours())
        start:    (row, col) start position
        goal:     (row, col) goal position

    Returns:
        Ordered list of (row, col) positions from start to goal (inclusive),
        or None if no path exists.
    """
    if start == goal:
        return [start]

    open_heap: List[Tuple[float, Pos]] = []
    heapq.heappush(open_heap, (0.0, start))

    came_from: Dict[Pos, Optional[Pos]] = {start: None}
    g_score: Dict[Pos, float] = {start: 0.0}

    while open_heap:
        _, current = heapq.heappop(open_heap)

        if current == goal:
            return _reconstruct(came_from, goal)

        for nb in grid_map.neighbours(*current):
            tentative_g = g_score[current] + 1  # uniform edge cost
            if tentative_g < g_score.get(nb, float("inf")):
                came_from[nb] = current
                g_score[nb] = tentative_g
                f = tentative_g + manhattan(nb, goal)
                heapq.heappush(open_heap, (f, nb))

    return None  # no path found


# ── Dijkstra ──────────────────────────────────────────────────────────────────

def dijkstra(grid_map, start: Pos, goal: Pos) -> Optional[List[Pos]]:
    """
    Find the shortest path using Dijkstra's algorithm (no heuristic).
    Slower than A* but useful as a correctness reference.
    """
    if start == goal:
        return [start]

    open_heap: List[Tuple[float, Pos]] = []
    heapq.heappush(open_heap, (0.0, start))

    came_from: Dict[Pos, Optional[Pos]] = {start: None}
    dist: Dict[Pos, float] = {start: 0.0}

    while open_heap:
        d, current = heapq.heappop(open_heap)

        if current == goal:
            return _reconstruct(came_from, goal)

        if d > dist.get(current, float("inf")):
            continue

        for nb in grid_map.neighbours(*current):
            new_d = dist[current] + 1
            if new_d < dist.get(nb, float("inf")):
                dist[nb] = new_d
                came_from[nb] = current
                heapq.heappush(open_heap, (new_d, nb))

    return None


# ── Path utility ──────────────────────────────────────────────────────────────

def _reconstruct(came_from: Dict[Pos, Optional[Pos]], goal: Pos) -> List[Pos]:
    path: List[Pos] = []
    node: Optional[Pos] = goal
    while node is not None:
        path.append(node)
        node = came_from[node]
    path.reverse()
    return path


def path_length(path: List[Pos]) -> int:
    """Number of steps in a path (edges, not nodes)."""
    return max(0, len(path) - 1)


def find_path(grid_map, start: Pos, goal: Pos, algorithm: str = "astar") -> Optional[List[Pos]]:
    """Dispatcher: choose algorithm by name."""
    if algorithm == "astar":
        return astar(grid_map, start, goal)
    elif algorithm == "dijkstra":
        return dijkstra(grid_map, start, goal)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm!r}. Use 'astar' or 'dijkstra'.")
