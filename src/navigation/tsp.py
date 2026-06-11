"""
navigation/tsp.py
Solves the multi-stop sequencing problem (a.k.a. Travelling Salesman) for
warehouse orders using a Nearest-Neighbour heuristic.

For warehouse orders with ≤ 15 stops this gives routes within ~25% of optimal
with negligible compute time.
"""
from __future__ import annotations
from typing import Callable, List, Optional, Tuple

Pos = Tuple[int, int]


def manhattan(a: Pos, b: Pos) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def nearest_neighbour(
    stops: List[Pos],
    start: Pos,
    dist_fn: Callable[[Pos, Pos], float] = manhattan,
) -> List[Pos]:
    """
    Greedy nearest-neighbour TSP starting from `start`.

    Returns an ordered list of stops (does NOT include `start` at index 0
    unless it is also in `stops`).

    Args:
        stops:   list of (row, col) positions to visit
        start:   starting position (robot's current location or depot)
        dist_fn: distance function between two positions

    Returns:
        Ordered list of positions to visit.
    """
    if not stops:
        return []

    remaining = list(stops)
    route: List[Pos] = []
    current = start

    while remaining:
        nearest = min(remaining, key=lambda p: dist_fn(current, p))
        route.append(nearest)
        remaining.remove(nearest)
        current = nearest

    return route


def two_opt_improve(
    route: List[Pos],
    start: Pos,
    dist_fn: Callable[[Pos, Pos], float] = manhattan,
    max_passes: int = 5,
) -> List[Pos]:
    """
    Improve a route using the 2-opt local search.
    Iteratively reverses sub-sequences if doing so reduces total distance.

    Typically cuts 5–15% off the nearest-neighbour solution.
    """
    best = list(route)
    improved = True
    passes = 0

    while improved and passes < max_passes:
        improved = False
        passes += 1
        for i in range(len(best) - 1):
            for j in range(i + 2, len(best)):
                # Reverse the segment best[i+1 … j]
                candidate = best[: i + 1] + best[i + 1 : j + 1][::-1] + best[j + 1 :]
                if _total_distance([start] + candidate, dist_fn) < _total_distance(
                    [start] + best, dist_fn
                ):
                    best = candidate
                    improved = True
    return best


def _total_distance(
    path: List[Pos], dist_fn: Callable[[Pos, Pos], float] = manhattan
) -> float:
    return sum(dist_fn(path[i], path[i + 1]) for i in range(len(path) - 1))


def sequence_order(
    stops: List[Pos],
    start: Pos,
    use_two_opt: bool = True,
) -> List[Pos]:
    """
    Public API: sequence a list of pick stops optimally from `start`.

    Returns the ordered list of stops to visit.
    """
    route = nearest_neighbour(stops, start)
    if use_two_opt and len(route) > 2:
        route = two_opt_improve(route, start)
    return route


def total_route_distance(stops: List[Pos], start: Pos, end: Optional[Pos] = None) -> int:
    """
    Estimate total Manhattan distance for a sequenced route.
    Includes return to `end` (usually the depot) if provided.
    """
    full = [start] + stops
    if end is not None:
        full.append(end)
    return int(_total_distance(full))
