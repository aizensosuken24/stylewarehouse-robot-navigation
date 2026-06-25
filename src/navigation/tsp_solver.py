"""
TSP (Travelling Salesman Problem) solver for multi-stop warehouse route optimization.
Uses nearest-neighbour heuristic with 2-opt improvement.
"""
from typing import List, Tuple, Optional
import math


def euclidean_distance(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


def nearest_neighbour_tsp(start: Tuple[int, int],
                          stops: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
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
        nearest = min(unvisited, key=lambda s: euclidean_distance(current, s))
        route.append(nearest)
        unvisited.remove(nearest)
        current = nearest

    return route


def two_opt_improve(route: List[Tuple[int, int]],
                    start: Tuple[int, int],
                    max_iterations: int = 100) -> List[Tuple[int, int]]:
    """
    2-opt local search improvement for TSP route.
    Reverses sub-sequences to reduce total distance.
    """
    if len(route) < 3:
        return route

    full = [start] + list(route)
    improved = True
    iteration = 0

    while improved and iteration < max_iterations:
        improved = False
        iteration += 1
        for i in range(1, len(full)):
            for j in range(i + 1, len(full) + 1):
                next_node = full[j] if j < len(full) else full[0]
                d_before = (euclidean_distance(full[i-1], full[i]) +
                            euclidean_distance(full[j-1], next_node))
                d_after  = (euclidean_distance(full[i-1], full[j-1]) +
                            euclidean_distance(full[i], next_node))

                if d_after < d_before - 1e-10:
                    full[i:j] = full[i:j][::-1]
                    improved = True

    return full[1:]  # Remove start


def solve_tsp(start: Tuple[int, int],
              stops: List[Tuple[int, int]],
              improve: bool = True) -> dict:
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

    route = nearest_neighbour_tsp(start, stops)

    if improve and len(route) >= 3:
        route = two_opt_improve(route, start)

    # Calculate total distance
    full_path = [start] + route + [start]
    total_dist = sum(
        euclidean_distance(full_path[i], full_path[i+1])
        for i in range(len(full_path) - 1)
    )

    return {
        "route": route,
        "total_distance": round(total_dist, 2),
        "num_stops": len(route),
        "start": start
    }
