"""Katalog produktów wczytywany z pliku JSON."""

from __future__ import annotations

import json
from pathlib import Path

from shopcart.models import Product

DEFAULT_PRODUCTS_PATH = Path(__file__).resolve().parents[2] / "data" / "products.json"


class ProductNotFoundError(KeyError):
    """Brak produktu o podanym SKU."""


class Catalog:
    def __init__(self, products: list[Product]) -> None:
        self._products = {p.sku: p for p in products}

    @classmethod
    def from_json(cls, path: Path | str = DEFAULT_PRODUCTS_PATH) -> Catalog:
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        products = [
            Product(
                sku=item["sku"],
                name=item["name"],
                price=float(item["price"]),
                category=item["category"],
                vat_rate=float(item.get("vat_rate", 0.23)),
            )
            for item in raw
        ]
        return cls(products)

    def __len__(self) -> int:
        return len(self._products)

    def all(self) -> list[Product]:
        return sorted(self._products.values(), key=lambda p: p.sku)

    def get(self, sku: str) -> Product:
        try:
            return self._products[sku]
        except KeyError:
            raise ProductNotFoundError(sku) from None

    def search(self, query: str) -> list[Product]:
        q = query.lower()
        return [p for p in self.all() if q in p.name.lower()]

    def by_category(self, category: str) -> list[Product]:
        return [p for p in self.all() if p.category == category]
