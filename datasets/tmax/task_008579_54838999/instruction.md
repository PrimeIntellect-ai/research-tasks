I need you to act as a data analyst and help me process a database lock dependency log to identify a specific deadlock risk chain. 

I have a file located at `/home/user/locks.csv`. This file logs transactions that are currently waiting on locks held by other transactions. It has three columns:
1. `waiting_txn`: The ID of the transaction that is blocked.
2. `holding_txn`: The ID of the transaction holding the lock.
3. `wait_time_ms`: The time in milliseconds the `waiting_txn` has been waiting (representing the weight of the edge).

This data forms a directed graph where an edge goes from `waiting_txn` to `holding_txn` with the weight `wait_time_ms`.

Your task is to:
1. Parse the CSV file and build a directed graph.
2. Find the shortest path (based on the total sum of `wait_time_ms`) from transaction `T10` to transaction `T50`.
3. Export the resulting path as a JSON array of transaction IDs (strings) representing the sequence of nodes in the shortest path, starting with `"T10"` and ending with `"T50"`. 
4. Save this JSON array exactly to the file `/home/user/deadlock_path.json`.

You can use any programming language you are comfortable with to write a script and execute it to generate the result. Ensure the final JSON file contains only the array (e.g., `["T10", "T...", "T50"]`) and is valid JSON.