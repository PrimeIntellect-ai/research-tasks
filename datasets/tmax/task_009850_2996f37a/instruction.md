You are a log analyst investigating suspicious user activity patterns. You need to process a messy server log file, extract key fields, clean the data, calculate an anomaly score based on User-Agent similarity, and export the results to a database.

You must implement a tool in Rust to process the logs, and then use standard bash tools (`sqlite3`) to load the processed data into a database.

**Inputs:**
A raw log file is located at `/home/user/raw_logs.txt`.
Each valid line in the log follows this exact format:
`[{TIMESTAMP}] {IP_ADDRESS} "{METHOD} {PATH} {PROTOCOL}" {STATUS_CODE} "{USER_AGENT}" "{SESSION_ID}"`

Example valid line:
`[2023-10-01T10:00:00Z] 192.168.1.10 "GET /api/v1//data HTTP/1.1" 200 "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "sess_123"`

**Requirements:**
1. Create a new Rust project at `/home/user/log_processor` to perform the data processing.
2. Read the file `/home/user/raw_logs.txt`.
3. **Regex & Validation:** Parse the lines using regex. Discard any malformed lines that do not strictly adhere to the expected format (quality gate).
4. **Cleaning:** Normalize the extracted `{PATH}` by replacing any occurrences of multiple consecutive slashes (e.g., `//` or `///`) with a single slash `/`.
5. **Deduplication:** Keep only the *first* valid log entry for each unique `{SESSION_ID}`. Discard subsequent entries with a previously seen session ID.
6. **Distance Computation:** Calculate the Levenshtein distance (edit distance) between the extracted `{USER_AGENT}` and the baseline string: `"Mozilla/5.0 (Windows NT 10.0; Win64; x64)"`. You must implement the Levenshtein distance algorithm manually in your Rust code.
7. **Export:** Output the cleaned, deduplicated data to a CSV file at `/home/user/processed_logs.csv` with the following columns in order (NO header row):
   `timestamp,ip_address,path,status_code,session_id,ua_distance`
8. **Database Import:** Use the `sqlite3` CLI tool to bulk import `/home/user/processed_logs.csv` into an SQLite database at `/home/user/logs.db`. The table should be named `cleaned_logs` with the columns `timestamp TEXT, ip_address TEXT, path TEXT, status_code INTEGER, session_id TEXT, ua_distance INTEGER`.

Ensure your Rust tool compiles and runs correctly, and that the final SQLite database is populated with the correct rows.