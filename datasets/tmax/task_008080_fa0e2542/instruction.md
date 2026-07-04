You are a data analyst troubleshooting a database concurrency issue. The database engineering team has exported a snapshot of transaction lock waits into a CSV file located at `/home/user/wait_graph.csv`.

The CSV has the following columns: `waiter_tx`, `holder_tx`, `resource`, `wait_time_ms`. 
Each row represents a directed edge in a wait graph, where `waiter_tx` is waiting for a lock on `resource` currently held by `holder_tx` for `wait_time_ms` milliseconds.

Your task is to identify and extract specific "deadlock" cycles from this relational data by mapping it to a graph. 

Requirements:
1. Parse `/home/user/wait_graph.csv`.
2. Filter the data: Ignore any wait records where `wait_time_ms` is 100 or less.
3. Find all "deadlock" cycles of exactly length 3. A length-3 cycle means Transaction A waits for B, B waits for C, and C waits for A.
4. Normalize each cycle: Represent each cycle as a JSON array of 3 transaction IDs. The array must start with the lexicographically smallest transaction ID in the cycle, while preserving the directional order of the wait dependencies. (For example, if TX08 waits for TX02, TX02 waits for TX04, and TX04 waits for TX08, the normalized cycle is `["TX02", "TX04", "TX08"]`).
5. Sort all identified normalized cycles lexicographically.
6. Paginate the results: Take only the top 3 cycles from your sorted list.
7. Save the final output as a formatted JSON array of arrays to `/home/user/top_deadlocks.json`.

You may use any language available in the environment (e.g., Python, Bash, Perl) to write your analysis script.