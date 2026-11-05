import pytest

from shopcart.catalog import Catalog


@pytest.fixture
def catalog() -> Catalog:
    return Catalog.from_json()
