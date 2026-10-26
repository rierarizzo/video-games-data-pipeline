CREATE TABLE IF NOT EXISTS etl_state (
    source VARCHAR PRIMARY KEY,
    last_completed_day DATE NOT NULL
);