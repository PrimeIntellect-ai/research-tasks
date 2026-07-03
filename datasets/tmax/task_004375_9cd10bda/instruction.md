As a database administrator, you are investigating a severe performance degradation in your distributed database. You suspect that complex cross-query aggregations have resulted in circular dependencies (deadlocks) among several concurrent transactions. 

You have exported a snapshot of the current resource locks into a CSV file located at `/home/user/locks.csv`.

The CSV has the following header and columns:
`tx_id,holds_resource,waits_for_resource`

Each row represents a lock state for a transaction:
- `tx_id`: The ID of the transaction (e.g., T1).
- `holds_resource`: The ID of a resource the transaction currently holds an exclusive lock on (e.g., R1). This can be empty if the row just indicates a waiting state.
- `waits_for_resource`: The ID of a resource the transaction is trying to lock but is currently waiting for. This can be empty if the row just indicates a holding state.

Your task is to write a C++ program `/home/user/detect_deadlocks.cpp` that parses this CSV and performs graph analytics to find the root cause of the deadlocks. 

Specifically, the program must:
1. Parse `/home/user/locks.csv`.
2. Construct a directed "Wait-For Graph" of transactions. A directed edge exists from Transaction A to Transaction B if Transaction A is waiting for a resource that is currently held by Transaction B.
3. Detect all transactions that are part of at least one cycle in this Wait-For Graph (these are the deadlocked transactions).
4. For only the transactions involved in a cycle, calculate their "wait-degree" (the out-degree in the Wait-For Graph, meaning the number of unique transactions they are directly waiting for).
5. Output the deadlocked transactions and their wait-degrees to `/home/user/deadlock_report.txt`.

The output file `/home/user/deadlock_report.txt` must contain exactly one line per deadlocked transaction in the format `tx_id:wait_degree`, sorted alphabetically by `tx_id`.

Example output format:
```
T1:2
T2:1
T3:1
```

Compile your C++ code using `g++ -std=c++17 /home/user/detect_deadlocks.cpp -o /home/user/detect_deadlocks` and run it to produce the report. Do not use any external libraries other than the C++ standard library.