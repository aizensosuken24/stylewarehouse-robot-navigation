"""
robot/order.py
Represents a customer pick order: a list of SKUs to collect.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class OrderLine:
    sku: str
    quantity: int
    picked: bool = False
    pick_time: Optional[datetime] = None

    def mark_picked(self) -> None:
        self.picked = True
        self.pick_time = datetime.now()


class Order:
    """
    Represents a warehouse pick order.

    An order is created with an order_id and a list of (sku, qty) tuples.
    As the robot picks each item the corresponding line is marked complete.
    """

    def __init__(self, order_id: str, items: Optional[List[tuple]] = None):
        self.order_id = order_id
        self.created_at = datetime.now()
        self.lines: Dict[str, OrderLine] = {}
        if items:
            for sku, qty in items:
                self.add_item(sku, qty)

    # ── Mutation ──────────────────────────────────────────────────────────────

    def add_item(self, sku: str, quantity: int = 1) -> None:
        if sku in self.lines:
            self.lines[sku].quantity += quantity
        else:
            self.lines[sku] = OrderLine(sku=sku, quantity=quantity)

    def mark_picked(self, sku: str) -> bool:
        """Mark a SKU as picked. Returns True if successful."""
        if sku in self.lines and not self.lines[sku].picked:
            self.lines[sku].mark_picked()
            return True
        return False

    # ── Query ─────────────────────────────────────────────────────────────────

    def is_complete(self) -> bool:
        return all(line.picked for line in self.lines.values())

    def pending_skus(self) -> List[str]:
        return [sku for sku, line in self.lines.items() if not line.picked]

    def picked_skus(self) -> List[str]:
        return [sku for sku, line in self.lines.items() if line.picked]

    def summary(self) -> str:
        total = len(self.lines)
        done  = sum(1 for l in self.lines.values() if l.picked)
        lines = [f"Order {self.order_id}  ({done}/{total} picked)"]
        for sku, line in self.lines.items():
            status = "✓" if line.picked else "○"
            lines.append(f"  {status} {sku} × {line.quantity}")
        return "\n".join(lines)

    def __len__(self) -> int:
        return len(self.lines)

    def __repr__(self) -> str:
        return f"Order({self.order_id!r}, {len(self.lines)} lines)"
