You are a database administrator tasked with optimizing a broken query and performing graph analytics on the results.

In `/home/user/network.db` (a SQLite database), there are two tables:
1. `nodes` (`id` INTEGER, `name` TEXT, `region` TEXT)
2. `edges` (`source` INTEGER, `target` INTEGER, `weight` INTEGER, `timestamp` INTEGER)

A junior developer wrote a query saved at `/home/user/bad_query.sql`. It is supposed to find the single most recent connection (highest timestamp) for every pair of interacting nodes that belong to the *same region*. However, they used an implicit cross join without proper join conditions, resulting in an enormous Cartesian product, slow performance, and completely wrong aggregations.

Your task is to:
1. Write a corrected SQL query and save it to `/home/user/fixed_query.sql`. The query must use standard SQL `JOIN`s and a Window Function (like `ROW_NUMBER()`) to get the latest edge per source-target pair where both source and target have the identical `region`. The output columns must be: `source, target, weight, timestamp, region`.
2. Write a SQL script at `/home/user/indexes.sql` containing `CREATE INDEX` statements that would optimize your new query. Apply these indexes to the database.
3. Export the results of `fixed_query.sql` to a CSV file at `/home/user/recent_edges.csv` (include column headers).
4. Write and execute a Python script at `/home/user/graph_analytics.py` (you may only use the Python standard library, no third-party packages) that reads `/home/user/recent_edges.csv`, treats the data as an *undirected* unweighted graph (if A->B exists, A is connected to B and B is connected to A), and computes:
   - The shortest path (by number of hops) from node ID 1 to node ID 5.
   - The node ID with the highest degree centrality (most connections to unique nodes). If there's a tie, pick the lower ID.
5. The Python script must output these findings to `/home/user/report.json` with the exact format:
```json
{
    "shortest_path": [1, ..., 5],
    "max_degree_node": 123
}
```