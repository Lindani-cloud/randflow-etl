"""Load transformed exchange-rate records into a SQLite warehouse."""

from __future__ import annotations

import sqlite3
from collections.abc import Iterable, Mapping
from pathlib import Path

TABLE_NAME = "exchange_rates"

CREATE_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    rate_date TEXT NOT NULL,
    base_currency TEXT NOT NULL,
    target_currency TEXT NOT NULL,
    exchange_rate REAL NOT NULL CHECK (exchange_rate > 0),
    loaded_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (rate_date, base_currency, target_currency)
)
"""


def load_rates(
    records: Iterable[Mapping[str, str | float]],
    database_path: str | Path = "data/randflow.db",
) -> int:
    """Upsert transformed rate records and return the number processed."""
    rows = [
        (
            str(record["rate_date"]),
            str(record["base_currency"]),
            str(record["target_currency"]),
            float(record["exchange_rate"]),
        )
        for record in records
    ]

    path = Path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(path) as connection:
        connection.execute(CREATE_TABLE_SQL)
        connection.executemany(
            f"""
            INSERT INTO {TABLE_NAME}
                (rate_date, base_currency, target_currency, exchange_rate)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(rate_date, base_currency, target_currency)
            DO UPDATE SET exchange_rate = excluded.exchange_rate,
                          loaded_at = CURRENT_TIMESTAMP
            """,
            rows,
        )

    return len(rows)
