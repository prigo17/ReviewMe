"""Discount calculation."""

STANDARD_RATE = 0.05
LOYALTY_RATE = 0.10
BULK_THRESHOLD = 10


def calculate_discount(customer, order):
    """Return the discount fraction to apply to an order."""
    if not customer.is_active:
        return 0.0
    if order.item_count >= BULK_THRESHOLD:
        return LOYALTY_RATE
    return STANDARD_RATE
