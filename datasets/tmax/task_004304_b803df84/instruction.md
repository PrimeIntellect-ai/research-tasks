You are acting as a compliance officer auditing a system's document access logs. The logs are stored in an SQLite database at `/home/user/audit.db`. 

Recently, the compliance monitoring system flagged this database because its index on the timestamp column (`idx_timestamp`) is corrupted, causing it to return stale or missing rows for recent queries. 

Your task is to trace a leaked document's access chain. To do this, write a Bash script at `/home/user/audit_trace.sh` that does the following:
1. Takes a single argument: the starting `access_id` (e.g., `1`).
2. Safely passes this argument to an `sqlite3` command to query `/home/user/audit.db`.
3. Before querying, the script must execute the `REINDEX;` command to fix the corrupted indices and ensure accurate data retrieval.
4. Using a Recursive CTE, retrieves the initial access record matching the provided `access_id` and all subsequent access records that stem from it (matching `parent_access_id` to the previous `id`).
5. Uses a Window Function to calculate a sequential number (`user_seq`) for each user's actions within this specific access chain. The sequence should start at 1 for each `user_id` and be ordered chronologically by `timestamp`.
6. Outputs the result in CSV format with the exact headers: `id,user_id,doc_id,timestamp,user_seq`.

After writing the script, make it executable and run it with the starting `access_id` of `1`. Redirect the output to `/home/user/audit_result.csv`.

Ensure your bash script properly parameterizes the SQL query to prevent SQL injection or quoting issues, even though this is an internal tool.