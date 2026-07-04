You are an AI assistant helping a database researcher analyze distributed transaction logs to detect and resolve deadlocks. 

The researcher has extracted transaction metadata and lock-wait events from a distributed system. The data is spread across two different representations:
1. A document store export: `/home/user/tx_metadata.json` containing metadata about each transaction (transaction ID, start time, user).
2. A relational export: `/home/user/lock_waits.csv` containing the "wait-for" edges. The columns are `waiter_tx`, `holder_tx`, and `wait_timestamp`. A row indicates that `waiter_tx` is blocked waiting for a lock held by `holder_tx`.

Your task is to write and execute a Python script (`/home/user/analyze_deadlocks.py`) that performs the following steps:
1. Parse the JSON and CSV files to map the relational and document data into a unified directed graph structure (a "wait-for" graph where edges point from waiter to holder).
2. Detect all deadlocks in the system. A deadlock is defined as an elementary circuit (directed cycle) in the wait-for graph.
3. For each detected cycle, you must select a "victim" transaction to abort. To do this, perform an analytical aggregation over the edges *within that specific cycle*: the victim is the `waiter_tx` of the edge in the cycle that has the **maximum (latest) `wait_timestamp`**. (Assume no ties in timestamps).
4. Save the results to `/home/user/deadlock_victims.csv`.

The output file `/home/user/deadlock_victims.csv` must have exactly two columns, with a header row:
- `cycle_members`: A hyphen-separated string of the transaction IDs involved in the cycle, sorted lexicographically (e.g., `T1-T2-T3`).
- `victim_tx`: The transaction ID of the chosen victim.

Constraints and guarantees:
- Every transaction in `lock_waits.csv` will exist in `tx_metadata.json`.
- Ignore any nodes or edges that are not part of a cycle.
- If there are independent, disconnected cycles, process all of them.
- Standard libraries and `networkx` / `pandas` are allowed.

Write the script, run it, and ensure `/home/user/deadlock_victims.csv` is correctly generated.