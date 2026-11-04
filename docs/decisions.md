# Design Decisions

Each entry explains *why* the code looks the way it does, and what it costs.
Commit hashes are references.

## 1. Raw payload stored as JSONB, not typed columns

`raw_*` tables keep the untouched API object in a `data JSONB` column
(`ad5ad72`). The typed shape lives on top, in `stg_*` objects.

**Why:** RAWG adds and changes fields without notice. With JSONB a new field
needs no migration, and the transformation can be rewritten and re-run from
stored data — no second extraction. Re-extracting is the expensive, rate-limited
part; re-transforming is free.

**Cost:** no type safety or constraints on the payload, and every read pays a
parse. That is acceptable because only the staging layer reads it.

## 2. Schema lives in `sql/`, applied in filename order

DDL moved out of Python into `sql/NNN_*.sql` (`6b09410`), and the runner now
globs the directory and sorts (`de2c9b4`) instead of listing each file.

**Why:** schema changes are reviewable as plain SQL, and adding a script does not
require editing Python. The zero-padded prefix encodes dependency order: a view
must have a higher number than the table it reads.

**Cost:** each file must hold exactly one statement (the driver executes a single
statement per file), and the runner depends on its working directory.

## 3. Idempotent upserts instead of an existence check

`get_existing_game_ids()` loaded every stored id into a Python set, then filtered
in memory. It was removed in favour of `INSERT ... ON CONFLICT (id) DO UPDATE`
(`c0a59e4`), later refined with `WHERE data IS DISTINCT FROM EXCLUDED.data`.

**Why:** the Python check grew linearly with the table, and it only inserted —
it could never update a game whose RAWG data changed. The upsert moves the work
to the database and makes a re-run safe. The `WHERE` clause stops unchanged rows
from being rewritten, which keeps `extracted_at`/storage churn down.

**Cost:** the write path now depends on the primary key being the natural RAWG
`id`, and correctness relies on PostgreSQL conflict resolution.

## 4. Day-level watermark in `etl_state`

`get_latest_game_updated()` derived the cursor from `MAX(data->>'updated')` on
`raw_games`. It was replaced by an explicit watermark table and a day-based loop
(`3002826`).

**Why:** `MAX` conflates "have I seen this data" with "have I finished this
range". If a run dies halfway through a day, `MAX` already points at the newest
row, so the rest of that day is silently skipped. A watermark written only after
a day completes — and only on success, in the same commit semantics — cannot lie.
It also decouples the ingestion state from the payload, so transforming or
deleting rows never moves the cursor.

**Cost:** state is now duplicated (rows + watermark) and needs a bootstrap
constant (`min_updated_date`) for the first run.

## 5. Ordered by `updated` and sliced one day at a time

Fetching adds `ordering=updated` (`2dc5320`) and requests
`updated=<day>,<day>` (`3002826`).

**Why:** an incremental cursor is only meaningful over a stable sort order;
RAWG's default ordering could reorder results between pages and produce gaps or
duplicates. Slicing per day bounds the number of pages the API has to serve for
any single request, which is exactly what broke the previous approach.

## 6. A deep-pagination workaround was built, then deleted

RAWG returns 404 past page ~251. `383ef48` special-cased it by restarting from
the last seen `updated` value. `3002826` removed the workaround entirely.

**Why it was deleted, not kept:** the workaround encoded a moving target into
the control flow and only papered over the real problem — deep pagination over
an unbounded, ever-shifting collection. Day-based slicing never asks for page
250, so the bug cannot occur. The decision was to change the access pattern, not
to survive the bug.

## 7. 404 is not retried

`404` was added to `status_forcelist` (`e570a58`) and removed one commit later
(`383ef48`); only `429` and `5xx` are retried now, with exponential backoff.

**Why:** 404, 400 and 401 are deterministic — retrying them burns five attempts
and hides the actual fault behind a timeout. Retries are for transient failures
only.

## 8. Staging is a view, not a table

`stg_games` started as a `CREATE TABLE` (`f419a28`) and became a
`CREATE OR REPLACE VIEW` (`de2c9b4`).

**Why:** a staging table needs a refresh step, and that step silently drifts from
the raw layer when it is not run. A view cannot be stale, so the raw layer stays
the single source of truth and the transformation is just SQL that can be edited
and re-read immediately.

**Cost:** every query recomputes the parse; there are no indexes or stored
statistics. Materialize it once analysis queries get slow — that is a
measurement, not a guess.

## 9. One pagination helper for every catalog

`ff6908e` replaced per-catalog fetchers with `fetch_catalog_pages(url)`.

**Why:** genres, platforms, parent platforms and stores all paginate through the
same `next` field. Duplicating the loop four times means fixing the retry or
pagination logic four times.

## Open decisions

* Games reference `genres`, `platforms` and `stores` as nested lists inside the
  JSONB payload. Normalizing them into bridge tables is pending and will decide
  whether the analytical layer can answer per-genre questions without `jsonb`
  unnesting.
* The transform layer is the current work. Nothing above blocks it: the raw
  layer is stable and re-transformable.
