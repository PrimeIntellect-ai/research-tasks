You are a data analyst working with network routing data. We have exported the latest network topology into two CSV files, but our previous system left some stale data in the extracts. 

Your task is to write a robust Bash script that builds an SQLite database from these CSVs, cleans the stale data, and performs a graph traversal using advanced SQL to find optimal routing paths.

**Input Data:**
1. `/home/user/nodes.csv`: Contains `node_id`, `node_name`.
2. `/home/user/edges.csv`: Contains `source_id`, `target_id`, `weight`, `is_stale`.

**Requirements:**
1. Create a Bash script at `/home/user/analyze_graph.sh` that accepts exactly two arguments: `START_NODE_NAME` and `MAX_HOPS`.
2. The script must initialize an SQLite database at `/home/user/routing.db`. If the database already exists, the script should cleanly overwrite or drop/recreate the tables to ensure idempotency.
3. Import the CSV files into tables named `nodes` and `edges`.
4. Stale data filtering: When querying the graph, completely ignore any edges where `is_stale = 1`. 
5. Graph Traversal: Using a Recursive CTE in SQLite, traverse the graph starting from the node with `node_name == START_NODE_NAME`. The traversal should explore paths up to `MAX_HOPS` depth (e.g., 1 hop means direct neighbors only). Edges are directed (`source_id` -> `target_id`).
6. Analytical Aggregation: Multiple paths may exist to the same destination. Using SQL Window Functions (`MIN()` over a partition, or `DENSE_RANK()`), calculate the minimum total weight to reach each reachable node. Rank the reachable destination nodes by their minimum total weight in ascending order.
7. Parameterized execution: The Bash script must safely pass the positional arguments (`$1` and `$2`) into the `sqlite3` CLI. 
8. The script must output the final result directly to standard output as a CSV (including headers) with the following exact columns: `destination_name,min_total_weight,rank`. Do not include the start node itself in the output unless there is a cycle back to it.
9. Validate the output format: Ensure there are no stray spaces in the headers and the CSV delimiter is a comma.

**Example execution:**
```bash
chmod +x /home/user/analyze_graph.sh
./analyze_graph.sh "Alpha" 3 > /home/user/output.csv
```

Your final output when the automated test runs `./analyze_graph.sh "Alpha" 3` must perfectly match the expected calculated graph traversal.