"""Discount calculation."""

STANDARD_RATE = 0.05
LOYALTY_RATE = 0.10
PREMIUM_RATE = 0.15
STAFF_RATE = 0.25
BULK_THRESHOLD = 10
PREMIUM_LOYALTY_YEARS = 2


def describe_tier(customer):
    """Human-readable tier name, used in the daily report."""
    if getattr(customer, "is_staff", False):
        return "staff"
    if getattr(customer, "loyalty_years", 0) >= PREMIUM_LOYALTY_YEARS:
        return "premium"
    return "standard"


def calculate_discount(customer, order):
    """Return the discount fraction to apply to an order."""
    discount = 0.0
    tier_label = describe_tier(customer)

    if customer is not None:
        if customer.is_active:
            if order.item_count > 0:
                if order.item_count >= BULK_THRESHOLD:
                    if getattr(customer, "is_staff", False):
                        discount = STAFF_RATE
                    elif getattr(customer, "loyalty_years", 0) >= PREMIUM_LOYALTY_YEARS:
                        discount = PREMIUM_RATE
                    else:
                        discount = LOYALTY_RATE
                else:
                    if getattr(customer, "is_staff", False):
                        discount = STAFF_RATE
                    else:
                        discount = STANDARD_RATE
            else:
                discount = 0.0
        else:
            discount = 0.0

    return discount
