"""Interfejs wiersza poleceń: python -m shopcart <komenda>."""

from __future__ import annotations

import argparse
import sys

from shopcart.cart import Cart
from shopcart.catalog import Catalog, ProductNotFoundError
from shopcart.discounts import DiscountNotApplicableError, InvalidDiscountCodeError
from shopcart.pricing import format_pln
from shopcart.reports import load_orders, render_report


def _cmd_catalog(args: argparse.Namespace) -> int:
    catalog = Catalog.from_json()
    products = catalog.by_category(args.category) if args.category else catalog.all()
    for p in products:
        print(f"{p.sku:<8} {p.name:<32} {format_pln(p.price):>12}  [{p.category}]")
    return 0


def _cmd_search(args: argparse.Namespace) -> int:
    for p in Catalog.from_json().search(args.query):
        print(f"{p.sku:<8} {p.name}")
    return 0


def _cmd_cart(args: argparse.Namespace) -> int:
    cart = Cart(Catalog.from_json())
    try:
        for item in args.add:
            sku, _, qty = item.partition(":")
            cart.add(sku, int(qty or 1))
        if args.code:
            cart.apply_code(args.code)
        total = cart.total()
    except (ProductNotFoundError, InvalidDiscountCodeError, DiscountNotApplicableError) as exc:
        print(f"Błąd: {exc}", file=sys.stderr)
        return 1
    for line in cart.lines:
        print(f"{line.quantity} x {line.product.name}")
    print(f"Netto:  {format_pln(cart.subtotal_net())}")
    print(f"Brutto: {format_pln(cart.subtotal_gross())}")
    print(f"Do zapłaty: {format_pln(total)}")
    return 0


def _cmd_report(args: argparse.Namespace) -> int:
    orders = load_orders(args.orders) if args.orders else load_orders()
    print(render_report(orders))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="shopcart", description="Mały sklep do ćwiczeń")
    sub = parser.add_subparsers(dest="command", required=True)

    p_catalog = sub.add_parser("catalog", help="Lista produktów")
    p_catalog.add_argument("--category", help="Filtruj po kategorii")
    p_catalog.set_defaults(func=_cmd_catalog)

    p_search = sub.add_parser("search", help="Szukaj produktu po nazwie")
    p_search.add_argument("query")
    p_search.set_defaults(func=_cmd_search)

    p_cart = sub.add_parser("cart", help="Policz koszyk, np. --add KUB-001:2 --code LATO10")
    p_cart.add_argument("--add", action="append", default=[], metavar="SKU[:ILOŚĆ]")
    p_cart.add_argument("--code", help="Kod rabatowy")
    p_cart.set_defaults(func=_cmd_cart)

    p_report = sub.add_parser("report", help="Raport sprzedaży z data/orders.csv")
    p_report.add_argument("--orders", help="Ścieżka do pliku CSV z zamówieniami")
    p_report.set_defaults(func=_cmd_report)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)
