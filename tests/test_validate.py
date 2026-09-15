"""Tests for exchange-rate data-quality validation."""

import pytest

from src.validate import ExchangeRateValidationError, validate_rates


@pytest.fixture
def valid_payload():
    return {
        "base": "ZAR",
        "date": "2026-09-15",
        "rates": {"USD": 0.058, "EUR": 0.049, "GBP": 0.043},
    }


def test_validate_rates_accepts_valid_payload(valid_payload):
    assert validate_rates(valid_payload) is valid_payload


def test_validate_rates_rejects_missing_required_field(valid_payload):
    del valid_payload["date"]

    with pytest.raises(ExchangeRateValidationError, match="date"):
        validate_rates(valid_payload)


def test_validate_rates_rejects_wrong_base_currency(valid_payload):
    valid_payload["base"] = "USD"

    with pytest.raises(ExchangeRateValidationError, match="Expected base"):
        validate_rates(valid_payload)


def test_validate_rates_rejects_missing_target_rate(valid_payload):
    del valid_payload["rates"]["GBP"]

    with pytest.raises(ExchangeRateValidationError, match="GBP"):
        validate_rates(valid_payload)


@pytest.mark.parametrize("invalid_rate", [0, -1, "0.058", True])
def test_validate_rates_rejects_invalid_rate_values(valid_payload, invalid_rate):
    valid_payload["rates"]["USD"] = invalid_rate

    with pytest.raises(ExchangeRateValidationError, match="USD"):
        validate_rates(valid_payload)
