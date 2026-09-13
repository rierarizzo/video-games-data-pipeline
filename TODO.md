# TODO

* Improve API retry handling for temporary errors such as `429`, `500`, `502`, `503`, and `504`.
* Add fault tolerance so the pipeline can resume from the last successfully processed page after a failure.
* Add incremental loading to avoid fetching and processing all RAWG pages on every execution.
