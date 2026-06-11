#!/usr/bin/env python3
"""StyleWarehouse robot navigation demo entrypoint."""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from config import ALGORITHM, CATALOGUE_FILE, DEPOT_POSITION
from src.navigation.pathfinder import find_path
from src.robot.order import Order
from src.robot.robot import Robot
from src.ui.visualiser import animate_path, animate_pygame, print_map
from src.utils.output import safe_print
from src.warehouse.catalogue import ItemCatalogue
from src.warehouse.map import build_default_map


DEMO_ORDER = [
    ("SW001", 1),
    ("SW007", 1),
    ("SW013", 1),
    ("SW021", 1),
    ("SW033", 1),
]


def load_system():
    """Load the warehouse map and item catalogue."""
    warehouse_map = build_default_map()
    catalogue = ItemCatalogue()

    if os.path.exists(CATALOGUE_FILE):
        catalogue.load_from_csv(CATALOGUE_FILE)
    else:
        safe_print(f"[!] Catalogue not found at {CATALOGUE_FILE} - using empty catalogue")

    return warehouse_map, catalogue


def interactive(warehouse_map, catalogue, robot, use_pygame: bool = False):
    safe_print("\n" + "=" * 55)
    safe_print("  [BOT] StyleWarehouse Robot Navigation System")
    safe_print("=" * 55)
    safe_print(f"  Warehouse : {warehouse_map.rows} x {warehouse_map.cols} grid")
    safe_print(f"  Catalogue : {len(catalogue)} items")
    safe_print(f"  Algorithm : {ALGORITHM.upper()}")
    safe_print(f"  Robot     : {robot.name} @ depot {DEPOT_POSITION}")
    safe_print("=" * 55)

    print_map(warehouse_map, robot_pos=robot.position, title="Initial Warehouse State")

    while True:
        safe_print("\nOptions:")
        safe_print("  1. Place a new order")
        safe_print("  2. Show warehouse map")
        safe_print("  3. Search catalogue")
        safe_print("  4. Show robot status")
        safe_print("  5. Run demo order")
        safe_print("  0. Exit")
        choice = input("\nEnter choice: ").strip()

        if choice == "0":
            safe_print("Goodbye!")
            break

        if choice == "1":
            order_id = input("Order ID (e.g. ORD-001): ").strip() or "ORD-001"
            order = Order(order_id)
            safe_print("Enter SKUs to pick (blank line to finish):")
            while True:
                sku = input("  SKU: ").strip().upper()
                if not sku:
                    break
                qty_str = input("  Qty [1]: ").strip()
                quantity = int(qty_str) if qty_str.isdigit() else 1
                order.add_item(sku, quantity)

            if not order.lines:
                safe_print("No items added.")
                continue

            safe_print(f"\nExecuting {order}")
            robot.execute_order(order, verbose=True)
            if use_pygame:
                _show_pygame_for_order(warehouse_map, robot, order, catalogue)
            continue

        if choice == "2":
            print_map(warehouse_map, robot_pos=robot.position)
            continue

        if choice == "3":
            keyword = input("Search keyword: ").strip()
            results = catalogue.search_by_name(keyword)
            if results:
                for item in results:
                    safe_print(f"  {item}")
            else:
                safe_print("  No results.")
            continue

        if choice == "4":
            safe_print(robot.status())
            continue

        if choice == "5":
            order = Order("DEMO-001", DEMO_ORDER)
            safe_print(f"\nRunning demo order: {[sku for sku, _ in DEMO_ORDER]}")
            robot.execute_order(order, verbose=True)
            if use_pygame:
                _show_pygame_for_order(warehouse_map, robot, order, catalogue)
            else:
                _show_terminal_animation(warehouse_map, order, catalogue)
            continue

        safe_print("Invalid choice.")


def _show_terminal_animation(warehouse_map, order, catalogue):
    """Replay the robot path in the terminal for the selected order."""
    positions = [DEPOT_POSITION]
    for sku in order.picked_skus() or [sku for sku, _ in DEMO_ORDER]:
        item = catalogue.find(sku)
        if item:
            positions.append(item.location)
    positions.append(DEPOT_POSITION)

    full_path = [positions[0]]
    for index in range(len(positions) - 1):
        segment = find_path(warehouse_map, positions[index], positions[index + 1], ALGORITHM)
        if segment:
            full_path.extend(segment[1:])

    animate_path(warehouse_map, full_path, delay=0.05, title="Robot Route Animation")


def _show_pygame_for_order(warehouse_map, robot, order, catalogue):
    """Animate the path for a completed order in pygame."""
    positions = [DEPOT_POSITION]
    for sku in order.picked_skus():
        item = catalogue.find(sku)
        if item:
            positions.append(item.location)
    positions.append(DEPOT_POSITION)

    full_path = [positions[0]]
    for index in range(len(positions) - 1):
        segment = find_path(warehouse_map, positions[index], positions[index + 1], ALGORITHM)
        if segment:
            full_path.extend(segment[1:])

    animate_pygame(warehouse_map, full_path)


def auto_demo(warehouse_map, catalogue, use_pygame: bool = False):
    """Run the non-interactive demo order."""
    robot = Robot("AutoBot", warehouse_map, catalogue)
    order = Order("AUTO-001", DEMO_ORDER)

    safe_print("\n" + "=" * 55)
    safe_print("  [BOT] StyleWarehouse - Auto Demo")
    safe_print("=" * 55)
    print_map(warehouse_map, title="Warehouse Layout")

    robot.execute_order(order, verbose=True)

    if use_pygame:
        _show_pygame_for_order(warehouse_map, robot, order, catalogue)
    else:
        _show_terminal_animation(warehouse_map, order, catalogue)


def main():
    parser = argparse.ArgumentParser(description="StyleWarehouse Robot Navigation")
    parser.add_argument("--auto", action="store_true", help="Run auto demo and exit")
    parser.add_argument("--pygame", action="store_true", help="Use pygame visualiser")
    args = parser.parse_args()

    warehouse_map, catalogue = load_system()
    robot = Robot("StyleBot-1", warehouse_map, catalogue)

    if args.auto:
        auto_demo(warehouse_map, catalogue, use_pygame=args.pygame)
    else:
        interactive(warehouse_map, catalogue, robot, use_pygame=args.pygame)


if __name__ == "__main__":
    main()
