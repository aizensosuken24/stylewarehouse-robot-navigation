"""
TSP (Travelling Salesman Problem) solver for multi-stop warehouse route optimization.
Uses nearest-neighbour heuristic with 2-opt improvement.
"""
from typing import Callable, List, Tuple
import math


def euclidean_distance(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


def nearest_neighbour_tsp(start: Tuple[int, int],
                          stops: List[Tuple[int, int]],
                          distance_fn: Callable[[Tuple[int, int], Tuple[int, int]], float] = euclidean_distance) -> List[Tuple[int, int]]:
    """
    Greedy nearest-neighbour TSP heuristic.
    Returns ordered list of stops (not including start).
    """
    if not stops:
        return []

    unvisited = list(stops)
    route = []
    current = start

    while unvisited:
        nearest = min(unvisited, key=lambda s: distance_fn(current, s))
        route.append(nearest)
        unvisited.remove(nearest)
        current = nearest

    return route


def route_distance(
    start: Tuple[int, int],
    route: List[Tuple[int, int]],
    distance_fn: Callable[[Tuple[int, int], Tuple[int, int]], float] = euclidean_distance,
) -> float:
    """Calculate the round-trip distance for a route that starts and ends at start."""
    if not route:
        return 0.0

    full_path = [start] + list(route) + [start]
    return sum(
        distance_fn(full_path[i], full_path[i + 1])
        for i in range(len(full_path) - 1)
    )


def two_opt_improve(route: List[Tuple[int, int]],
                    start: Tuple[int, int],
                    distance_fn: Callable[[Tuple[int, int], Tuple[int, int]], float] = euclidean_distance,
                    max_iterations: int = 100) -> List[Tuple[int, int]]:
    """
    2-opt local search improvement for TSP route.
    Reverses sub-sequences to reduce total distance.
    """
    if len(route) < 3:
        return list(route)

    best_route = list(route)
    best_distance = route_distance(start, best_route, distance_fn)
    iteration = 0
    improved = True

    while improved and iteration < max_iterations:
        improved = False
        iteration += 1

        for i in range(len(best_route) - 1):
            for j in range(i + 1, len(best_route)):
                candidate = (
                    best_route[:i]
                    + list(reversed(best_route[i:j + 1]))
                    + best_route[j + 1:]
                )
                candidate_distance = route_distance(start, candidate, distance_fn)

                if candidate_distance < best_distance - 1e-10:
                    best_route = candidate
                    best_distance = candidate_distance
                    improved = True

        if improved:
            continue

    return best_route


def solve_tsp(start: Tuple[int, int],
              stops: List[Tuple[int, int]],
              improve: bool = True,
              distance_fn: Callable[[Tuple[int, int], Tuple[int, int]], float] = euclidean_distance) -> dict:
    """
    Solve the TSP for warehouse pick route.

    Args:
        start: Robot starting position (x, y)
        stops: List of shelf positions to visit
        improve: Apply 2-opt improvement

    Returns:
        dict with 'route', 'total_distance', 'num_stops'
    """
    if not stops:
        return {"route": [], "total_distance": 0.0, "num_stops": 0}

    route = nearest_neighbour_tsp(start, stops, distance_fn=distance_fn)

    if improve and len(route) >= 3:
        route = two_opt_improve(route, start, distance_fn=distance_fn)

    # Calculate total distance
    total_dist = route_distance(start, route, distance_fn)

    return {
        "route": route,
        "total_distance": round(total_dist, 2),
        "num_stops": len(route),
        "start": start
    }
