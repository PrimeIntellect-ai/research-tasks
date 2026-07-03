You are an analyst investigating database deadlocks. You have been given two CSV extracts from a database monitoring tool: `/home/user/locks.csv` and `/home/user/requests.csv`. 

Your task is to write a Python script `/home/user/detect_deadlocks.py` that processes these relational datasets, builds a "wait-for" dependency graph, detects deadlocks (cycles in the graph), and outputs the results as a strictly formatted JSON file.

### Data Description

1. **`/home/user/locks.csv`**
   Contains records of locks currently held by transactions.
   Columns: `tx_id`, `resource_id`, `lock_mode`
   `lock_mode` is either `SHARED` or `EXCLUSIVE`.

2. **`/home/user/requests.csv`**
   Contains records of locks requested by transactions that are currently blocked.
   Columns: `tx_id`, `resource_id`, `requested_mode`, `timestamp`
   `requested_mode` is either `SHARED` or `EXCLUSIVE`.

### "Wait-For" Graph Rules
A wait-for graph is a directed graph where nodes are transactions (`tx_id`). A directed edge exists from Transaction A to Transaction B (i.e., A waits for B) if and only if:
- Transaction A is requesting a lock on a resource (`resource_id`) that Transaction B currently holds a lock on, AND
- The lock modes conflict. 
  - Conflict occurs if at least one of the lock modes (held or requested) is `EXCLUSIVE`.
  - If A requests `SHARED` and B holds `SHARED`, they do NOT conflict, and A does not wait for B.
- Note: A transaction cannot wait for itself. 

### Task Requirements
1. Write a Python script `/home/user/detect_deadlocks.py` to parse the CSVs and build this directed graph. You may use standard libraries and `networkx`.
2. Find all simple cycles in the graph (representing deadlocks).
3. Materialize the output to `/home/user/deadlocks.json`.

**Output Schema (`/home/user/deadlocks.json`):**
The output must be a JSON array of arrays. Each inner array represents a deadlock cycle containing the `tx_id`s involved in the cycle.
- To ensure deterministic output, sort the `tx_id` strings alphabetically *within* each cycle array.
- Then, sort the outer list of arrays alphabetically based on the first element of each inner array (then the second, and so on).
- Only output unique cycles (e.g., if A->B->C->A and B->C->A->B are detected, only include `["A", "B", "C"]` once in the final output).

Example Output Format:
```json
[
  ["T1", "T2", "T3"],
  ["T4", "T5"]
]
```

Run your script to generate the final `deadlocks.json` file.