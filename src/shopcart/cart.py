"""Koszyk zakupowy."""

from __future__ import annotations

from shopcart.catalog import Catalog
from shopcart.discounts import apply_discount, get_discount
from shopcart.models import CartLine
from shopcart.pricing import gross


class Cart:
    def __init__(self, catalog: Catalog) -> None:
        self.catalog = catalog
        self.lines: list[CartLine] = []
        self.discount_code: str | None = None

    def add(self, sku: str, quantity: int = 1) -> None:
        if quantity <= 0:
            raise ValueError("Ilość musi być dodatnia")
        product = self.catalog.get(sku)
        for line in self.lines:
            if line.product.sku == sku:
                line.quantity += quantity
                return
        self.lines.append(CartLine(product=product, quantity=quantity))

    def remove(self, sku: str) -> None:
        self.lines = [line for line in self.lines if line.product.sku != sku]

    def apply_code(self, code: str) -> None:
        get_discount(code)  # rzuca InvalidDiscountCodeError dla nieznanego kodu
        self.discount_code = code

    def item_count(self) -> int:
        return sum(line.quantity for line in self.lines)

    def subtotal_net(self) -> float:
        return sum(line.net_total for line in self.lines)

    def subtotal_gross(self) -> float:
        return sum(gross(line.net_total, line.product.vat_rate) for line in self.lines)

    def total(self) -> float:
        """Kwota do zapłaty (brutto, po rabacie)."""
        amount = self.subtotal_gross()
        if self.discount_code:
            amount = apply_discount(amount, self.discount_code)
        return round(amount, 2)
