"""Item catalogue primitives."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class Item:
    sku: str
    name: str
    category: str
    brand: str
    size: str
    colour: str
    grid_row: int
    grid_col: int
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
    """Stores all warehouse items and supports SKU and search lookups."""

    def __init__(self):
        self._items: Dict[str, Item] = {}

    def add_item(self, item: Item) -> None:
        self._items[item.sku] = item

    def remove_item(self, sku: str) -> None:
        self._items.pop(sku, None)

    def update_quantity(self, sku: str, delta: int) -> None:
        if sku in self._items:
            self._items[sku].quantity = max(0, self._items[sku].quantity + delta)

    def find(self, sku: str) -> Optional[Item]:
        return self._items.get(sku)

    def search_by_name(self, keyword: str) -> List[Item]:
        lowered = keyword.lower()
        return [item for item in self._items.values() if lowered in item.name.lower()]

    def items_at(self, row: int, col: int) -> List[Item]:
        return [item for item in self._items.values() if item.grid_row == row and item.grid_col == col]

    def all_items(self) -> List[Item]:
        return list(self._items.values())

    def __len__(self) -> int:
        return len(self._items)

    def load_from_csv(self, filepath: str) -> "ItemCatalogue":
        with open(filepath, newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
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
        fieldnames = [
            "sku",
            "name",
            "category",
            "brand",
            "size",
            "colour",
            "grid_row",
            "grid_col",
            "quantity",
        ]
        with open(filepath, "w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            for item in self._items.values():
                writer.writerow(
                    {
                        "sku": item.sku,
                        "name": item.name,
                        "category": item.category,
                        "brand": item.brand,
                        "size": item.size,
                        "colour": item.colour,
                        "grid_row": item.grid_row,
                        "grid_col": item.grid_col,
                        "quantity": item.quantity,
                    }
                )

    def __repr__(self) -> str:
        return f"ItemCatalogue({len(self._items)} items)"
