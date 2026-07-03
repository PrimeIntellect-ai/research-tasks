You are a database administrator tasked with optimizing and analyzing a Knowledge Graph of an IT infrastructure. The graph is stored in a SQLite database at `/home/user/infra_graph.db`. Due to environment constraints, you must use standard `sqlite3` commands orchestrated via Bash to perform graph operations.

The database contains two tables:
- `Nodes` (id TEXT PRIMARY KEY, label TEXT, name TEXT)
- `Edges` (source TEXT, target TEXT, type TEXT)

The labels include 'Service', 'Database', and 'Server'. The edge types include 'DEPENDS_ON' and 'HOSTED_ON'.

Currently, the queries are too slow. Your task is to write a Bash script at `/home/user/analyze_graph.sh` that takes the database path as its first argument and performs the following operations in order:

1. **Graph Projection & Materialization:**
   Create a materialized view (a new table) named `ServiceDependencyGraph` containing only edges where the `type` is 'DEPENDS_ON' and both the source and target nodes have the label 'Service'. The table should have columns: `source`, `target`.

2. **Index Strategy Design:**
   Create an optimal index (or indexes) on `ServiceDependencyGraph` to explicitly speed up forward graph traversal (finding targets given a source). 

3. **Knowledge Graph Pattern Matching:**
   Write a query to find all unique `Service` node names that directly 'DEPENDS_ON' a `Database` node, which in turn is 'HOSTED_ON' a `Server` named "srv-core-01". 
   Append the alphabetically sorted list of these Service names to `/home/user/output.log` (one name per line). Prefix this section with `--- Pattern Match ---`.

4. **Shortest Path Computation:**
   Using a Recursive CTE on the optimized `ServiceDependencyGraph` table, compute the shortest path length (number of edges) from the Service node named "GatewayAPI" to the Service node named "PaymentProcessor".
   Assume node `id` and `name` are identical for 'Service' nodes in this specific dataset.
   Append the single integer result to `/home/user/output.log`. Prefix this section with `--- Shortest Path ---`.

Requirements:
- Your script `/home/user/analyze_graph.sh` must be executable (`chmod +x`).
- Do not hardcode the expected answers; your script must query the database dynamically.
- The output in `/home/user/output.log` must precisely match the requested format.