# RandFlow ETL

RandFlow is a small data engineering project that extracts daily South African
rand (ZAR) exchange rates, validates and transforms the records, and loads the
clean data into a SQLite database for analysis.

The project demonstrates a complete ETL pipeline:

1. **Extract** exchange-rate data from the Frankfurter API.
2. **Validate** the response and reject incomplete or invalid records.
3. **Transform** the data into an analysis-ready tabular format.
4. **Load** the transformed records into SQLite.
5. **Analyse** historical rates with SQL and a simple visual report.

## Planned technology

- Python 3
- Requests
- pandas
- SQLite
- Matplotlib
- pytest
- GitHub Actions

## Project structure

```text
randflow-etl/
├── .github/workflows/   # Automated tests and scheduled pipeline runs
├── data/                # Local data outputs (database files are ignored)
├── reports/             # Generated charts and summaries
├── src/                 # ETL pipeline source code
├── tests/               # Automated tests
├── .gitignore
├── README.md
└── requirements.txt
```

## Development roadmap

- [x] Create the repository structure and document the project scope.
- [ ] Extract ZAR exchange rates from the API.
- [ ] Validate and clean extracted records.
- [ ] Transform rates and calculate daily changes.
- [ ] Load the processed records into SQLite.
- [ ] Add automated tests and error handling.
- [ ] Generate an analytics report and automate the pipeline.
- [ ] Record and link the project demonstration.

## Data source

Exchange rates will be retrieved from the
[Frankfurter API](https://frankfurter.dev/), a free exchange-rate API that does
not require an API key.

## Status

The project is currently under active development.
