CREATE TABLE IF NOT EXISTS stg_games (
    id INTEGER PRIMARY KEY,
    slug VARCHAR NOT NULL,
    name VARCHAR NOT NULL,
    playtime INTEGER,
    released DATE,
    to_be_announced BOOLEAN,
    rawg_rating DECIMAL,
    rawg_rating_count INTEGER,
    added_to_library INTEGER,
    metacritic_score DECIMAL,
    updated_at TIMESTAMP
)