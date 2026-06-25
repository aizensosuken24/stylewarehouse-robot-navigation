"""Tests for A* pathfinder."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from src.navigation.pathfinder import AStarPathfinder, Node


@pytest.fixture
def empty_grid():
    return AStarPathfinder(10, 10)


@pytest.fixture
def grid_with_wall():
    pf = AStarPathfinder(10, 10)
    # Vertical wall at x=5, y=0..8
    pf.set_obstacles({(5, y) for y in range(9)})
    return pf


class TestNode:
    def test_equality(self):
        assert Node(1, 2) == Node(1, 2)

    def test_hash(self):
        s = {Node(1, 2), Node(1, 2), Node(3, 4)}
        assert len(s) == 2

    def test_lt(self):
        a = Node(0, 0, g=1, h=1)
        b = Node(0, 0, g=5, h=5)
        assert a < b


class TestAStarPathfinder:
    def test_same_start_goal(self, empty_grid):
        path = empty_grid.find_path((0, 0), (0, 0))
        assert path == [(0, 0)]

    def test_simple_path(self, empty_grid):
        path = empty_grid.find_path((0, 0), (3, 0))
        assert path is not None
        assert path[0] == (0, 0)
        assert path[-1] == (3, 0)
        assert len(path) == 4

    def test_no_path_blocked(self):
        pf = AStarPathfinder(5, 5)
        # Block entire column
        pf.set_obstacles({(2, y) for y in range(5)})
        path = pf.find_path((0, 0), (4, 0))
        assert path is None

    def test_path_around_wall(self, grid_with_wall):
        # Must go around x=5 wall
        path = grid_with_wall.find_path((0, 0), (9, 0))
        assert path is not None
        assert path[-1] == (9, 0)
        # Path must go through y=9 (gap in wall)
        xs = [p[0] for p in path]
        assert 5 in xs  # crosses x=5 at y=9

    def test_out_of_bounds_start(self, empty_grid):
        path = empty_grid.find_path((-1, 0), (5, 5))
        assert path is None

    def test_out_of_bounds_goal(self, empty_grid):
        path = empty_grid.find_path((0, 0), (20, 20))
        assert path is None

    def test_path_length(self, empty_grid):
        path = empty_grid.find_path((0, 0), (3, 4))
        assert path is not None
        length = empty_grid.path_length(path)
        assert length > 0

    def test_add_remove_obstacle(self, empty_grid):
        empty_grid.add_obstacle(1, 0)
        path = empty_grid.find_path((0, 0), (2, 0))
        # Path should avoid (1,0)
        assert path is not None
        assert (1, 0) not in path

        empty_grid.remove_obstacle(1, 0)
        path2 = empty_grid.find_path((0, 0), (2, 0))
        assert (1, 0) in path2  # Direct path now available

    def test_diagonal_heuristic(self):
        pf = AStarPathfinder(10, 10, allow_diagonal=True)
        node_a = Node(0, 0)
        node_b = Node(1, 1)
        h = pf.heuristic(node_a, node_b)
        assert abs(h - 1.41421356237) < 1e-9

        path = pf.find_path((0, 0), (1, 1))
        assert path == [(0, 0), (1, 1)]
