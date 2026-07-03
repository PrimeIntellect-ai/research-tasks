You are a log analyst investigating patterns in a web application's access logs. The raw logs are messy, contain duplicate retries, and lack aggregated performance metrics.

Your task is to build a Bash-based data processing pipeline (using standard tools like `awk`, `jq`, `sqlite3`, `sha1sum`, etc.) that cleans the logs, deduplicates them, calculates rolling statistics, and bulk imports them into an SQLite database.

**Input Data:**
You have a raw log file located at `/home/user/raw_logs.txt`. Each line has the following format (pipe-separated):
`TIMESTAMP|IP|ENDPOINT|STATUS|RESPONSE_TIME_MS|PAYLOAD_JSON`

**Processing Requirements:**

1. **Hash-based Deduplication & Cleaning:**
   - Some clients send identical retry requests. You must deduplicate entries based on a composite key: `IP|ENDPOINT|PAYLOAD_JSON`.
   - Keep ONLY the *first* occurrence (chronologically) of each composite key. Discard the rest.
   - Filter out any rows where `RESPONSE_TIME_MS` is strictly less than `0` (this acts as your quality gate/validation checkpoint).

2. **Rolling Statistics Computation:**
   - For the deduplicated and cleaned logs, calculate a rolling average of `RESPONSE_TIME_MS` *per ENDPOINT*.
   - The rolling window should be the last **3** requests to that specific endpoint (including the current request).
   - If there are fewer than 3 requests for an endpoint so far, average the available requests.
   - The rolling average should be rounded down to the nearest integer (floor).

3. **CSV Generation:**
   - Save the intermediate processed data to `/home/user/processed_logs.csv`.
   - The CSV must have the following columns (comma-separated, no headers):
     `TIMESTAMP,IP,ENDPOINT,STATUS,RESPONSE_TIME_MS,ROLLING_AVG_MS,PAYLOAD_JSON`
   - *Note: Ensure your comma separation doesn't break on the JSON payload. The JSON in the raw logs does not contain raw commas at the top level, but it does contain them inside. Keep the JSON string intact as the last column.*

4. **Database Bulk Import:**
   - Create an SQLite database at `/home/user/logs.db`.
   - Create a table named `metrics` with the following schema:
     `CREATE TABLE metrics (timestamp TEXT, ip TEXT, endpoint TEXT, status INTEGER, response_time INTEGER, rolling_avg INTEGER, payload TEXT);`
   - Bulk import `/home/user/processed_logs.csv` into the `metrics` table.

**Deliverables:**
1. A Bash script or set of commands executed in the terminal that completes the pipeline.
2. The final processed CSV file at `/home/user/processed_logs.csv`.
3. The final SQLite database at `/home/user/logs.db` populated with the data.

Ensure all file paths match exactly.