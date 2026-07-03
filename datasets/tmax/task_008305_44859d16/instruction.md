You are acting as a technical compliance officer auditing a database system's transaction logs to investigate system freezes. You suspect that concurrent transactions are frequently resulting in deadlocks. 

To prove this, you need to model the resource locks as a Wait-For Graph (WFG) and detect cycles. 

You have been provided a system dump of the current locking table at `/home/user/locks.csv`. 
The CSV has the following schema (with a header row):
`tx_id,resource_id,lock_state`

Where:
- `tx_id` is an integer representing the transaction ID.
- `resource_id` is a string (up to 10 characters) representing the locked resource.
- `lock_state` is either `HELD` (the transaction currently owns the lock on the resource) or `WAITING` (the transaction is blocked, waiting to acquire the lock).

In a Wait-For Graph, a directed edge exists from Transaction A to Transaction B if Transaction A is `WAITING` for a resource that is currently `HELD` by Transaction B. A transaction is considered "deadlocked" if it is part of a cycle in this directed graph. 

Your task:
1. Write a C program at `/home/user/detect_deadlocks.c` that parses `/home/user/locks.csv`.
2. The program must build the Wait-For Graph and perform a graph traversal to detect all transactions that are part of any cycle.
3. The program must output the deadlocked `tx_id`s to a file named `/home/user/deadlocks.log`.
4. The output must contain exactly one `tx_id` per line, sorted in ascending numerical order. Do not include any other text in the file.
5. Compile your C program to `/home/user/detect` using `gcc` and run it to produce the log file.