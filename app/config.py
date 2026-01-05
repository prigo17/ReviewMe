"""Runtime configuration.

Values come from the environment so that nothing secret lives in the repository.
"""

import os

ENVIRONMENT = os.environ.get("APP_ENV", "development")
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://localhost:5432/checkout")
REQUEST_TIMEOUT_SECONDS = int(os.environ.get("REQUEST_TIMEOUT_SECONDS", "10"))


def is_production():
    """True when running against production infrastructure."""
    return ENVIRONMENT == "production"
