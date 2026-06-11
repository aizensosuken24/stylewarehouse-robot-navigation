"""
warehouse/catalogue.py
Manages the item catalogue: maps SKU → (aisle, shelf, bin) coordinates on the grid.
"""
from __future__ import annotations
import csv
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class Item:
    sku: str
    name: str
    category: str          # e.g. "Tops", "Trousers", "Footwear"
    brand: str
    size: str
    colour: str
    grid_row: int          # row on the WarehouseMap
    grid_col: int          # col on the WarehouseMap
    quantity: int = 0

    @property
    def location(self) -> Tuple[int, int]:
        return (self.grid_row, self.grid_col)

    def __str__(self) -> str:
        return (
            f"[{self.sku}] {self.brand} {self.name} "
            f"({self.colour}, {self.size}) @ ({self.grid_row},{self.grid_col})"
        )


class ItemCatalogue:
    """Stores all warehouse items and provides lookup by SKU or location."""

    def __init__(self):
        self._items: Dict[str, Item] = {}

    # ── Mutation ──────────────────────────────────────────────────────────────

    def add_item(self, item: Item) -> None:
        self._items[item.sku] = item

    def remove_item(self, sku: str) -> None:
        self._items.pop(sku, None)

    def update_quantity(self, sku: str, delta: int) -> None:
        if sku in self._items:
            self._items[sku].quantity = max(0, self._items[sku].quantity + delta)

    # ── Query ─────────────────────────────────────────────────────────────────

    def find(self, sku: str) -> Optional[Item]:
        return self._items.get(sku)

    def search_by_name(self, keyword: str) -> List[Item]:
        kw = keyword.lower()
        return [i for i in self._items.values() if kw in i.name.lower()]

    def items_at(self, row: int, col: int) -> List[Item]:
        return [i for i in self._items.values() if i.grid_row == row and i.grid_col == col]

    def all_items(self) -> List[Item]:
        return list(self._items.values())

    def __len__(self) -> int:
        return len(self._items)

    # ── I/O ───────────────────────────────────────────────────────────────────

    def load_from_csv(self, filepath: str) -> "ItemCatalogue":
        """
        Expected CSV columns:
        sku, name, category, brand, size, colour, grid_row, grid_col, quantity
        """
        with open(filepath, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                item = Item(
                    sku=row["sku"],
                    name=row["name"],
                    category=row["category"],
                    brand=row["brand"],
                    size=row["size"],
                    colour=row["colour"],
                    grid_row=int(row["grid_row"]),
                    grid_col=int(row["grid_col"]),
                    quantity=int(row.get("quantity", 0)),
                )
                self.add_item(item)
        return self

    def save_to_csv(self, filepath: str) -> None:
        fieldnames = ["sku", "name", "category", "brand", "size", "colour",
                      "grid_row", "grid_col", "quantity"]
        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for item in self._items.values():
                writer.writerow({
                    "sku": item.sku, "name": item.name,
                    "category": item.category, "brand": item.brand,
                    "size": item.size, "colour": item.colour,
                    "grid_row": item.grid_row, "grid_col": item.grid_col,
                    "quantity": item.quantity,
                })

    def __repr__(self) -> str:
        return f"ItemCatalogue({len(self._items)} items)"
