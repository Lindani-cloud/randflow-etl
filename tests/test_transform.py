import pytest

from src.transform import transform_rates


VALID_PAYLOAD = {
    "base": "ZAR",
    "date": "2026-09-16",
    "rates": {
        "USD": 0.056,
        "EUR": 0.048,
        "GBP": 0.042,
    },
}


def test_transform_rates_returns_one_row_per_currency():
    rows = transform_rates(VALID_PAYLOAD)

    assert rows == [
        {
            "rate_date": "2026-09-16",
            "base_currency": "ZAR",
            "target_currency": "EUR",
            "exchange_rate": 0.048,
        },
        {
            "rate_date": "2026-09-16",
            "base_currency": "ZAR",
            "target_currency": "GBP",
            "exchange_rate": 0.042,
        },
        {
            "rate_date": "2026-09-16",
            "base_currency": "ZAR",
            "target_currency": "USD",
            "exchange_rate": 0.056,
        },
    ]


def test_transform_rates_keeps_extra_supported_targets():
    payload = {
        **VALID_PAYLOAD,
        "rates": {
            **VALID_PAYLOAD["rates"],
            "CAD": 0.076,
        },
    }

    rows = transform_rates(payload)

    assert rows[0]["target_currency"] == "CAD"
    assert rows[0]["exchange_rate"] == 0.076


def test_transform_rates_reuses_validation_rules():
    payload = {
        **VALID_PAYLOAD,
        "rates": {
            "USD": 0.056,
            "EUR": 0.048,
        },
    }

    with pytest.raises(ValueError, match="Missing required rates: GBP"):
        transform_rates(payload)
