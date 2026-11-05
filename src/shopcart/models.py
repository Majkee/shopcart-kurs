"""Modele danych sklepu."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    """Produkt z katalogu. Cena jest ceną NETTO w PLN."""

    sku: str
    name: str
    price: float
    category: str
    vat_rate: float = 0.23


@dataclass
class CartLine:
    """Jedna pozycja w koszyku."""

    product: Product
    quantity: int

    @property
    def net_total(self) -> float:
        return self.product.price * self.quantity
