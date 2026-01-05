# checkout-service

A deliberately small order and checkout service, used as the review target for the automated
code review agent challenge. Every flaw in here is on purpose.

## Layout

- `app/checkout.py` — entry points that validate input before touching orders
- `app/orders.py` — order mutation, including refunds
- `app/pricing.py` — discount calculation
- `app/config.py` — runtime configuration
- `app/report.py` — end-of-day reporting
- `tests/` — pytest suite

## Development

```sh
uv sync
uv run pytest
uv run ruff check .
```
