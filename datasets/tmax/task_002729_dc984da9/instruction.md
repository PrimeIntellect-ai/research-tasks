You are a data analyst investigating an information flow network. You have two CSV files representing a graph of communications: 
1. `/home/user/nodes.csv` with columns: `node_id`, `department`, `account_status`
2. `/home/user/edges.csv` with columns: `source_id`, `target_id`, `message_size`, `timestamp`

Your task is to write a Python script at `/home/user/analyze_graph.py` that processes this data to find specific indirect communication paths (2-hop paths: A -> B -> C). 

You must use Python's built-in `sqlite3` and `csv` modules to load the CSV data into an in-memory SQLite database and execute a single parameterized SQL query to find the paths.

The target paths must meet all of the following conditions:
1. Node A (the start) must belong to the 'Engineering' department and have an 'active' account_status.
2. Node C (the end) must belong to the 'Finance' department and have an 'active' account_status.
3. Node B (the intermediary) must have an 'inactive' account_status (representing a compromised or disabled relay account).
4. The total `message_size` of the path (size of A->B plus size of B->C) must be strictly greater than a threshold provided as a command-line argument.

Your script must:
1. Take exactly one command-line argument: the minimum total message size threshold (an integer).
2. Use parameterized queries for the size threshold to prevent SQL injection (do not use string formatting for the parameter).
3. Select the following columns for the output:
   - `start_node`: the `node_id` of A
   - `end_node`: the `node_id` of C
   - `total_size`: the sum of the message sizes
   - `latest_timestamp`: the maximum of the two edge timestamps
4. Order the results first by `latest_timestamp` descending, then by `total_size` descending.
5. Limit the results to the top 5 paths (pagination).
6. Export the final result to a CSV file at `/home/user/results.csv` including the header row.

For example, running:
`python3 /home/user/analyze_graph.py 50`
should generate `/home/user/results.csv` containing the top 5 paths matching the criteria with a total size > 50.