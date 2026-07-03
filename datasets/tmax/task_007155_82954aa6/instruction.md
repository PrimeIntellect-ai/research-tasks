You are a compliance officer auditing a database system for malicious activity. A recent outage was caused by an intentional deadlock. You need to forensically analyze the system logs to identify the users involved in this deadlock cycle.

You have been provided with two data exports:
1. `/home/user/locks.csv`: A CSV file containing a log of database lock requests.
   Columns: `timestamp,trx_id,resource_id,lock_mode,state`
   - `lock_mode` is either `SHARED` or `EXCLUSIVE`.
   - `state` is either `GRANTED` or `WAITING`.

2. `/home/user/trx_users.json`: A JSON document mapping transaction IDs (`trx_id`) to the users who initiated them.

Your task is to build a process that detects the deadlock.
A "wait-for" dependency occurs when Transaction A is `WAITING` for a lock on a `resource_id`, and Transaction B currently holds a `GRANTED` lock on that exact same `resource_id`, AND their lock modes conflict. 
Lock modes conflict if AT LEAST ONE of the locks (either the requested one or the held one) is `EXCLUSIVE`. (If both are `SHARED`, they do not conflict, and there is no wait-for dependency).

Perform the following steps:
1. Process the CSV and JSON files and ingest them into a format suitable for graph traversal and relational queries (you may use a SQLite database, Python, or shell tools).
2. Compute the wait-for graph: A directed edge from `trx_A` to `trx_B` exists if `trx_A` is waiting for a resource that `trx_B` holds in a conflicting mode.
3. Find the shortest deadlock cycle (a directed cycle in the wait-for graph).
4. Map the transactions in the cycle back to their respective `user_id`s.
5. Create a JSON report at `/home/user/deadlock_report.json` containing the ordered array of `user_id`s in the cycle.
   - The array must be ordered sequentially following the direction of the wait-for dependencies (User A waits for User B, who waits for User C...).
   - The cycle should start with the `user_id` that is lexicographically smallest.

Example output format for `/home/user/deadlock_report.json`:
```json
{
  "deadlock_cycle": ["U_AARON", "U_BETH", "U_CHUCK"]
}
```

Additionally, write the DDL schema you would use for a relational database approach to this problem into `/home/user/schema.sql`, making sure to include `CREATE INDEX` statements that would optimize the wait-for dependency join on massive datasets.