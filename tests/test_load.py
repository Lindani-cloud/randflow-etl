"""Tests for the SQLite load stage."""

import sqlite3

from src.load import TABLE_NAME, load_rates


def test_load_rates_writes_transformed_records(tmp_path):
    database = tmp_path / "rates.db"
    records = [
        {
            "rate_date": "2026-09-18",
            "base_currency": "ZAR",
            "target_currency": "USD",
            "exchange_rate": 0.059,
        },
        {
            "rate_date": "2026-09-18",
            "base_currency": "ZAR",
            "target_currency": "EUR",
            "exchange_rate": 0.050,
        },
    ]

    assert load_rates(records, database) == 2

    with sqlite3.connect(database) as connection:
        rows = connection.execute(
            f"""SELECT target_currency, exchange_rate
                FROM {TABLE_NAME}
                ORDER BY target_currency"""
        ).fetchall()

    assert rows == [("EUR", 0.05), ("USD", 0.059)]


def test_load_rates_upserts_existing_rate(tmp_path):
    database = tmp_path / "rates.db"
    record = {
        "rate_date": "2026-09-18",
        "base_currency": "ZAR",
        "target_currency": "USD",
        "exchange_rate": 0.059,
    }
    load_rates([record], database)

    updated = {**record, "exchange_rate": 0.061}
    load_rates([updated], database)

    with sqlite3.connect(database) as connection:
        count, rate = connection.execute(
            f"""SELECT COUNT(*), exchange_rate
                FROM {TABLE_NAME}
                WHERE target_currency = 'USD'"""
        ).fetchone()

    assert count == 1
    assert rate == 0.061
