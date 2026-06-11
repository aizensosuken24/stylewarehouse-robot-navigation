"""
tests/test_robot.py
Unit tests for Robot and Order classes.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from src.warehouse.map import build_default_map
from src.warehouse.catalogue import ItemCatalogue, Item
from src.robot.robot import Robot
from src.robot.order import Order, OrderLine


# ── Helpers ───────────────────────────────────────────────────────────────────

def make_catalogue():
    cat = ItemCatalogue()
    cat.add_item(Item("SW001","Classic Tee","Tops","StyleCo","M","White",0,3,10))
    cat.add_item(Item("SW002","Slim Jeans","Trousers","DenimX","32","Blue",0,6,5))
    cat.add_item(Item("SW003","Hoodie","Tops","StreetWear","L","Black",0,9,8))
    return cat

def make_robot():
    wm  = build_default_map()
    cat = make_catalogue()
    return Robot("TestBot", wm, cat), wm, cat


# ── Order tests ───────────────────────────────────────────────────────────────

class TestOrder(unittest.TestCase):

    def test_add_items(self):
        o = Order("ORD-001", [("SW001", 1), ("SW002", 2)])
        self.assertEqual(len(o), 2)

    def test_mark_picked(self):
        o = Order("ORD-002", [("SW001", 1)])
        self.assertFalse(o.is_complete())
        o.mark_picked("SW001")
        self.assertTrue(o.is_complete())

    def test_pending_skus(self):
        o = Order("ORD-003", [("SW001", 1), ("SW002", 1)])
        o.mark_picked("SW001")
        self.assertEqual(o.pending_skus(), ["SW002"])

    def test_summary(self):
        o = Order("ORD-004", [("SW001", 1)])
        summary = o.summary()
        self.assertIn("ORD-004", summary)

    def test_duplicate_sku_adds_quantity(self):
        o = Order("ORD-005")
        o.add_item("SW001", 2)
        o.add_item("SW001", 3)
        self.assertEqual(o.lines["SW001"].quantity, 5)


# ── Robot tests ───────────────────────────────────────────────────────────────

class TestRobot(unittest.TestCase):

    def test_initial_position(self):
        robot, _, _ = make_robot()
        self.assertEqual(robot.position, (0, 0))

    def test_navigate_to_reachable(self):
        robot, _, _ = make_robot()
        path = robot.navigate_to((0, 6), verbose=False)
        self.assertIsNotNone(path)
        self.assertEqual(robot.position, (0, 6))

    def test_battery_decreases(self):
        robot, _, _ = make_robot()
        initial_battery = robot.battery
        robot.navigate_to((0, 6), verbose=False)
        self.assertLess(robot.battery, initial_battery)

    def test_recharge(self):
        robot, _, _ = make_robot()
        robot.battery = 10
        robot.recharge()
        from config import ROBOT_BATTERY_CAPACITY
        self.assertEqual(robot.battery, ROBOT_BATTERY_CAPACITY)

    def test_execute_order(self):
        robot, _, _ = make_robot()
        order = Order("ORD-TEST", [("SW001", 1), ("SW002", 1)])
        result = robot.execute_order(order, verbose=False)
        self.assertTrue(result)
        self.assertTrue(order.is_complete())

    def test_execute_order_unknown_sku(self):
        robot, _, _ = make_robot()
        order = Order("ORD-BAD", [("UNKNOWN_SKU", 1)])
        result = robot.execute_order(order, verbose=False)
        # Should handle gracefully and return False (nothing picked)
        self.assertFalse(result)

    def test_robot_returns_to_depot(self):
        robot, _, _ = make_robot()
        order = Order("ORD-DEPOT", [("SW001", 1)])
        robot.execute_order(order, verbose=False)
        self.assertEqual(robot.position, (0, 0))


# ── Catalogue tests ───────────────────────────────────────────────────────────

class TestCatalogue(unittest.TestCase):

    def test_find_existing(self):
        cat = make_catalogue()
        item = cat.find("SW001")
        self.assertIsNotNone(item)
        self.assertEqual(item.name, "Classic Tee")

    def test_find_missing(self):
        cat = make_catalogue()
        self.assertIsNone(cat.find("NOPE"))

    def test_search_by_name(self):
        cat = make_catalogue()
        results = cat.search_by_name("tee")
        self.assertTrue(any(i.sku == "SW001" for i in results))

    def test_len(self):
        cat = make_catalogue()
        self.assertEqual(len(cat), 3)

    def test_items_at(self):
        cat = make_catalogue()
        items = cat.items_at(0, 3)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].sku, "SW001")


if __name__ == "__main__":
    unittest.main()
