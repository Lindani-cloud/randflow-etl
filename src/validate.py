"""Validate extracted exchange-rate data before transformation."""

from collections.abc import Sequence
from datetime import date
from typing import Any

DEFAULT_REQUIRED_CURRENCIES = ("USD", "EUR", "GBP")
REQUIRED_FIELDS = {"base", "date", "rates"}


class ExchangeRateValidationError(ValueError):
    """Raised when extracted exchange-rate data fails a quality check."""


def validate_rates(
    payload: dict[str, Any],
    expected_base: str = "ZAR",
    required_currencies: Sequence[str] = DEFAULT_REQUIRED_CURRENCIES,
) -> dict[str, Any]:
    """Validate the shape and values of an exchange-rate API payload.

    The original payload is returned unchanged when all checks pass, allowing
    this function to be inserted cleanly between extraction and transformation.
    """
    if not isinstance(payload, dict):
        raise ExchangeRateValidationError("Payload must be a dictionary.")

    missing_fields = REQUIRED_FIELDS.difference(payload)
    if missing_fields:
        missing = ", ".join(sorted(missing_fields))
        raise ExchangeRateValidationError(f"Missing required fields: {missing}.")

    if payload["base"] != expected_base.upper():
        raise ExchangeRateValidationError(
            f"Expected base currency {expected_base.upper()}, "
            f"received {payload['base']}."
        )

    try:
        date.fromisoformat(payload["date"])
    except (TypeError, ValueError) as exc:
        raise ExchangeRateValidationError(
            "The date must use ISO format YYYY-MM-DD."
        ) from exc

    rates = payload["rates"]
    if not isinstance(rates, dict):
        raise ExchangeRateValidationError("Rates must be a dictionary.")

    targets = tuple(currency.upper() for currency in required_currencies)
    missing_rates = [currency for currency in targets if currency not in rates]
    if missing_rates:
        raise ExchangeRateValidationError(
            f"Missing required rates: {', '.join(missing_rates)}."
        )

    for currency in targets:
        value = rates[currency]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ExchangeRateValidationError(
                f"Rate for {currency} must be numeric."
            )
        if value <= 0:
            raise ExchangeRateValidationError(
                f"Rate for {currency} must be greater than zero."
            )

    return payload
