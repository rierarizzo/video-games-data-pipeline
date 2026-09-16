# TODO

* Add fault tolerance so the pipeline can resume from the last successfully processed page after a failure.
* Improve incremental loading to avoid reprocessing records from the same day.
* Replace the current existing-ID lookup with PostgreSQL `ON CONFLICT` handling.
* Consider using an upsert strategy so existing games are updated when RAWG data changes.
