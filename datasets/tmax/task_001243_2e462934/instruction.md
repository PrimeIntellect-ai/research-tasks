You are a data scientist responsible for cleaning and normalizing sensor data pipelines. 

We process high-frequency JSON-lines (JSONL) files. Recently, malformed logs have been causing our legacy C++ ingestion engine to crash. We have isolated a stripped compiled binary of the legacy engine's validation logic at `/app/validator`. It reads a single JSON line from standard input and exits with code 0 if safe, or crashes (exit code 139 / segfault) if it encounters the fatal edge cases (related to specific Unicode escape sequence anomalies in text fields). 

Your task is to write a robust Python pipeline that filters out the "evil" lines and performs cleaning, resampling, and database exporting for the safe lines.

Create a script at `/home/user/pipeline.py` that takes two arguments:
`python /home/user/pipeline.py <input.jsonl> <output.db>`

For each JSONL file processed, your script must:
1. **Filter**: Drop any JSON object that would crash the `/app/validator` binary. (Calling the binary for every line is too slow for production; you must deduce the crashing condition by experimenting with the binary and implement the filter natively in Python).
2. **Extraction**: From the raw text `comment` field of valid rows, extract the structured error code. The comment contains text like `"Reading stable. [CODE: E-492]"` - extract `E-492` into a new field `error_code`. If no code is present, use `NULL`.
3. **Cleaning & Deduplication**: Normalize `sensor_id` to uppercase. Deduplicate records based on `sensor_id` and `timestamp` (keep the record that appears last in the file).
4. **Resampling & Gap-Filling**: For each `sensor_id`, resample the time-series to exactly 1-minute intervals. Forward-fill missing values in the `reading` field for up to 3 minutes.
5. **Export**: Bulk import the finalized dataset into a SQLite database (`<output.db>`), in a table named `processed_sensors` with columns: `timestamp` (ISO8601 string), `sensor_id` (TEXT), `reading` (FLOAT), and `error_code` (TEXT).

Ensure your script handles standard edge cases and runs efficiently. You are provided with some sample data in `/home/user/sample.jsonl` to test your assumptions.