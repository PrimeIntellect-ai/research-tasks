You are a data engineer troubleshooting an ETL pipeline that has become stuck. We suspect a deadlock between concurrent transactions. 

I have captured a snapshot of the current lock-wait graph in a SQLite database located at `/home/user/etl_locks.db`. 

The database contains a single table:
`CREATE TABLE lock_waits (waiter_tx TEXT, holder_tx TEXT, wait_start_ms INTEGER);`

Each row indicates that `waiter_tx` is currently blocked waiting for a lock held by `holder_tx`. `wait_start_ms` is the epoch timestamp (in milliseconds) when the wait began. 

There is exactly one deadlock cycle in this data (e.g., A waits for B, B waits for C, C waits for A).

Your task is to write a Python script at `/home/user/process_deadlock.py` that:
1. Connects to `/home/user/etl_locks.db`.
2. Uses a single SQL query (utilizing recursive CTEs for graph traversal and window functions for analytical ranking) to:
   - Identify all transactions (`waiter_tx`) that are part of the deadlock cycle.
   - Rank the transactions in the cycle based on their `wait_start_ms` in ascending order (earliest wait gets rank 1).
3. Executes the query and processes the result, saving it to `/home/user/deadlock_report.csv`.

The output CSV must have exactly this header: `tx_id,wait_start_ms,cycle_rank`
The rows should be ordered by `cycle_rank` ascending.

You can use the terminal to explore the database, test your queries, and run your Python script. The final verification will check the contents of `/home/user/deadlock_report.csv`.