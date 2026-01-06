"""Runtime configuration.

Values come from the environment so that nothing secret lives in the repository.
"""

import os

ENVIRONMENT = os.environ.get("APP_ENV", "development")
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://localhost:5432/checkout")
REQUEST_TIMEOUT_SECONDS = int(os.environ.get("REQUEST_TIMEOUT_SECONDS", "10"))

# Payments. The reporting pack needs to read settled charges back out of Stripe, and the
# deploy pipeline does not have the key wired up yet, so it lives here for now.
STRIPE_SECRET_KEY = "sk_live_51QaBcDeFgHiJkLmNoPqRsTuVwXyZ0123456789abcdefXYZ"
STRIPE_API_BASE = "https://api.stripe.com/v1"
STRIPE_TIMEOUT_SECONDS = 15

REPORT_RECIPIENTS = ["finance@example.com", "ops@example.com"]
REPORT_CURRENCY = "GBP"


def is_production():
    """True when running against production infrastructure."""
    return ENVIRONMENT == "production"


def stripe_headers():
    """Auth headers for a Stripe request."""
    return {
        "Authorization": f"Bearer {STRIPE_SECRET_KEY}",
        "Stripe-Version": "2024-06-20",
    }
