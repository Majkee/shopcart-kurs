import pytest

from shopcart.catalog import ProductNotFoundError


def test_loads_all_products(catalog):
    assert len(catalog) == 10


def test_get_returns_product(catalog):
    product = catalog.get("KUB-001")
    assert product.name == "Kubek ceramiczny Kraków"
    assert product.price == 29.99


def test_get_unknown_sku_raises(catalog):
    with pytest.raises(ProductNotFoundError):
        catalog.get("NIE-MA")


def test_search_is_case_insensitive(catalog):
    skus = [p.sku for p in catalog.search("KUBEK")]
    assert skus == ["KUB-001", "KUB-002"]


def test_books_have_reduced_vat(catalog):
    assert all(p.vat_rate == 0.05 for p in catalog.by_category("książki"))
