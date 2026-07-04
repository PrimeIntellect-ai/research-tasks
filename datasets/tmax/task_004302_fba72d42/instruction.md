You are acting as a data analyst working with database performance logs. We suspect that our database is experiencing deadlocks due to conflicting concurrent transactions. 

I have extracted a "wait-for" graph from the database logs and saved it as a CSV file at `/home/user/wait_for_graph.csv`. The CSV has two columns: `waiting_txn` and `holding_txn`. Each row indicates that the transaction in `waiting_txn` is waiting for a lock held by the transaction in `holding_txn`.

A deadlock occurs when there is a cycle in this directed wait-for graph. 

Your task is to write a Rust program in `/home/user/deadlock_detector/` that parses this CSV file, builds the graph, and detects the transactions involved in the deadlock (the cycle). 

Requirements:
1. Initialize a new Rust project at `/home/user/deadlock_detector/`.
2. Parse `/home/user/wait_for_graph.csv`.
3. Identify the transaction IDs that form a cycle in the graph. Assume there is exactly one cycle in the provided data.
4. Output the transaction IDs involved in the cycle as a JSON array of strings, sorted alphabetically, to the file `/home/user/deadlock_report.json`.

For example, if the cycle involves T1 waiting for T2, T2 waiting for T3, and T3 waiting for T1, the output in `/home/user/deadlock_report.json` should be exactly:
`["T1", "T2", "T3"]`

Run your Rust program to generate the output file.