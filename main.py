#!/usr/bin/env python3
"""
main.py — StyleWarehouse Robot Navigation Demo
================================================
Runs an interactive simulation of the warehouse robot.

Usage:
    python main.py                  # interactive mode
    python main.py --auto           # auto-demo with sample order
    python main.py --pygame         # use pygame visualiser (requires: pip install pygame)
"""
from __future__ import annotations
import sys, os, argparse

# Make src importable
sys.path.insert(0, os.path.dirname(__file__))

from src.warehouse.map import build_default_map
from src.warehouse.catalogue import ItemCatalogue
from src.robot.robot import Robot
from src.robot.order import Order
from src.ui.visualiser import print_map, animate_path, animate_pygame
from src.navigation.pathfinder import find_path
from config import DEPOT_POSITION, CATALOGUE_FILE, ALGORITHM


# ── Setup ─────────────────────────────────────────────────────────────────────

def load_system():
    """Load warehouse map and item catalogue."""
    wm = build_default_map()

    cat = ItemCatalogue()
    if os.path.exists(CATALOGUE_FILE):
        cat.load_from_csv(CATALOGUE_FILE)
    else:
        print(f"⚠ Catalogue not found at {CATALOGUE_FILE} — using empty catalogue")

    return wm, cat


# ── Demo order ────────────────────────────────────────────────────────────────

DEMO_ORDER = [
    ("SW001", 1),   # Classic Tee
    ("SW007", 1),   # Slim Jeans
    ("SW013", 1),   # Bomber Jacket
    ("SW021", 1),   # Canvas Sneaker
    ("SW033", 1),   # Woollen Scarf
]


# ── Interactive mode ──────────────────────────────────────────────────────────

def interactive(wm, cat, robot, use_pygame: bool = False):
    print("\n" + "="*55)
    print("  🤖  StyleWarehouse Robot Navigation System")
    print("="*55)
    print(f"  Warehouse : {wm.rows} × {wm.cols} grid")
    print(f"  Catalogue : {len(cat)} items")
    print(f"  Algorithm : {ALGORITHM.upper()}")
    print(f"  Robot     : {robot.name}  @ depot {DEPOT_POSITION}")
    print("="*55)

    print_map(wm, robot_pos=robot.position, title="Initial Warehouse State")

    while True:
        print("\nOptions:")
        print("  1. Place a new order")
        print("  2. Show warehouse map")
        print("  3. Search catalogue")
        print("  4. Show robot status")
        print("  5. Run demo order")
        print("  0. Exit")
        choice = input("\nEnter choice: ").strip()

        if choice == "0":
            print("Goodbye! 👋")
            break

        elif choice == "1":
            order_id = input("Order ID (e.g. ORD-001): ").strip() or "ORD-001"
            order = Order(order_id)
            print("Enter SKUs to pick (blank line to finish):")
            while True:
                sku = input("  SKU: ").strip().upper()
                if not sku:
                    break
                qty_str = input("  Qty [1]: ").strip()
                qty = int(qty_str) if qty_str.isdigit() else 1
                order.add_item(sku, qty)

            if not order.lines:
                print("No items added.")
                continue

            print(f"\nExecuting {order}")
            success = robot.execute_order(order, verbose=True)
            if use_pygame:
                _show_pygame_for_order(wm, robot, order, cat)

        elif choice == "2":
            print_map(wm, robot_pos=robot.position)

        elif choice == "3":
            kw = input("Search keyword: ").strip()
            results = cat.search_by_name(kw)
            if results:
                for item in results:
                    print(f"  {item}")
            else:
                print("  No results.")

        elif choice == "4":
            print(robot.status())

        elif choice == "5":
            order = Order("DEMO-001", DEMO_ORDER)
            print(f"\nRunning demo order: {[s for s,_ in DEMO_ORDER]}")
            robot.execute_order(order, verbose=True)

            # Show path visualisation
            if use_pygame:
                _show_pygame_for_order(wm, robot, order, cat)
            else:
                _show_terminal_animation(wm, robot, order, cat)

        else:
            print("Invalid choice.")


def _show_terminal_animation(wm, robot, order, cat):
    """Replay the robot's path in the terminal for each picked SKU."""
    from config import DEPOT_POSITION
    positions = [DEPOT_POSITION]
    for sku in [s for s,_ in DEMO_ORDER]:
        item = cat.find(sku)
        if item:
            positions.append(item.location)
    positions.append(DEPOT_POSITION)

    # Build full path
    full_path = [positions[0]]
    for i in range(len(positions)-1):
        segment = find_path(wm, positions[i], positions[i+1], ALGORITHM)
        if segment:
            full_path.extend(segment[1:])

    animate_path(wm, full_path, delay=0.05, title="Robot Route Animation")


def _show_pygame_for_order(wm, robot, order, cat):
    """Animate demo path in pygame."""
    from config import DEPOT_POSITION
    positions = [DEPOT_POSITION]
    for sku in order.picked_skus():
        item = cat.find(sku)
        if item:
            positions.append(item.location)
    positions.append(DEPOT_POSITION)

    full_path = [positions[0]]
    for i in range(len(positions)-1):
        segment = find_path(wm, positions[i], positions[i+1], ALGORITHM)
        if segment:
            full_path.extend(segment[1:])

    animate_pygame(wm, full_path)


# ── Auto demo ─────────────────────────────────────────────────────────────────

def auto_demo(wm, cat, use_pygame: bool = False):
    robot = Robot("AutoBot", wm, cat)
    order = Order("AUTO-001", DEMO_ORDER)

    print("\n" + "="*55)
    print("  🤖  StyleWarehouse — Auto Demo")
    print("="*55)
    print_map(wm, title="Warehouse Layout")

    robot.execute_order(order, verbose=True)

    if use_pygame:
        _show_pygame_for_order(wm, robot, order, cat)
    else:
        _show_terminal_animation(wm, robot, order, cat)


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="StyleWarehouse Robot Navigation")
    parser.add_argument("--auto",   action="store_true", help="Run auto demo and exit")
    parser.add_argument("--pygame", action="store_true", help="Use pygame visualiser")
    args = parser.parse_args()

    wm, cat = load_system()
    robot   = Robot("StyleBot-1", wm, cat)

    if args.auto:
        auto_demo(wm, cat, use_pygame=args.pygame)
    else:
        interactive(wm, cat, robot, use_pygame=args.pygame)


if __name__ == "__main__":
    main()
