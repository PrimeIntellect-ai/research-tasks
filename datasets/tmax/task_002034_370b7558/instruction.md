You are tasked with fixing a broken query builder and writing a robust data aggregation script to analyze database transaction logs for a DBA team. 

We use a custom, internal Python package called `tiny_sql_builder` (located at `/app/tiny_sql_builder`). Unfortunately, the package has a bug in its window function implementation which drops the `ORDER BY` clause inside the `OVER` block. 

Your task involves two parts:

1. **Fix the vendored package**: Inspect `/app/tiny_sql_builder` and fix the `Window` class so that it properly renders the `ORDER BY` clause when provided.
2. **Write an Aggregation Script**: Create an executable Python script at `/home/user/aggregate.py`.
   - The script must read JSON Lines (JSONL) from `stdin`. Each line represents a transaction event with the schema: `{"tx_id": str, "user_id": int, "status": str, "timestamp": int}`. The `status` can be "success", "rollback", or "deadlock".
   - Load this data into an in-memory SQLite database.
   - Use the fixed `tiny_sql_builder` package to construct a SQL query that calculates the **maximum time difference (interval)** between *consecutive* deadlocks for each `user_id`. You must use a SQL window function (e.g., `LAG` or `LEAD`) to find the difference in `timestamp` between a deadlock and the immediately previous deadlock for the same user.
   - Only include users who have experienced **2 or more** deadlocks.
   - Output the aggregated results to `stdout` as a strictly formatted JSON object matching this schema:
     ```json
     {
       "results": [
         {
           "user_id": 123,
           "max_deadlock_interval": 450
         }
       ]
     }
     ```
   - The `results` array must be sorted by `user_id` in ascending order.
   - If no users meet the criteria, output `{"results": []}`.

Ensure your script is robust and deterministic. Automated fuzz-testing will pipe hundreds of random JSONL streams into your script and compare its exact output bit-for-bit against a verified oracle.