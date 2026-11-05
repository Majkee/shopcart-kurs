"""Raporty sprzedaży na podstawie pliku CSV z zamówieniami.

Moduł przejęty po poprzednim zespole. Działa, ale nie ma testów.
"""

import csv
from pathlib import Path

DEFAULT_ORDERS_PATH = Path(__file__).resolve().parents[2] / "data" / "orders.csv"


def load_orders(path=DEFAULT_ORDERS_PATH):
    orders = []
    with open(path, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            row["quantity"] = int(row["quantity"])
            row["unit_price"] = float(row["unit_price"])
            orders.append(row)
    return orders


def total_revenue(orders):
    total = 0
    for o in orders:
        total = total + o["quantity"] * o["unit_price"]
    return total


def revenue_by_day(orders):
    result = {}
    for o in orders:
        d = o["date"]
        if d not in result:
            result[d] = 0
        result[d] = result[d] + o["quantity"] * o["unit_price"]
    return result


def top_products(orders, n=3):
    counts = {}
    for o in orders:
        counts[o["sku"]] = counts.get(o["sku"], 0) + o["quantity"]
    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)
    return items[:n]


def render_report(orders):
    lines = []
    lines.append("RAPORT SPRZEDAŻY")
    lines.append("================")
    lines.append(f"Liczba zamówień: {len(set(o['order_id'] for o in orders))}")
    lines.append(f"Przychód łącznie: {total_revenue(orders)}")
    lines.append("")
    lines.append("Przychód dziennie:")
    for d, v in sorted(revenue_by_day(orders).items()):
        lines.append(f"  {d}: {v}")
    lines.append("")
    lines.append("Najczęściej kupowane:")
    for sku, q in top_products(orders):
        lines.append(f"  {sku}: {q} szt.")
    return "\n".join(lines)
