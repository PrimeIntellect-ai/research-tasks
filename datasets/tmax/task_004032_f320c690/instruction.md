You are assisting a compliance officer in auditing system logs for potential race conditions and deadlock risks. We have an exported document-based audit log of database transactions, but we need to analyze it relationally to find concurrent operations.

The raw log is located at `/home/user/audit_logs.json`. It contains a list of JSON objects representing transactions, each with the following keys:
- `tx_id` (string)
- `account_id` (string)
- `start_time` (integer, epoch milliseconds)
- `end_time` (integer, epoch milliseconds)
- `operation` (string)

Your task is to:
1. Parse this JSON file and map the document data into a relational SQLite database located at `/home/user/audit.db`. The table must be named `transactions` and contain the exact columns matching the JSON keys.
2. Design and create an optimal database index (or indexes) on the `transactions` table to specifically accelerate partitioning by account and sorting by start time.
3. Query the database to identify "overlapping" transactions (potential deadlock risks). An overlap occurs if, for a given `account_id`, the *very next* transaction (chronologically by `start_time`) starts strictly before the current transaction's `end_time`. 
   *CRITICAL REQUIREMENT:* You must use SQL Window Functions (e.g., `LEAD`) to perform this analytical aggregation. Do not use self-joins.
4. Filter the results to only include those where an overlap is detected.
5. Sort the final output by `account_id` in DESCENDING order, and then by the current transaction's `tx_id` in ASCENDING order.
6. Apply pagination/limiting to return exactly the first 10 overlapping pairs.
7. Save the processed results to `/home/user/deadlock_risks.csv`. The CSV must have exactly these headers: `account_id,current_tx,next_tx`.

You may use Python, bash, or the `sqlite3` CLI to complete this task. 
Ensure the CSV is correctly formatted and contains only the headers and the 10 rows of data.