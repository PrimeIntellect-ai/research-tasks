You are tasked with fixing and processing a corrupted dataset from our server configuration manager. The system exports configuration changes and mathematical metrics as a JSON-lines file, but a recent bug introduced several issues that you must resolve.

The raw data is located at `/home/user/raw_configs.jsonl`.

Your goal is to build a Python ETL pipeline that performs the following steps:

1. **Parse and Clean (Handling Corrupted JSON):**
   The JSON-lines file contains invalid unicode escape sequences (e.g., `\uXXXX` where `XXXX` are not valid hex characters) in the `metadata` field. Standard JSON parsers will throw a `JSONDecodeError`. You must write a parser that safely sanitizes these lines (e.g., by stripping or replacing invalid unicode escapes) before parsing.

2. **Hash-based Deduplication:**
   Due to retry loops in the logging system, there are duplicate entries. For each parsed JSON object, compute the SHA-256 hash of the string concatenated from `server_id` and `timestamp` (e.g., `srv-1_1680000000`). If multiple entries produce the same hash, keep only the first one encountered in the file and discard the rest.

3. **Parallel Processing:**
   You must implement the parsing and deduplication step using parallel processing (e.g., Python's `multiprocessing` module) to process the data efficiently.

4. **Mathematical Interpolation & Imputation:**
   The JSON objects contain two metric fields: `temp_celsius` and `cpu_load`. Many of these values are recorded as `null`.
   Group the deduplicated data by `server_id`. Sort each group chronologically by `timestamp`.
   For each server, use **linear interpolation** to fill in the missing (`null`) values for both `temp_celsius` and `cpu_load`. 
   * Rule: If the first or last values in a server's time series are `null`, use forward-fill for trailing nulls and backward-fill for leading nulls after the linear interpolation.

5. **Database Bulk Import & Export:**
   * Bulk insert the cleaned, deduplicated, and interpolated data into an SQLite database located at `/home/user/configs.db` in a table named `metrics`. The table should have columns: `server_id` (TEXT), `timestamp` (INTEGER), `temp_celsius` (REAL), `cpu_load` (REAL).
   * Query the database to calculate the average `temp_celsius` and `cpu_load` for each `server_id`.
   * Export these averages to a CSV file at `/home/user/final_averages.csv` with the headers: `server_id,avg_temp,avg_load`. Round the averages to 2 decimal places.

Ensure your script is self-contained, runs automatically, and handles the missing data accurately.