"""Transform exchange-rate API payloads into analytics-ready rows."""

from __future__ import annotations

from typing import Any

from src.validate import validate_rates


def transform_rates(payload: dict[str, Any]) -> list[dict[str, str | float]]:
    """Return one clean row per target currency in the rates payload."""
    validated = validate_rates(payload)

    return [
        {
            "rate_date": validated["date"],
            "base_currency": validated["base"],
            "target_currency": currency,
            "exchange_rate": float(rate),
        }
        for currency, rate in sorted(validated["rates"].items())
    ]
