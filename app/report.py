"""End-of-day reporting.

Currently a stub: the reporting rewrite lands in a later change.
"""


def daily_totals(orders):
    """Return the summed total for a day's orders."""
    return round(sum(order.total for order in orders), 2)


def format_summary(orders):
    """Render a one-line summary of a day's orders."""
    return f"{len(orders)} orders, {daily_totals(orders):.2f} total"
