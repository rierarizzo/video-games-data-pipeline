# Video Games Data Pipeline

Data engineering project built using data from the [RAWG Video Games Database API](https://rawg.io/apidocs).

The goal of this project is to build an end-to-end data pipeline that extracts video game data from RAWG, stores the raw data in PostgreSQL, and transforms it into structured datasets ready for analysis.

## Objectives

* Extract game data from the RAWG API.
* Store raw API responses in PostgreSQL.
* Implement incremental data loading.
* Transform raw data into clean and structured tables.
* Build a reproducible ETL/ELT pipeline following data engineering practices.

## Analytical Questions

The transformed data model is being designed to answer questions such as:

* Which genre has the highest average playtime?
* Which platform has the largest number of available games?
* Which genre has the highest average RAWG rating?

Additional analytical questions will be added as the data model evolves.

## Selected Fields

RAWG fields used by the pipeline and where each one lands.

| RAWG field | Target |
| --- | --- |
| `id`, `slug`, `name` | `stg_games` |
| `playtime`, `released`, `tba` | `stg_games` |
| `rating`, `ratings_count`, `metacritic` | `stg_games` |
| `added` | `stg_games.added_to_library` |
| `updated` | `stg_games.updated_at` |
| `genres`, `platforms`, `parent_platforms`, `stores`, `ratings`, `added_by_status` | staging tables (pending) |

## Data Model

Raw payloads are stored untouched in JSONB. Staging is derived from them: a
flattened view for the scalar fields and one table per nested collection.

| Layer | Object | Source | Shape | Status |
| --- | --- | --- | --- | --- |
| Control | `etl_state` | pipeline | table | done |
| Raw | `raw_games` | `/games` | JSONB | done |
| Raw | `raw_genres` | `/genres` | JSONB | done |
| Raw | `raw_platforms` | `/platforms` | JSONB | done |
| Raw | `raw_parent_platforms` | `/platforms/lists/parents` | JSONB | done |
| Raw | `raw_stores` | `/stores` | JSONB | done |
| Staging | `stg_games` | `raw_games` | view | done |
| Staging | bridge tables for the nested collections above | `raw_games` | tables | pending |

## Tech Stack

* Python
* PostgreSQL
* SQLAlchemy
* Docker
* RAWG API

## Running the Project

Install dependencies:

```bash
uv sync
```

Start the PostgreSQL services:

```bash
docker compose up -d
```

Run the pipeline:

```bash
uv run rawg-pipeline
```

## Development

Lint and auto-fix:

```bash
uv run ruff check . --fix
```

Format:

```bash
uv run ruff format .
```

## Design Decisions

Non-obvious choices — JSONB raw layer vs typed columns, watermark table vs `MAX(updated)`, views vs tables — are documented with their trade-offs in [docs/decisions.md](docs/decisions.md).

## Project Status

Work in progress.
