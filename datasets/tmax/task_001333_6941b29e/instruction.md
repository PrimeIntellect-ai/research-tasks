You are tasked with building a Rust-based Configuration Tracker and ETL Data Cleaner service.

A legacy ETL job regularly fails and retries, producing duplicate records and incomplete metrics. You need to create an HTTP network service in Rust that ingests these metrics, cleans them, and serves the finalized configuration state. 

Additionally, the legacy system relies on a rotating authentication token. The current token has been securely transmitted via an automated voice system and saved as an audio file at `/app/auth_token.wav`. 

Requirements:
1. **Audio Transcription**: Listen to (or transcribe) the audio file at `/app/auth_token.wav`. It contains a short spoken phrase which serves as the Bearer token for your HTTP API.
2. **Rust HTTP Service**: 
   - Initialize a new Rust project at `/home/user/etl_tracker`.
   - The server MUST listen on `127.0.0.1:8080`.
   - Implement a `POST /ingest` endpoint that accepts JSON arrays of ETL records.
   - Implement a `GET /config` endpoint that returns the cleaned JSON state.
   - Both endpoints must require the `Authorization: Bearer <transcribed_phrase>` header. Return `401 Unauthorized` if missing or incorrect.
3. **Data Cleaning Logic (in Rust)**:
   - The ingested JSON looks like: `[{"sequence": 1, "metric": 10.5, "config_hash": "a1b2c"}, {"sequence": 2, "metric": null, "config_hash": "a1b2d"}, ...]`
   - **Interpolation/Imputation**: Some records have `null` for `metric`. You must impute these missing values using linear interpolation based on the nearest valid `metric` values ordered by `sequence`. (If the first or last values are missing, carry over the nearest valid value).
   - **Distance/Similarity Deduplication**: The ETL retry mechanism creates near-duplicate `config_hash` strings. You must compute the Levenshtein distance between `config_hash` values. If a record has a `config_hash` with a Levenshtein distance of 2 or less from any *previously processed* record's `config_hash`, it is considered a duplicate and must be discarded.
   - The server should maintain an in-memory state of the cleaned, accumulated records.

Please write, compile, and run this Rust server so it is actively listening on port 8080. Leave the server running in the background when you complete your task.