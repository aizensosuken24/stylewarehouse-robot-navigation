"""
tests/test_pathfinder.py
Unit tests for the A* and Dijkstra pathfinders.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from src.warehouse.map import WarehouseMap, build_default_map
from src.navigation.pathfinder import astar, dijkstra, find_path, path_length
from config import CELL_OBSTACLE


class SimpleGrid:
    """Minimal 5×5 open grid for isolated pathfinder testing."""
    def __init__(self, rows=5, cols=5, obstacles=None):
        self.rows = rows
        self.cols = cols
        self.grid = [[0]*cols for _ in range(rows)]
        for r, c in (obstacles or []):
            self.grid[r][c] = CELL_OBSTACLE

    def is_walkable(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] != CELL_OBSTACLE

    def neighbours(self, r, c):
        return [(nr, nc) for nr, nc in [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]
                if self.is_walkable(nr, nc)]


class TestAstar(unittest.TestCase):

    def test_same_start_goal(self):
        g = SimpleGrid()
        path = astar(g, (0,0), (0,0))
        self.assertEqual(path, [(0,0)])

    def test_simple_path(self):
        g = SimpleGrid()
        path = astar(g, (0,0), (4,4))
        self.assertIsNotNone(path)
        self.assertEqual(path[0], (0,0))
        self.assertEqual(path[-1], (4,4))
        self.assertEqual(path_length(path), 8)   # Manhattan optimal

    def test_no_path(self):
        # Wall of obstacles across column 2
        obs = [(r, 2) for r in range(5)]
        g = SimpleGrid(obstacles=obs)
        path = astar(g, (0,0), (0,4))
        self.assertIsNone(path)

    def test_path_around_obstacle(self):
        # Single obstacle at (0,1) — must go around
        g = SimpleGrid(obstacles=[(0,1)])
        path = astar(g, (0,0), (0,2))
        self.assertIsNotNone(path)
        self.assertNotIn((0,1), path)
        self.assertEqual(path[-1], (0,2))

    def test_adjacent_goal(self):
        g = SimpleGrid()
        path = astar(g, (2,2), (2,3))
        self.assertEqual(path_length(path), 1)


class TestDijkstra(unittest.TestCase):

    def test_same_result_as_astar(self):
        g = SimpleGrid()
        p_a = astar(g, (0,0), (4,4))
        p_d = dijkstra(g, (0,0), (4,4))
        self.assertEqual(path_length(p_a), path_length(p_d))

    def test_no_path(self):
        obs = [(r, 2) for r in range(5)]
        g = SimpleGrid(obstacles=obs)
        self.assertIsNone(dijkstra(g, (0,0), (0,4)))


class TestFindPath(unittest.TestCase):

    def test_dispatcher_astar(self):
        g = SimpleGrid()
        path = find_path(g, (0,0), (3,3), algorithm="astar")
        self.assertIsNotNone(path)

    def test_dispatcher_dijkstra(self):
        g = SimpleGrid()
        path = find_path(g, (0,0), (3,3), algorithm="dijkstra")
        self.assertIsNotNone(path)

    def test_dispatcher_invalid(self):
        g = SimpleGrid()
        with self.assertRaises(ValueError):
            find_path(g, (0,0), (1,1), algorithm="bfs")


class TestWarehouseMap(unittest.TestCase):

    def test_default_map_walkable(self):
        wm = build_default_map()
        # depot should be walkable
        self.assertTrue(wm.is_walkable(0, 0))

    def test_out_of_bounds_not_walkable(self):
        wm = build_default_map()
        self.assertFalse(wm.is_walkable(-1, 0))
        self.assertFalse(wm.is_walkable(999, 999))

    def test_path_on_real_map(self):
        wm = build_default_map()
        path = astar(wm, (0,0), (0,6))
        self.assertIsNotNone(path)


if __name__ == "__main__":
    unittest.main()
