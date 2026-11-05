import pytest

from shopcart.discounts import DiscountNotApplicableError, apply_discount


def test_percent_discount():
    assert apply_discount(200.0, "LATO10") == pytest.approx(180.0)


def test_fixed_discount():
    assert apply_discount(100.0, "WITAJ20") == pytest.approx(80.0)


def test_min_total_not_met():
    with pytest.raises(DiscountNotApplicableError):
        apply_discount(100.0, "DUZE15")


def test_min_total_met():
    assert apply_discount(400.0, "DUZE15") == pytest.approx(340.0)
