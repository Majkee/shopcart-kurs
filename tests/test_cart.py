import pytest

from shopcart.cart import Cart
from shopcart.discounts import InvalidDiscountCodeError


def test_empty_cart_total_is_zero(catalog):
    assert Cart(catalog).total() == 0


def test_adding_same_sku_merges_lines(catalog):
    cart = Cart(catalog)
    cart.add("KUB-001")
    cart.add("KUB-001", 2)
    assert len(cart.lines) == 1
    assert cart.item_count() == 3


def test_add_rejects_non_positive_quantity(catalog):
    with pytest.raises(ValueError):
        Cart(catalog).add("KUB-001", 0)


def test_remove(catalog):
    cart = Cart(catalog)
    cart.add("KUB-001")
    cart.add("TSH-001")
    cart.remove("KUB-001")
    assert [line.product.sku for line in cart.lines] == ["TSH-001"]


def test_total_includes_vat(catalog):
    cart = Cart(catalog)
    cart.add("TSH-001", 2)  # 2 x 49.99 netto
    assert cart.total() == 122.98


def test_total_with_percent_code(catalog):
    cart = Cart(catalog)
    cart.add("BLU-001")  # 159.00 netto -> 195.57 brutto
    cart.apply_code("LATO10")
    assert cart.total() == 176.01


def test_unknown_code_is_rejected(catalog):
    with pytest.raises(InvalidDiscountCodeError):
        Cart(catalog).apply_code("NIEISTNIEJE")
