"""Kody rabatowe."""

from __future__ import annotations

DISCOUNT_CODES: dict[str, dict] = {
    "LATO10": {"type": "percent", "value": 10},
    "WITAJ20": {"type": "fixed", "value": 20},
    "DUZE15": {"type": "percent", "value": 15, "min_total": 300},
}


class InvalidDiscountCodeError(ValueError):
    """Nieznany kod rabatowy."""


class DiscountNotApplicableError(ValueError):
    """Kod istnieje, ale nie spełniono jego warunków (np. minimalnej kwoty)."""


def get_discount(code: str) -> dict:
    rule = DISCOUNT_CODES.get(code)
    if rule is None:
        raise InvalidDiscountCodeError(code)
    return rule


def apply_discount(total: float, code: str) -> float:
    """Zwraca kwotę brutto po rabacie."""
    rule = get_discount(code)
    if total < rule.get("min_total", 0):
        raise DiscountNotApplicableError(
            f"Kod {code} wymaga zamówienia za min. {rule['min_total']} zł"
        )
    if rule["type"] == "percent":
        return total * (1 - rule["value"] / 100)
    if rule["type"] == "fixed":
        return total - rule["value"]
    raise ValueError(f"Nieznany typ rabatu: {rule['type']}")
