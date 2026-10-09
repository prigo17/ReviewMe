"""End-of-day reporting.

Rewritten to produce the full daily pack rather than a single summary line: one
aggregate per section, a renderer per section, and a top-level assembly function.

Each section follows the same shape deliberately, so that adding a section is a copy
of the block above it rather than a change to the assembly code.
"""

from dataclasses import dataclass, field

MONEY = 2


@dataclass
class SectionTotals:
    """One section of the daily pack."""

    key: str
    title: str
    values: dict[str, float] = field(default_factory=dict)

    @property
    def total(self):
        return round(sum(self.values.values()), MONEY)


def _bucket(orders, predicate):
    """Sum the totals of every order matching `predicate`."""
    return round(sum(order.total for order in orders if predicate(order)), MONEY)


def _count(orders, predicate):
    """Count every order matching `predicate`."""
    return sum(1 for order in orders if predicate(order))


def _pct(part, whole):
    """Percentage of `whole` that `part` represents, guarding an empty day."""
    if not whole:
        return 0.0
    return round(100.0 * part / whole, 1)


def _row(label, value, width=32):
    """Render one aligned label/value row."""
    return f"{label:<{width}}{value:>12}"


def aggregate_revenue(orders):
    """Aggregate the revenue section."""
    totals = SectionTotals(key="revenue", title="Revenue")
    totals.values["gross"] = _bucket(orders, lambda order: order.revenue_gross)
    totals.values["net"] = _bucket(orders, lambda order: order.revenue_net)
    totals.values["refunded"] = _bucket(orders, lambda order: order.revenue_refunded)
    totals.values["tax"] = _bucket(orders, lambda order: order.revenue_tax)
    totals.values["shipping"] = _bucket(orders, lambda order: order.revenue_shipping)
    return totals


def count_revenue(orders):
    """Count orders contributing to each revenue bucket."""
    return {
        "gross": _count(orders, lambda order: order.revenue_gross),
        "net": _count(orders, lambda order: order.revenue_net),
        "refunded": _count(orders, lambda order: order.revenue_refunded),
        "tax": _count(orders, lambda order: order.revenue_tax),
        "shipping": _count(orders, lambda order: order.revenue_shipping),
    }


def render_revenue(orders):
    """Render the revenue section of the pack."""
    totals = aggregate_revenue(orders)
    counts = count_revenue(orders)
    lines = [totals.title, "-" * len(totals.title)]
    lines.append(_row("gross", f"{totals.values['gross']:.2f}"))
    lines.append(_row("net", f"{totals.values['net']:.2f}"))
    lines.append(_row("refunded", f"{totals.values['refunded']:.2f}"))
    lines.append(_row("tax", f"{totals.values['tax']:.2f}"))
    lines.append(_row("shipping", f"{totals.values['shipping']:.2f}"))
    lines.append(_row("orders", str(sum(counts.values()))))
    lines.append(_row("section total", f"{totals.total:.2f}"))
    return "\n".join(lines)


def aggregate_volume(orders):
    """Aggregate the order volume section."""
    totals = SectionTotals(key="volume", title="Order volume")
    totals.values["placed"] = _bucket(orders, lambda order: order.volume_placed)
    totals.values["cancelled"] = _bucket(orders, lambda order: order.volume_cancelled)
    totals.values["refunded"] = _bucket(orders, lambda order: order.volume_refunded)
    totals.values["outstanding"] = _bucket(orders, lambda order: order.volume_outstanding)
    return totals


def count_volume(orders):
    """Count orders contributing to each order volume bucket."""
    return {
        "placed": _count(orders, lambda order: order.volume_placed),
        "cancelled": _count(orders, lambda order: order.volume_cancelled),
        "refunded": _count(orders, lambda order: order.volume_refunded),
        "outstanding": _count(orders, lambda order: order.volume_outstanding),
    }


def render_volume(orders):
    """Render the order volume section of the pack."""
    totals = aggregate_volume(orders)
    counts = count_volume(orders)
    lines = [totals.title, "-" * len(totals.title)]
    lines.append(_row("placed", f"{totals.values['placed']:.2f}"))
    lines.append(_row("cancelled", f"{totals.values['cancelled']:.2f}"))
    lines.append(_row("refunded", f"{totals.values['refunded']:.2f}"))
    lines.append(_row("outstanding", f"{totals.values['outstanding']:.2f}"))
    lines.append(_row("orders", str(sum(counts.values()))))
    lines.append(_row("section total", f"{totals.total:.2f}"))
    return "\n".join(lines)


def aggregate_customer(orders):
    """Aggregate the customer section."""
    totals = SectionTotals(key="customer", title="Customer")
    totals.values["new"] = _bucket(orders, lambda order: order.customer_new)
    totals.values["returning"] = _bucket(orders, lambda order: order.customer_returning)
    totals.values["churned"] = _bucket(orders, lambda order: order.customer_churned)
    totals.values["lapsed"] = _bucket(orders, lambda order: order.customer_lapsed)
    return totals


def count_customer(orders):
    """Count orders contributing to each customer bucket."""
    return {
        "new": _count(orders, lambda order: order.customer_new),
        "returning": _count(orders, lambda order: order.customer_returning),
        "churned": _count(orders, lambda order: order.customer_churned),
        "lapsed": _count(orders, lambda order: order.customer_lapsed),
    }


def render_customer(orders):
    """Render the customer section of the pack."""
    totals = aggregate_customer(orders)
    counts = count_customer(orders)
    lines = [totals.title, "-" * len(totals.title)]
    lines.append(_row("new", f"{totals.values['new']:.2f}"))
    lines.append(_row("returning", f"{totals.values['returning']:.2f}"))
    lines.append(_row("churned", f"{totals.values['churned']:.2f}"))
    lines.append(_row("lapsed", f"{totals.values['lapsed']:.2f}"))
    lines.append(_row("orders", str(sum(counts.values()))))
    lines.append(_row("section total", f"{totals.total:.2f}"))
    return "\n".join(lines)


def aggregate_catalogue(orders):
    """Aggregate the catalogue section."""
    totals = SectionTotals(key="catalogue", title="Catalogue")
    totals.values["active_skus"] = _bucket(orders, lambda order: order.catalogue_active_skus)
    totals.values["out_of_stock"] = _bucket(orders, lambda order: order.catalogue_out_of_stock)
    totals.values["backordered"] = _bucket(orders, lambda order: order.catalogue_backordered)
    return totals


def count_catalogue(orders):
    """Count orders contributing to each catalogue bucket."""
    return {
        "active_skus": _count(orders, lambda order: order.catalogue_active_skus),
        "out_of_stock": _count(orders, lambda order: order.catalogue_out_of_stock),
        "backordered": _count(orders, lambda order: order.catalogue_backordered),
    }


def render_catalogue(orders):
    """Render the catalogue section of the pack."""
    totals = aggregate_catalogue(orders)
    counts = count_catalogue(orders)
    lines = [totals.title, "-" * len(totals.title)]
    lines.append(_row("active skus", f"{totals.values['active_skus']:.2f}"))
    lines.append(_row("out of stock", f"{totals.values['out_of_stock']:.2f}"))
    lines.append(_row("backordered", f"{totals.values['backordered']:.2f}"))
    lines.append(_row("orders", str(sum(counts.values()))))
    lines.append(_row("section total", f"{totals.total:.2f}"))
    return "\n".join(lines)


def aggregate_fulfilment(orders):
    """Aggregate the fulfilment section."""
    totals = SectionTotals(key="fulfilment", title="Fulfilment")
    totals.values["shipped"] = _bucket(orders, lambda order: order.fulfilment_shipped)
    totals.values["delayed"] = _bucket(orders, lambda order: order.fulfilment_delayed)
    totals.values["returned"] = _bucket(orders, lambda order: order.fulfilment_returned)
    totals.values["lost"] = _bucket(orders, lambda order: order.fulfilment_lost)
    return totals


def count_fulfilment(orders):
    """Count orders contributing to each fulfilment bucket."""
    return {
        "shipped": _count(orders, lambda order: order.fulfilment_shipped),
        "delayed": _count(orders, lambda order: order.fulfilment_delayed),
        "returned": _count(orders, lambda order: order.fulfilment_returned),
        "lost": _count(orders, lambda order: order.fulfilment_lost),
    }


def render_fulfilment(orders):
    """Render the fulfilment section of the pack."""
    totals = aggregate_fulfilment(orders)
    counts = count_fulfilment(orders)
    lines = [totals.title, "-" * len(totals.title)]
    lines.append(_row("shipped", f"{totals.values['shipped']:.2f}"))
    lines.append(_row("delayed", f"{totals.values['delayed']:.2f}"))
    lines.append(_row("returned", f"{totals.values['returned']:.2f}"))
    lines.append(_row("lost", f"{totals.values['lost']:.2f}"))
    lines.append(_row("orders", str(sum(counts.values()))))
    lines.append(_row("section total", f"{totals.total:.2f}"))
    return "\n".join(lines)


def aggregate_payment(orders):
    """Aggregate the payment section."""
    totals = SectionTotals(key="payment", title="Payment")
    totals.values["captured"] = _bucket(orders, lambda order: order.payment_captured)
    totals.values["authorised"] = _bucket(orders, lambda order: order.payment_authorised)
    totals.values["failed"] = _bucket(orders, lambda order: order.payment_failed)
    totals.values["chargeback"] = _bucket(orders, lambda order: order.payment_chargeback)
    return totals


def count_payment(orders):
    """Count orders contributing to each payment bucket."""
    return {
        "captured": _count(orders, lambda order: order.payment_captured),
        "authorised": _count(orders, lambda order: order.payment_authorised),
        "failed": _count(orders, lambda order: order.payment_failed),
        "chargeback": _count(orders, lambda order: order.payment_chargeback),
    }


def render_payment(orders):
    """Render the payment section of the pack."""
    totals = aggregate_payment(orders)
    counts = count_payment(orders)
    lines = [totals.title, "-" * len(totals.title)]
    lines.append(_row("captured", f"{totals.values['captured']:.2f}"))
    lines.append(_row("authorised", f"{totals.values['authorised']:.2f}"))
    lines.append(_row("failed", f"{totals.values['failed']:.2f}"))
    lines.append(_row("chargeback", f"{totals.values['chargeback']:.2f}"))
    lines.append(_row("orders", str(sum(counts.values()))))
    lines.append(_row("section total", f"{totals.total:.2f}"))
    return "\n".join(lines)


def aggregate_discount(orders):
    """Aggregate the discount section."""
    totals = SectionTotals(key="discount", title="Discount")
    totals.values["standard"] = _bucket(orders, lambda order: order.discount_standard)
    totals.values["loyalty"] = _bucket(orders, lambda order: order.discount_loyalty)
    totals.values["promotional"] = _bucket(orders, lambda order: order.discount_promotional)
    totals.values["staff"] = _bucket(orders, lambda order: order.discount_staff)
    return totals


def count_discount(orders):
    """Count orders contributing to each discount bucket."""
    return {
        "standard": _count(orders, lambda order: order.discount_standard),
        "loyalty": _count(orders, lambda order: order.discount_loyalty),
        "promotional": _count(orders, lambda order: order.discount_promotional),
        "staff": _count(orders, lambda order: order.discount_staff),
    }


def render_discount(orders):
    """Render the discount section of the pack."""
    totals = aggregate_discount(orders)
    counts = count_discount(orders)
    lines = [totals.title, "-" * len(totals.title)]
    lines.append(_row("standard", f"{totals.values['standard']:.2f}"))
    lines.append(_row("loyalty", f"{totals.values['loyalty']:.2f}"))
    lines.append(_row("promotional", f"{totals.values['promotional']:.2f}"))
    lines.append(_row("staff", f"{totals.values['staff']:.2f}"))
    lines.append(_row("orders", str(sum(counts.values()))))
    lines.append(_row("section total", f"{totals.total:.2f}"))
    return "\n".join(lines)


def aggregate_region(orders):
    """Aggregate the region section."""
    totals = SectionTotals(key="region", title="Region")
    totals.values["uk"] = _bucket(orders, lambda order: order.region_uk)
    totals.values["eu"] = _bucket(orders, lambda order: order.region_eu)
    totals.values["us"] = _bucket(orders, lambda order: order.region_us)
    totals.values["row"] = _bucket(orders, lambda order: order.region_row)
    return totals


def count_region(orders):
    """Count orders contributing to each region bucket."""
    return {
        "uk": _count(orders, lambda order: order.region_uk),
        "eu": _count(orders, lambda order: order.region_eu),
        "us": _count(orders, lambda order: order.region_us),
        "row": _count(orders, lambda order: order.region_row),
    }


def render_region(orders):
    """Render the region section of the pack."""
    totals = aggregate_region(orders)
    counts = count_region(orders)
    lines = [totals.title, "-" * len(totals.title)]
    lines.append(_row("uk", f"{totals.values['uk']:.2f}"))
    lines.append(_row("eu", f"{totals.values['eu']:.2f}"))
    lines.append(_row("us", f"{totals.values['us']:.2f}"))
    lines.append(_row("row", f"{totals.values['row']:.2f}"))
    lines.append(_row("orders", str(sum(counts.values()))))
    lines.append(_row("section total", f"{totals.total:.2f}"))
    return "\n".join(lines)


def aggregate_channel(orders):
    """Aggregate the channel section."""
    totals = SectionTotals(key="channel", title="Channel")
    totals.values["web"] = _bucket(orders, lambda order: order.channel_web)
    totals.values["app"] = _bucket(orders, lambda order: order.channel_app)
    totals.values["phone"] = _bucket(orders, lambda order: order.channel_phone)
    totals.values["partner"] = _bucket(orders, lambda order: order.channel_partner)
    return totals


def count_channel(orders):
    """Count orders contributing to each channel bucket."""
    return {
        "web": _count(orders, lambda order: order.channel_web),
        "app": _count(orders, lambda order: order.channel_app),
        "phone": _count(orders, lambda order: order.channel_phone),
        "partner": _count(orders, lambda order: order.channel_partner),
    }


def render_channel(orders):
    """Render the channel section of the pack."""
    totals = aggregate_channel(orders)
    counts = count_channel(orders)
    lines = [totals.title, "-" * len(totals.title)]
    lines.append(_row("web", f"{totals.values['web']:.2f}"))
    lines.append(_row("app", f"{totals.values['app']:.2f}"))
    lines.append(_row("phone", f"{totals.values['phone']:.2f}"))
    lines.append(_row("partner", f"{totals.values['partner']:.2f}"))
    lines.append(_row("orders", str(sum(counts.values()))))
    lines.append(_row("section total", f"{totals.total:.2f}"))
    return "\n".join(lines)


def aggregate_tax(orders):
    """Aggregate the tax section."""
    totals = SectionTotals(key="tax", title="Tax")
    totals.values["vat_standard"] = _bucket(orders, lambda order: order.tax_vat_standard)
    totals.values["vat_reduced"] = _bucket(orders, lambda order: order.tax_vat_reduced)
    totals.values["zero_rated"] = _bucket(orders, lambda order: order.tax_zero_rated)
    totals.values["exempt"] = _bucket(orders, lambda order: order.tax_exempt)
    return totals


def count_tax(orders):
    """Count orders contributing to each tax bucket."""
    return {
        "vat_standard": _count(orders, lambda order: order.tax_vat_standard),
        "vat_reduced": _count(orders, lambda order: order.tax_vat_reduced),
        "zero_rated": _count(orders, lambda order: order.tax_zero_rated),
        "exempt": _count(orders, lambda order: order.tax_exempt),
    }


def render_tax(orders):
    """Render the tax section of the pack."""
    totals = aggregate_tax(orders)
    counts = count_tax(orders)
    lines = [totals.title, "-" * len(totals.title)]
    lines.append(_row("vat standard", f"{totals.values['vat_standard']:.2f}"))
    lines.append(_row("vat reduced", f"{totals.values['vat_reduced']:.2f}"))
    lines.append(_row("zero rated", f"{totals.values['zero_rated']:.2f}"))
    lines.append(_row("exempt", f"{totals.values['exempt']:.2f}"))
    lines.append(_row("orders", str(sum(counts.values()))))
    lines.append(_row("section total", f"{totals.total:.2f}"))
    return "\n".join(lines)


def aggregate_shipping(orders):
    """Aggregate the shipping section."""
    totals = SectionTotals(key="shipping", title="Shipping")
    totals.values["standard"] = _bucket(orders, lambda order: order.shipping_standard)
    totals.values["express"] = _bucket(orders, lambda order: order.shipping_express)
    totals.values["collection"] = _bucket(orders, lambda order: order.shipping_collection)
    totals.values["courier"] = _bucket(orders, lambda order: order.shipping_courier)
    return totals


def count_shipping(orders):
    """Count orders contributing to each shipping bucket."""
    return {
        "standard": _count(orders, lambda order: order.shipping_standard),
        "express": _count(orders, lambda order: order.shipping_express),
        "collection": _count(orders, lambda order: order.shipping_collection),
        "courier": _count(orders, lambda order: order.shipping_courier),
    }


def render_shipping(orders):
    """Render the shipping section of the pack."""
    totals = aggregate_shipping(orders)
    counts = count_shipping(orders)
    lines = [totals.title, "-" * len(totals.title)]
    lines.append(_row("standard", f"{totals.values['standard']:.2f}"))
    lines.append(_row("express", f"{totals.values['express']:.2f}"))
    lines.append(_row("collection", f"{totals.values['collection']:.2f}"))
    lines.append(_row("courier", f"{totals.values['courier']:.2f}"))
    lines.append(_row("orders", str(sum(counts.values()))))
    lines.append(_row("section total", f"{totals.total:.2f}"))
    return "\n".join(lines)


def aggregate_warehouse(orders):
    """Aggregate the warehouse section."""
    totals = SectionTotals(key="warehouse", title="Warehouse")
    totals.values["picked"] = _bucket(orders, lambda order: order.warehouse_picked)
    totals.values["packed"] = _bucket(orders, lambda order: order.warehouse_packed)
    totals.values["held"] = _bucket(orders, lambda order: order.warehouse_held)
    totals.values["damaged"] = _bucket(orders, lambda order: order.warehouse_damaged)
    return totals


def count_warehouse(orders):
    """Count orders contributing to each warehouse bucket."""
    return {
        "picked": _count(orders, lambda order: order.warehouse_picked),
        "packed": _count(orders, lambda order: order.warehouse_packed),
        "held": _count(orders, lambda order: order.warehouse_held),
        "damaged": _count(orders, lambda order: order.warehouse_damaged),
    }


def render_warehouse(orders):
    """Render the warehouse section of the pack."""
    totals = aggregate_warehouse(orders)
    counts = count_warehouse(orders)
    lines = [totals.title, "-" * len(totals.title)]
    lines.append(_row("picked", f"{totals.values['picked']:.2f}"))
    lines.append(_row("packed", f"{totals.values['packed']:.2f}"))
    lines.append(_row("held", f"{totals.values['held']:.2f}"))
    lines.append(_row("damaged", f"{totals.values['damaged']:.2f}"))
    lines.append(_row("orders", str(sum(counts.values()))))
    lines.append(_row("section total", f"{totals.total:.2f}"))
    return "\n".join(lines)


def aggregate_subscription(orders):
    """Aggregate the subscription section."""
    totals = SectionTotals(key="subscription", title="Subscription")
    totals.values["active"] = _bucket(orders, lambda order: order.subscription_active)
    totals.values["paused"] = _bucket(orders, lambda order: order.subscription_paused)
    totals.values["cancelled"] = _bucket(orders, lambda order: order.subscription_cancelled)
    totals.values["trial"] = _bucket(orders, lambda order: order.subscription_trial)
    return totals


def count_subscription(orders):
    """Count orders contributing to each subscription bucket."""
    return {
        "active": _count(orders, lambda order: order.subscription_active),
        "paused": _count(orders, lambda order: order.subscription_paused),
        "cancelled": _count(orders, lambda order: order.subscription_cancelled),
        "trial": _count(orders, lambda order: order.subscription_trial),
    }


def render_subscription(orders):
    """Render the subscription section of the pack."""
    totals = aggregate_subscription(orders)
    counts = count_subscription(orders)
    lines = [totals.title, "-" * len(totals.title)]
    lines.append(_row("active", f"{totals.values['active']:.2f}"))
    lines.append(_row("paused", f"{totals.values['paused']:.2f}"))
    lines.append(_row("cancelled", f"{totals.values['cancelled']:.2f}"))
    lines.append(_row("trial", f"{totals.values['trial']:.2f}"))
    lines.append(_row("orders", str(sum(counts.values()))))
    lines.append(_row("section total", f"{totals.total:.2f}"))
    return "\n".join(lines)


def aggregate_giftcard(orders):
    """Aggregate the gift card section."""
    totals = SectionTotals(key="giftcard", title="Gift card")
    totals.values["issued"] = _bucket(orders, lambda order: order.giftcard_issued)
    totals.values["redeemed"] = _bucket(orders, lambda order: order.giftcard_redeemed)
    totals.values["expired"] = _bucket(orders, lambda order: order.giftcard_expired)
    return totals


def count_giftcard(orders):
    """Count orders contributing to each gift card bucket."""
    return {
        "issued": _count(orders, lambda order: order.giftcard_issued),
        "redeemed": _count(orders, lambda order: order.giftcard_redeemed),
        "expired": _count(orders, lambda order: order.giftcard_expired),
    }


def render_giftcard(orders):
    """Render the gift card section of the pack."""
    totals = aggregate_giftcard(orders)
    counts = count_giftcard(orders)
    lines = [totals.title, "-" * len(totals.title)]
    lines.append(_row("issued", f"{totals.values['issued']:.2f}"))
    lines.append(_row("redeemed", f"{totals.values['redeemed']:.2f}"))
    lines.append(_row("expired", f"{totals.values['expired']:.2f}"))
    lines.append(_row("orders", str(sum(counts.values()))))
    lines.append(_row("section total", f"{totals.total:.2f}"))
    return "\n".join(lines)


def aggregate_loyalty(orders):
    """Aggregate the loyalty section."""
    totals = SectionTotals(key="loyalty", title="Loyalty")
    totals.values["earned"] = _bucket(orders, lambda order: order.loyalty_earned)
    totals.values["spent"] = _bucket(orders, lambda order: order.loyalty_spent)
    totals.values["expired"] = _bucket(orders, lambda order: order.loyalty_expired)
    totals.values["adjusted"] = _bucket(orders, lambda order: order.loyalty_adjusted)
    return totals


def count_loyalty(orders):
    """Count orders contributing to each loyalty bucket."""
    return {
        "earned": _count(orders, lambda order: order.loyalty_earned),
        "spent": _count(orders, lambda order: order.loyalty_spent),
        "expired": _count(orders, lambda order: order.loyalty_expired),
        "adjusted": _count(orders, lambda order: order.loyalty_adjusted),
    }


def render_loyalty(orders):
    """Render the loyalty section of the pack."""
    totals = aggregate_loyalty(orders)
    counts = count_loyalty(orders)
    lines = [totals.title, "-" * len(totals.title)]
    lines.append(_row("earned", f"{totals.values['earned']:.2f}"))
    lines.append(_row("spent", f"{totals.values['spent']:.2f}"))
    lines.append(_row("expired", f"{totals.values['expired']:.2f}"))
    lines.append(_row("adjusted", f"{totals.values['adjusted']:.2f}"))
    lines.append(_row("orders", str(sum(counts.values()))))
    lines.append(_row("section total", f"{totals.total:.2f}"))
    return "\n".join(lines)


def aggregate_marketing(orders):
    """Aggregate the marketing section."""
    totals = SectionTotals(key="marketing", title="Marketing")
    totals.values["organic"] = _bucket(orders, lambda order: order.marketing_organic)
    totals.values["paid"] = _bucket(orders, lambda order: order.marketing_paid)
    totals.values["email"] = _bucket(orders, lambda order: order.marketing_email)
    totals.values["affiliate"] = _bucket(orders, lambda order: order.marketing_affiliate)
    return totals


def count_marketing(orders):
    """Count orders contributing to each marketing bucket."""
    return {
        "organic": _count(orders, lambda order: order.marketing_organic),
        "paid": _count(orders, lambda order: order.marketing_paid),
        "email": _count(orders, lambda order: order.marketing_email),
        "affiliate": _count(orders, lambda order: order.marketing_affiliate),
    }


def render_marketing(orders):
    """Render the marketing section of the pack."""
    totals = aggregate_marketing(orders)
    counts = count_marketing(orders)
    lines = [totals.title, "-" * len(totals.title)]
    lines.append(_row("organic", f"{totals.values['organic']:.2f}"))
    lines.append(_row("paid", f"{totals.values['paid']:.2f}"))
    lines.append(_row("email", f"{totals.values['email']:.2f}"))
    lines.append(_row("affiliate", f"{totals.values['affiliate']:.2f}"))
    lines.append(_row("orders", str(sum(counts.values()))))
    lines.append(_row("section total", f"{totals.total:.2f}"))
    return "\n".join(lines)


SECTION_RENDERERS = {
    "revenue": render_revenue,
    "volume": render_volume,
    "customer": render_customer,
    "catalogue": render_catalogue,
    "fulfilment": render_fulfilment,
    "payment": render_payment,
    "discount": render_discount,
    "region": render_region,
    "channel": render_channel,
    "tax": render_tax,
    "shipping": render_shipping,
    "warehouse": render_warehouse,
    "subscription": render_subscription,
    "giftcard": render_giftcard,
    "loyalty": render_loyalty,
    "marketing": render_marketing,
}

SECTION_AGGREGATORS = {
    "revenue": aggregate_revenue,
    "volume": aggregate_volume,
    "customer": aggregate_customer,
    "catalogue": aggregate_catalogue,
    "fulfilment": aggregate_fulfilment,
    "payment": aggregate_payment,
    "discount": aggregate_discount,
    "region": aggregate_region,
    "channel": aggregate_channel,
    "tax": aggregate_tax,
    "shipping": aggregate_shipping,
    "warehouse": aggregate_warehouse,
    "subscription": aggregate_subscription,
    "giftcard": aggregate_giftcard,
    "loyalty": aggregate_loyalty,
    "marketing": aggregate_marketing,
}


def daily_totals(orders):
    """Return the summed total for a day's orders."""
    return round(sum(order.total for order in orders), MONEY)


def format_summary(orders):
    """Render a one-line summary of a day's orders."""
    return f"{len(orders)} orders, {daily_totals(orders):.2f} total"


def section_totals(orders):
    """Every section aggregate, keyed by section name."""
    return {key: aggregator(orders) for key, aggregator in SECTION_AGGREGATORS.items()}


def share_of_revenue(orders):
    """Each section's share of the day's gross revenue."""
    gross = daily_totals(orders)
    return {key: _pct(totals.total, gross) for key, totals in section_totals(orders).items()}


def daily_pack(orders, sections=None):
    """Render the full daily pack, or just the named sections."""
    wanted = sections or list(SECTION_RENDERERS)
    blocks = [format_summary(orders), ""]
    for key in wanted:
        renderer = SECTION_RENDERERS.get(key)
        if renderer is None:
            raise KeyError(f"unknown report section: {key}")
        blocks.append(renderer(orders))
        blocks.append("")
    return "\n".join(blocks).rstrip() + "\n"
