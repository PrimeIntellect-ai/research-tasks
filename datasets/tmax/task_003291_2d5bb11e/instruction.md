You are managing a configuration tracking system that monitors state changes across a fleet of servers. The raw configuration logs have become bloated with duplicate entries, sensitive credentials, and inconsistent timestamp formats.

Your task is to process a JSONL log file located at `/home/user/raw_configs.jsonl` and load the cleaned data into an SQLite database at `/home/user/config_history.db`. 

You may use any programming language (e.g., Python, Node.js) available on the system.

Please perform the following steps:
1. **Large-file streaming & Parsing**: Read `/home/user/raw_configs.jsonl` line by line. Each line is a JSON object with keys: `host_id`, `recorded_at`, and `state`.
2. **Timestamp Alignment**: The `recorded_at` field contains timestamps in various formats (e.g., ISO 8601, common log format). Convert every timestamp into a standard UNIX epoch timestamp (integer).
3. **Data Masking**: Inside the `state` object, if there are any keys named exactly `api_key` or `password`, change their values to the exact string `"***"`.
4. **Hash-based Deduplication**: Compute the SHA-256 hex digest of the *masked* `state` object (serialized as a compact JSON string with sorted keys, e.g., `{"api_key":"***","port":80}`). For each `host_id`, only keep the *first* occurrence of any given state hash. Ignore subsequent logs for that host that produce the exact same masked state hash.
5. **Database Import**: Create an SQLite database at `/home/user/config_history.db` with a table named `changes` having the following schema:
   `CREATE TABLE changes (host_id TEXT, epoch INTEGER, state_hash TEXT, masked_state TEXT);`
   Insert the processed, deduplicated records into this table.

Ensure your script handles the file efficiently and creates the database with the exact schema and table name specified.