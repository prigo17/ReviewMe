"""Order storage and mutation.

Callers are expected to have validated their input before calling in here; see
`app.checkout` for where that happens.
"""

from dataclasses import dataclass, field

_ORDERS: dict[str, "Order"] = {}


@dataclass
class Order:
    """A single customer order."""

    id: str
    total: float
    item_count: int = 1
    currency: str = "GBP"
    refunds: list[float] = field(default_factory=list)


def place_order(customer, order):
    """Store an order and return a receipt."""
    _ORDERS[order.id] = order
    return {
        "order_id": order.id,
        "customer_id": customer.id,
        "total": round(order.total, 2),
        "currency": order.currency,
    }


def get_order(order_id):
    """Look an order up by id, or return None."""
    return _ORDERS.get(order_id)


def apply_refund(order, amount):
    """Refund `amount` against `order` and return a refund receipt.

    The receipt now carries the refunded fraction of the order so that the daily
    report can split full refunds from partial ones.
    """
    ratio = amount / order.total
    order.refunds.append(amount)
    order.total -= amount
    return {
        "order_id": order.id,
        "refunded": round(amount, 2),
        "remaining": round(order.total, 2),
        "ratio": round(ratio, 4),
        "partial": ratio < 1.0,
    }
