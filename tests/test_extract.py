"""Tests for the exchange-rate extraction layer."""

from unittest.mock import Mock, patch

import pytest
import requests

from src.extract import (
    API_URL,
    REQUEST_TIMEOUT_SECONDS,
    ExchangeRateExtractionError,
    extract_rates,
)


@patch("src.extract.requests.get")
def test_extract_rates_returns_api_payload(mock_get: Mock) -> None:
    payload = {
        "amount": 1.0,
        "base": "ZAR",
        "date": "2026-09-14",
        "rates": {"USD": 0.06, "EUR": 0.05},
    }
    response = Mock()
    response.json.return_value = payload
    mock_get.return_value = response

    result = extract_rates("zar", ("usd", "eur"))

    assert result == payload
    mock_get.assert_called_once_with(
        API_URL,
        params={"from": "ZAR", "to": "USD,EUR"},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status.assert_called_once()


@patch("src.extract.requests.get")
def test_extract_rates_wraps_request_errors(mock_get: Mock) -> None:
    mock_get.side_effect = requests.Timeout("request timed out")

    with pytest.raises(ExchangeRateExtractionError):
        extract_rates()


def test_extract_rates_requires_a_target_currency() -> None:
    with pytest.raises(ValueError, match="At least one target currency"):
        extract_rates(target_currencies=())


@patch("src.extract.requests.get")
def test_extract_rates_rejects_non_object_json(mock_get: Mock) -> None:
    response = Mock()
    response.json.return_value = []
    mock_get.return_value = response

    with pytest.raises(ExchangeRateExtractionError, match="unexpected response"):
        extract_rates()
