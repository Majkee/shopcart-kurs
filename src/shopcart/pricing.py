"""Obliczenia cenowe: VAT i formatowanie kwot."""

from __future__ import annotations


def gross(net: float, vat_rate: float) -> float:
    """Zwraca kwotę brutto zaokrągloną do groszy."""
    return round(net * (1 + vat_rate), 2)


def format_pln(amount: float) -> str:
    """Formatuje kwotę po polsku, np. 1234.5 -> '1234,50 zł'."""
    return f"{amount:.2f} zł".replace(".", ",")
