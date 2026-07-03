You are an data engineer debugging and optimizing an ETL pipeline. We have an SQLite database located at `/home/user/events.db` containing a single table called `daily_metrics`:

```sql
CREATE TABLE daily_metrics (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    record_date TEXT,
    metric_value REAL
);
```
Currently, querying this table is slow, and we need to extract analytical data for our downstream pipeline. 

Your task is to create a Python script at `/home/user/etl_process.py` that does the following:
1. Connects to `/home/user/events.db` using the standard `sqlite3` module.
2. Creates an optimal composite index named `idx_user_date` on the `daily_metrics` table to speed up queries filtering by `user_id` and sorting by `record_date`. Ensure it uses `IF NOT EXISTS`.
3. Accepts a single command-line argument: the `user_id` (integer).
4. Executes a parameterized SQL query using a window function to calculate the "rolling 7-record sum" of `metric_value` for the specified `user_id`. The rolling 7-record sum includes the current record and the 6 preceding records based on the `record_date` ascending order.
5. Fetches the results and exports them to `/home/user/output.json`. 

The output JSON must be a list of dictionaries with exactly this format:
```json
[
  {
    "record_date": "2023-10-01",
    "rolling_sum": 10.5
  },
  ...
]
```
Ensure the `rolling_sum` values are floats rounded to 2 decimal places in Python if necessary, though standard SQLite float handling is fine.

To test your script, you should run it for `user_id` 5 like so:
`python3 /home/user/etl_process.py 5`

Ensure the script completes successfully and creates the `/home/user/output.json` file.