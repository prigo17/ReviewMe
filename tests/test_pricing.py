"""Tests for discount calculation."""

from dataclasses import dataclass

from app.pricing import BULK_THRESHOLD, LOYALTY_RATE, STANDARD_RATE, calculate_discount


@dataclass
class Customer:
    id: str = "cust-1"
    is_active: bool = True


@dataclass
class Basket:
    item_count: int = 1
    total: float = 100.0


def test_inactive_customer_gets_nothing():
    assert calculate_discount(Customer(is_active=False), Basket()) == 0.0


def test_small_order_gets_standard_rate():
    assert calculate_discount(Customer(), Basket(item_count=1)) == STANDARD_RATE


def test_bulk_order_gets_loyalty_rate():
    assert calculate_discount(Customer(), Basket(item_count=BULK_THRESHOLD)) == LOYALTY_RATE
