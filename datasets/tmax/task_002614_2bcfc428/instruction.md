You are a data engineer building an ETL pipeline that includes a monitoring system for database health. One critical issue is transaction deadlocks. 

You have been provided an SQLite database at `/home/user/etl_locks.db` which contains two tables representing a snapshot of currently running database transactions and their resource locks:

1. `transactions`
   - `tx_id` (TEXT): Unique transaction identifier.
   - `start_time` (DATETIME): When the transaction started.
   - `query` (TEXT): The SQL query being executed.

2. `locks`
   - `tx_id` (TEXT): The transaction requesting or holding the lock.
   - `resource_id` (TEXT): The resource being locked (e.g., table or row ID).
   - `status` (TEXT): Either 'GRANTED' (the transaction holds the lock) or 'WAITING' (the transaction is blocked waiting for the resource).

A deadlock occurs when there is a cycle in the wait-for graph. For example: Transaction A is WAITING for a resource GRANTED to Transaction B, which in turn is WAITING for a resource GRANTED to Transaction A.

**Your Task:**
Write a Python script at `/home/user/deadlock_detector.py` that:
1. Connects to `/home/user/etl_locks.db`.
2. Computes the wait-for graph and identifies all transactions that are part of a deadlock cycle (using a recursive CTE, graph traversal library, or hierarchical query).
3. Uses a window function (or equivalent analytical aggregation) to rank ONLY the deadlocked transactions by their `start_time` in ascending order (oldest transaction = rank 1).
4. Outputs the results to a CSV file at `/home/user/deadlocks.csv` with exactly this header: `tx_id,rank,query`. 
5. Run your script so the CSV is generated.

The CSV should strictly use comma separators and include only the transactions involved in cycles.