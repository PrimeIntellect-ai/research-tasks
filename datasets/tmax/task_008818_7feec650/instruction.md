You are a database administrator tasked with optimizing a graph traversal query for a network routing system. The routing topology is stored in an SQLite database located at `/home/user/routes.db`. 

The database contains a single table:
`edges (source TEXT, target TEXT, cost INTEGER)`

Currently, we use a recursive Common Table Expression (CTE) to find the lowest-cost paths to all reachable nodes from a given starting node, constrained by a maximum cost of 50. The query works, but `EXPLAIN QUERY PLAN` shows it is performing a full `SCAN TABLE edges` during the recursive step, which is inefficient.

Here is the base query:
```sql
WITH RECURSIVE paths(node, total_cost) AS (
    SELECT '{START_NODE}', 0
    UNION ALL
    SELECT e.target, p.total_cost + e.cost
    FROM paths p
    JOIN edges e ON p.node = e.source
    WHERE p.total_cost + e.cost <= 50
)
SELECT node, MIN(total_cost) as min_cost 
FROM paths 
GROUP BY node 
ORDER BY node;
```

Your task:
1. Identify the missing index that will optimize the `JOIN edges e ON p.node = e.source` step, converting the full table scan into an index search (ideally a covering index). Write the exact SQL statement to create this index into a file named `/home/user/optimize.sql`.
2. Apply your optimization to the `/home/user/routes.db` database.
3. Write a Bash script at `/home/user/get_reachable.sh` that takes a single starting node (e.g., 'A') as its first command-line argument (`$1`).
4. The script must execute the recursive CTE query against `/home/user/routes.db`, dynamically replacing `{START_NODE}` with the provided argument.
5. The script must output the results to standard output in the format `Node:Cost` (e.g., `B:15`), one per line, sorted alphabetically by node name. Use bash tools (like `awk`, `sed`, or `tr`) to format the raw SQLite output into the required `Node:Cost` format.

Ensure your Bash script is executable (`chmod +x`). 
Do not modify the table schema, only add the necessary index.