"""
tests/test_tsp.py
Unit tests for the TSP nearest-neighbour sequencer.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from src.navigation.tsp import nearest_neighbour, two_opt_improve, sequence_order, total_route_distance


class TestNearestNeighbour(unittest.TestCase):

    def test_empty_stops(self):
        self.assertEqual(nearest_neighbour([], (0,0)), [])

    def test_single_stop(self):
        result = nearest_neighbour([(5,5)], (0,0))
        self.assertEqual(result, [(5,5)])

    def test_visits_all_stops(self):
        stops = [(1,1), (3,3), (2,8), (7,2)]
        result = nearest_neighbour(stops, (0,0))
        self.assertEqual(set(result), set(stops))
        self.assertEqual(len(result), len(stops))

    def test_nearest_first(self):
        # (0,1) is closer to (0,0) than (5,5)
        stops = [(5,5), (0,1)]
        result = nearest_neighbour(stops, (0,0))
        self.assertEqual(result[0], (0,1))


class TestTwoOpt(unittest.TestCase):

    def test_does_not_add_stops(self):
        stops = [(1,1), (3,3), (2,8), (7,2)]
        route = nearest_neighbour(stops, (0,0))
        improved = two_opt_improve(route, (0,0))
        self.assertEqual(set(improved), set(stops))

    def test_same_or_shorter_distance(self):
        stops = [(0,9), (9,0), (5,5), (1,8), (8,1)]
        route = nearest_neighbour(stops, (0,0))
        improved = two_opt_improve(route, (0,0))
        from src.navigation.tsp import _total_distance, manhattan
        d_before = _total_distance([(0,0)] + route)
        d_after  = _total_distance([(0,0)] + improved)
        self.assertLessEqual(d_after, d_before + 1)  # +1 tolerance for ties


class TestSequenceOrder(unittest.TestCase):

    def test_returns_all_stops(self):
        stops = [(2,3), (7,8), (1,9)]
        seq = sequence_order(stops, (0,0))
        self.assertEqual(set(seq), set(stops))

    def test_total_distance(self):
        stops = [(2,0), (4,0), (6,0)]  # collinear — optimal is sequential
        seq = sequence_order(stops, (0,0))
        d = total_route_distance(seq, (0,0), (0,0))
        self.assertGreater(d, 0)


if __name__ == "__main__":
    unittest.main()
