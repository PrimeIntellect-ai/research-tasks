You are a database administrator tasked with optimizing and analyzing a complex system's performance logs.

A SQLite database containing account hierarchy and query execution logs is located at `/home/user/app.db`.

The database has the following schema:
```sql
CREATE TABLE accounts (
    account_id INTEGER PRIMARY KEY,
    parent_account_id INTEGER
);

CREATE TABLE logs (
    log_id INTEGER PRIMARY KEY,
    account_id INTEGER,
    data TEXT, -- Contains JSON payload
    created_at DATETIME
);
```

The `data` column in the `logs` table contains JSON objects with a `query_time_ms` field (e.g., `{"query_time_ms": 150, "bytes_read": 1024}`).

Write a Bash script at `/home/user/generate_report.sh` that executes a SQL query against this database to compute a specific performance report and saves the output to `/home/user/report.csv`. 

The report must calculate and extract the following for each `account_id`:
1. **`account_id`**: The ID of the account.
2. **`root_account_id`**: The ID of the absolute top-level parent in the account hierarchy (the ancestor whose `parent_account_id` is NULL). If an account has no parent, it is its own root.
3. **`max_rolling_query_time`**: The maximum rolling sum of `query_time_ms` for that account, calculated by summing the `query_time_ms` of the *current log* and the *immediately preceding log* for that same account, ordered by `created_at`. 

Apply the following result processing constraints:
- Filter the results to only include accounts where the `max_rolling_query_time` is strictly greater than `100`.
- Sort the results by `max_rolling_query_time` in descending order, then by `account_id` in ascending order.
- Paginate the results to return only the top 5 records.

Your Bash script `/home/user/generate_report.sh` must:
1. Be executable (`chmod +x`).
2. Run the necessary SQLite commands to generate the output.
3. Format the output as a headerless CSV file saved to `/home/user/report.csv` containing precisely three columns: `account_id,root_account_id,max_rolling_query_time`.

Do not modify the original database. Only read from it.