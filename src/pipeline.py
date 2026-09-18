"""Run the complete extract, transform, and load workflow."""

from __future__ import annotations

import argparse
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

from src.extract import DEFAULT_CURRENCIES, extract_rates
from src.load import load_rates
from src.transform import transform_rates


def run_pipeline(
    base_currency: str = "ZAR",
    target_currencies: Sequence[str] = DEFAULT_CURRENCIES,
    database_path: str | Path = "data/randflow.db",
    extractor: Callable[..., dict[str, Any]] = extract_rates,
) -> int:
    """Execute the ETL stages and return the number of loaded rates."""
    payload = extractor(
        base_currency=base_currency,
        target_currencies=target_currencies,
    )
    records = transform_rates(payload)
    return load_rates(records, database_path)


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line interface."""
    parser = argparse.ArgumentParser(
        description="Load current currency exchange rates into SQLite."
    )
    parser.add_argument("--base", default="ZAR", help="Base currency code.")
    parser.add_argument(
        "--targets",
        default=",".join(DEFAULT_CURRENCIES),
        help="Comma-separated target currency codes.",
    )
    parser.add_argument(
        "--database",
        default="data/randflow.db",
        help="Path to the SQLite database.",
    )
    return parser


def main() -> None:
    """Run the pipeline from command-line arguments."""
    args = build_parser().parse_args()
    targets = tuple(
        currency.strip().upper()
        for currency in args.targets.split(",")
        if currency.strip()
    )
    loaded = run_pipeline(
        base_currency=args.base.upper(),
        target_currencies=targets,
        database_path=args.database,
    )
    print(f"Loaded {loaded} exchange rates into {args.database}")


if __name__ == "__main__":
    main()
