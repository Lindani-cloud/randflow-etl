"""Extract exchange-rate data from the Frankfurter API."""

from collections.abc import Sequence
from typing import Any

import requests

API_URL = "https://api.frankfurter.dev/v1/latest"
DEFAULT_CURRENCIES = ("USD", "EUR", "GBP")
REQUEST_TIMEOUT_SECONDS = 15


class ExchangeRateExtractionError(RuntimeError):
    """Raised when exchange-rate data cannot be extracted."""


def extract_rates(
    base_currency: str = "ZAR",
    target_currencies: Sequence[str] = DEFAULT_CURRENCIES,
) -> dict[str, Any]:
    """Fetch the latest exchange rates for one base currency."""
    if not target_currencies:
        raise ValueError("At least one target currency is required.")

    params = {
        "from": base_currency.upper(),
        "to": ",".join(currency.upper() for currency in target_currencies),
    }

    try:
        response = requests.get(
            API_URL,
            params=params,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        payload = response.json()
    except (requests.RequestException, ValueError) as exc:
        raise ExchangeRateExtractionError(
            "Unable to extract exchange-rate data."
        ) from exc

    if not isinstance(payload, dict):
        raise ExchangeRateExtractionError("The API returned an unexpected response.")

    return payload


if __name__ == "__main__":
    print(extract_rates())
