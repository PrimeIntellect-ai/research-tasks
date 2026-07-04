You are a localization systems engineer. We have a translation ingestion pipeline located at `/app/localization_pipeline/` that processes CSV files containing UI strings and their localized translations. Our current pipeline has two major issues: it is mechanically broken due to misconfigured service routing, and the data processor silently drops translation entries that contain valid embedded newlines (or crashes on maliciously formatted rows).

Your objective is to fix the multi-service integration and build a robust translation sanitizer/filter.

Part 1: Multi-Service Configuration
The ingestion system consists of three services running on this machine:
1. An Nginx reverse proxy (listening on port 8080).
2. A FastAPI receiver service (running on port 5000, supposed to receive files via POST `/upload`).
3. A Redis instance (listening on port 6379).
4. A Python Celery worker (running in the background, reading from Redis and writing aggregated statistics to `/home/user/processed_stats.json`).

Currently, the Nginx configuration at `/app/localization_pipeline/nginx.conf` is missing the correct upstream routing to the FastAPI receiver, and the FastAPI application (`/app/localization_pipeline/receiver.py`) has an empty Redis connection URI. 
You must:
- Update `/app/localization_pipeline/nginx.conf` to correctly proxy traffic from `http://127.0.0.1:8080/upload` to the FastAPI service.
- Update the `REDIS_URL` environment variable or connection string in `/app/localization_pipeline/receiver.py` so it queues jobs properly.
- Restart the services using `/app/localization_pipeline/restart_services.sh`.
Ensure that sending a test CSV via `curl -X POST -F "file=@test.csv" http://127.0.0.1:8080/upload` results in a queued job that the worker successfully acknowledges.

Part 2: Translation CSV Filter (The Verifier)
The Celery worker uses a filter script to validate CSV files before processing them. You must write a Python script at `/home/user/translation_filter.py`.
This script will be used as a CLI tool: `python3 /home/user/translation_filter.py <input.csv> <output.csv>`

The script must perform the following:
1. Timestamp Alignment: Read the `updated_at` column (which comes in various formats like ISO8601, Unix Epoch, or MM/DD/YYYY) and normalize it to a strict ISO8601 UTC string (e.g., `2023-10-04T15:30:00Z`).
2. Feature Extraction: Extract the language code from the `locale` column (e.g., `en-US` -> `en`, `es-ES` -> `es`) and store it in a new column called `lang_primary`.
3. Embedded Newlines & Sanitization (The Core Challenge): 
   - Some valid localization strings contain intentional, properly escaped embedded newlines (e.g., `"Line 1\nLine2"`). Your script MUST preserve these and correctly parse the CSV without dropping the row.
   - Some rows are "evil" (e.g., containing unescaped newline injections, null bytes, or mismatched quote blocks designed to break standard string-split parsers). Your script must detect these structurally invalid rows and silently drop them, rather than corrupting the output CSV or crashing.
   - Compute summary statistics: The script must print to `STDOUT` a JSON object with the following schema exactly:
     `{"total_input_rows": X, "valid_rows_kept": Y, "invalid_rows_dropped": Z}`

To complete the task, ensure the services are running and your `translation_filter.py` script is fully implemented. An automated verifier will test your script against a hidden corpus of "clean" (properly formatted, valid embedded newlines) and "evil" (malformed, injection-attempt) CSVs.