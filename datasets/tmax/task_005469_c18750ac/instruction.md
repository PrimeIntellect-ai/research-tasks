You are a data analyst investigating a database issue. The system recently experienced several frozen transactions, and the engineering team suspects complex deadlocks (cyclic dependencies) are the cause. 

You have been given two CSV files extracted from the system's lock manager:
1. `/home/user/transactions.csv` - Contains `tx_id` (the transaction ID) and `amount` (the monetary value tied to the transaction).
2. `/home/user/locks.csv` - Contains `waiting_tx` (the ID of a transaction waiting for a lock) and `holding_tx` (the ID of the transaction currently holding that lock).

Your task is to identify all isolated deadlocks in the system. A deadlock occurs when a group of transactions form a cycle in the wait-for graph (e.g., A waits for B, B waits for C, C waits for A). 

Write a script in your preferred language to:
1. Parse the CSV files and construct a dependency graph.
2. Find all distinct transaction cycles (deadlocks) of length > 1. You can assume that each transaction belongs to at most one cycle (i.e., the deadlock components are disjoint).
3. For each deadlock cycle, calculate the `total_locked_amount` by summing the `amount` of all transactions involved in that cycle.
4. Output the results to a JSON file located at `/home/user/deadlock_report.json`.

The JSON file must be an array of objects, with each object structured exactly as follows:
```json
[
  {
    "cycle_members": ["TX_A", "TX_B", "TX_C"],
    "total_locked_amount": 1500.0
  }
]
```

Sorting requirements:
- The `cycle_members` array inside each object must be sorted alphabetically.
- The outer JSON array must be sorted in descending order by `total_locked_amount`. If there's a tie, sort alphabetically by the first element of `cycle_members`.

Execute your solution and ensure `/home/user/deadlock_report.json` is generated correctly.