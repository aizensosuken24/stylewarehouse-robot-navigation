"""Tests for TSP solver."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.navigation.tsp_solver import (
    euclidean_distance,
    nearest_neighbour_tsp,
    solve_tsp,
)


class TestEuclideanDistance:
    def test_same_point(self):
        assert euclidean_distance((0, 0), (0, 0)) == 0.0

    def test_horizontal(self):
        assert euclidean_distance((0, 0), (3, 0)) == 3.0

    def test_diagonal(self):
        d = euclidean_distance((0, 0), (3, 4))
        assert abs(d - 5.0) < 1e-9


class TestNearestNeighbour:
    def test_empty_stops(self):
        assert nearest_neighbour_tsp((0, 0), []) == []

    def test_single_stop(self):
        route = nearest_neighbour_tsp((0, 0), [(5, 5)])
        assert route == [(5, 5)]

    def test_visits_all_stops(self):
        stops = [(1, 0), (5, 5), (9, 9), (3, 3)]
        route = nearest_neighbour_tsp((0, 0), stops)
        assert set(route) == set(stops)
        assert len(route) == len(stops)


class TestSolveTSP:
    def test_empty_stops(self):
        result = solve_tsp((0, 0), [])
        assert result["num_stops"] == 0
        assert result["total_distance"] == 0.0

    def test_single_stop(self):
        result = solve_tsp((0, 0), [(5, 0)])
        assert result["num_stops"] == 1
        assert result["total_distance"] == 10.0  # 0→5→0

    def test_multiple_stops(self):
        stops = [(2, 0), (4, 0), (6, 0), (8, 0)]
        result = solve_tsp((0, 0), stops)
        assert result["num_stops"] == 4
        assert result["total_distance"] > 0
        assert len(result["route"]) == 4

    def test_all_stops_visited(self):
        stops = [(1, 1), (5, 5), (9, 1), (3, 8)]
        result = solve_tsp((0, 0), stops)
        assert set(map(tuple, result["route"])) == set(stops)

    def test_distance_positive(self):
        stops = [(1, 0), (2, 0), (3, 0)]
        result = solve_tsp((0, 0), stops, improve=False)
        assert result["total_distance"] > 0

    def test_improve_does_not_increase_distance(self):
        stops = [(9, 0), (0, 9), (9, 9), (0, 0), (5, 5)]
        r_no = solve_tsp((0, 0), stops, improve=False)
        r_yes = solve_tsp((0, 0), stops, improve=True)
        assert r_yes["total_distance"] <= r_no["total_distance"] + 1e-6

    def test_two_opt_closed_loop_optimization(self):
        stops = [(9, 0), (0, 9), (9, 9), (0, 0), (5, 5)]
        r_no = solve_tsp((0, 0), stops, improve=False)
        r_yes = solve_tsp((0, 0), stops, improve=True)
        assert r_yes["total_distance"] < r_no["total_distance"]
