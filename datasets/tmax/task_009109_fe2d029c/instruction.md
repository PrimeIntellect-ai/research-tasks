You are acting as a data analyst. You have been given an export of transaction wait states from our NoSQL database's internal diagnostic logs. The data is exported as a CSV file located at `/home/user/waits.csv`.

The CSV contains two columns: `tx_id` (the transaction that is waiting) and `waiting_for_tx_id` (the transaction it is waiting on). Together, these form a directed "Wait-For Graph". 

A deadlock occurs when there is a cycle in this wait-for graph (e.g., Transaction A waits for B, B waits for C, and C waits for A).

Your task is to:
1. Reverse engineer the wait-for graph from the CSV data.
2. Identify all unique `tx_id`s that are actively participating in any deadlock (i.e., they are part of a cycle in the directed graph). Note: Do not include transactions that are merely waiting on a deadlocked transaction but are not part of the cycle themselves.
3. Export the resulting deadlocked transaction IDs to a new CSV file at `/home/user/deadlocks.csv`. 

The output file `/home/user/deadlocks.csv` must have exactly one column with the header `deadlocked_tx_id`. The IDs must be sorted in ascending numerical order.

You may write and execute a script (e.g., Python, Bash/Awk) to process the graph and find the cycles.