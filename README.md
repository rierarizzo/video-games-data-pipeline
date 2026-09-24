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

## Selected Data

The transformation layer currently considers the following RAWG fields:

* `id`
* `slug`
* `name`
* `playtime`
* `platforms`
* `parent_platforms`
* `stores`
* `released`
* `tba`
* `rating` → `rawg_rating`
* `ratings`
* `ratings_count` → `rawg_ratings_count`
* `added`
* `added_by_status`
* `metacritic` → `metacritic_score`
* `updated`
* `esrb_rating`
* `genres`

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

## Project Status

Work in progress.
