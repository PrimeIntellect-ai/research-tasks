You are a data analyst tasked with identifying transaction deadlocks from database logs. 

In a database, a deadlock occurs when two or more transactions form a circular dependency, waiting for locks held by each other. You have been provided with two CSV files representing a snapshot of the database state:
1. `/home/user/data/held_locks.csv` (Columns: `txn_id`, `resource_id`)
2. `/home/user/data/requested_locks.csv` (Columns: `txn_id`, `resource_id`)

A "Wait-For Graph" (WFG) is a directed graph where each node is a transaction (`txn_id`). A directed edge exists from `Txn_A` to `Txn_B` if `Txn_A` has requested a lock on a `resource_id` that is currently held by `Txn_B`.

Your task:
1. Write a Python script `/home/user/detect_deadlocks.py` that reads these CSV files and constructs the Wait-For Graph.
2. Find all elementary cycles (deadlocks) in this graph.
3. Save the results to `/home/user/deadlocks.json`. The JSON file must contain a single list of lists, where each inner list represents a cycle of `txn_id` strings (e.g., `[["T1", "T2"], ["T3", "T4", "T5"]]`). Order of nodes within a cycle or order of cycles does not matter.
4. **Important Constraint:** You must use the `networkx` library to detect the cycles. However, you are operating in an offline, air-gapped environment. A vendored copy of the `networkx` source code has been provided at `/home/user/vendor/networkx`. You must ensure your script imports this specific copy.
5. The vendored `networkx` package has a known bug introduced by a recent internal patch that affects cycle detection. You will need to identify the bug in the vendored library's source code and fix it before your script can output the correct deadlocks.

To succeed, you must run your script and ensure `/home/user/deadlocks.json` is correctly populated with all transaction cycles.