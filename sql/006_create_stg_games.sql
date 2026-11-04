CREATE OR REPLACE VIEW stg_games AS
SELECT
    id,
    data->>'slug' AS slug,
    data->>'name' AS name,
    (data->>'playtime')::INT AS playtime,
    (NULLIF(data->>'released', ''))::DATE AS released,
    (data->>'tba')::BOOLEAN AS to_be_announced,
    (data->>'rating')::DECIMAL AS rawg_rating,
    (data->>'ratings_count')::INT AS rawg_ratings_count,
    (data->>'added')::INT AS added_to_library,
    (data->>'metacritic')::DECIMAL AS metacritic_score,
    (data->>'updated')::TIMESTAMP AT TIME ZONE 'UTC' AS updated_at
FROM raw_games;