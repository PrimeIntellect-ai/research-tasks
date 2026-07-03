You are a Database Administrator investigating a complete system freeze caused by multiple transaction deadlocks.

You have extracted the current lock wait-graph into a SQLite database located at `/home/user/locks.db`.
The database contains a single table:
`waits_for`
- `waiting_tx` (INTEGER): The ID of the transaction that is waiting.
- `blocking_tx` (INTEGER): The ID of the transaction holding the lock.

This table represents a directed graph where an edge from A to B means A is waiting for B. A deadlock occurs when there is a cycle in this graph (e.g., A waits for B, B waits for C, and C waits for A). 

Your task is to identify all transactions that are actively participating in a deadlock cycle.

Write a Bash script at `/home/user/detect_deadlocks.sh` that:
1. Queries the `/home/user/locks.db` database.
2. Performs graph analytics (cycle detection) to identify all `waiting_tx` IDs that are part of a circular dependency (a cycle of any length).
3. Writes the unique IDs of all deadlocked transactions to `/home/user/deadlocked_txs.txt`.
4. The output file must contain one transaction ID per line, sorted in ascending numerical order.

Note: Transactions that are waiting on a deadlocked transaction but are not part of the cycle themselves should *not* be included in the output.

Ensure your script is executable and completely self-contained. You may use standard Linux tools (bash, sqlite3, python3, awk, etc.) to accomplish this.