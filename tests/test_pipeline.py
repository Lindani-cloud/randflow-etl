"""Tests for the end-to-end ETL pipeline."""

import sqlite3

from src.pipeline import run_pipeline


def test_run_pipeline_connects_all_etl_stages(tmp_path):
    database = tmp_path / "pipeline.db"
    calls = []

    def fake_extractor(base_currency, target_currencies):
        calls.append((base_currency, tuple(target_currencies)))
        return {
            "amount": 1.0,
            "base": "ZAR",
            "date": "2026-09-18",
            "rates": {"USD": 0.059, "EUR": 0.050, "GBP": 0.043},
        }

    loaded = run_pipeline(
        base_currency="ZAR",
        target_currencies=("USD", "EUR", "GBP"),
        database_path=database,
        extractor=fake_extractor,
    )

    assert loaded == 3
    assert calls == [("ZAR", ("USD", "EUR", "GBP"))]

    with sqlite3.connect(database) as connection:
        rows = connection.execute(
            """SELECT target_currency, exchange_rate
               FROM exchange_rates
               ORDER BY target_currency"""
        ).fetchall()

    assert rows == [("EUR", 0.05), ("GBP", 0.043), ("USD", 0.059)]
