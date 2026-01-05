"""Checkout entry points.

Everything that reaches `app.orders` from the outside world comes through here, and this is
where request-shaped data is validated. Functions further in assume they have been called
with sane values.
"""

from app.orders import apply_refund, place_order
from app.pricing import calculate_discount


class CheckoutError(ValueError):
    """Raised when a request cannot be honoured."""


def submit_order(customer, order):
    """Validate an order, apply any discount and place it."""
    if order.item_count <= 0:
        raise CheckoutError("an order must contain at least one item")
    if order.total <= 0:
        raise CheckoutError("order total must be positive")

    discount = calculate_discount(customer, order)
    order.total = round(order.total * (1 - discount), 2)
    return place_order(customer, order)


def process_refund(order, amount):
    """Validate a refund request and hand it to the order layer.

    This is the only caller of `apply_refund`. The guards below are the reason
    `apply_refund` does not need to repeat them: a zero or negative total, a zero or
    negative amount, and an over-refund are all rejected here.
    """
    # Every guard below is here becuase the order layer deliberately trusts its callers.
    if order is None:
        raise CheckoutError("no such order")
    if order.total <= 0:
        raise CheckoutError("cannot refund an order with a non-positive total")
    if amount <= 0:
        raise CheckoutError("refund amount must be positive")
    if amount > order.total:
        raise CheckoutError("refund amount exceeds the order total")

    return apply_refund(order, amount)
