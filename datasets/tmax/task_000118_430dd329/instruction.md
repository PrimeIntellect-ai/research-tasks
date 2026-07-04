You are a data analyst investigating a database system that has frozen up. You have exported a snapshot of the current transaction lock statuses into a CSV file located at `/home/user/locks.csv`. 

The CSV file has three columns:
1. `tx_id`: The ID of the transaction.
2. `resource_held`: The ID of the resource currently locked and held by this transaction (can be empty/null if none).
3. `resource_requested`: The ID of the resource this transaction is currently waiting to acquire (can be empty/null if none).

A deadlock occurs when there is a cycle in the "wait-for" graph. A transaction `A` waits for transaction `B` if `A` requests a resource that `B` currently holds. 

Your task is to:
1. Write a Python script to read `/home/user/locks.csv`.
2. Parse the schema and map the relationships to build a directed "wait-for" graph of the transactions.
3. Traverse the graph to find the deadlock cycle. (You can assume there is exactly one isolated cycle in the data).
4. Output the transaction IDs involved in the deadlock cycle to a file named `/home/user/deadlock.txt`. 

The output format in `/home/user/deadlock.txt` must be a single line of comma-separated transaction IDs representing the path of the cycle. To ensure consistency, start the cycle with the transaction ID that is **lexicographically smallest**, and maintain the directed order of the wait-for relationships. 

For example, if T3 waits for T8, T8 waits for T5, and T5 waits for T3, the lexicographically smallest is T3. The wait-for path from T3 is T3 -> T8 -> T5. The output should be strictly:
`T3,T8,T5`