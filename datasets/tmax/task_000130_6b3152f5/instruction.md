You are a database administrator dealing with performance issues. A poorly written Python script has been locking up the system because it uses multiple nested loops and hundreds of individual queries to traverse a graph of transactions and calculate rolling statistics. This simulated deadlock scenario requires rewriting the logic into a single, efficient, parameterized SQL query.

An SQLite database is located at `/home/user/network.db`. It contains a graph of financial entities and their relationships:
- Table `entities` (`id` TEXT PRIMARY KEY, `type` TEXT, `region` TEXT)
- Table `transfers` (`source_id` TEXT, `target_id` TEXT, `amount` REAL, `timestamp` INTEGER)

Your task is to write a highly optimized Python script at `/home/user/analyze.py` that takes three command-line arguments: `region_name`, `limit`, and `offset`.

The script must connect to `/home/user/network.db` and execute a **single parameterized SQL query** that performs the following:
1. **Graph Traversal (Filtering & Joins):** Finds all "target" entities that are exactly 1 or 2 hops away (via the `transfers` table) from any entity in the given `region_name`. 
2. **Analytical Aggregation & Window Functions:** For each reached entity, calculate its `total_received` (sum of all transfer amounts where it is the target, across the entire database, not just the traversed paths). Then, use a SQL Window Function to assign a `regional_rank` to each reached entity, ranking them by `total_received` (descending) partitioned by their `region`. (If there is a tie, order by `id` ascending).
3. **Sorting and Pagination:** Order the final result by `regional_rank` ascending, then `id` ascending. Apply the `limit` and `offset` parameters directly in the SQL query.

The Python script must write the result to `/home/user/output.json` as a JSON array of dictionaries with the exact keys:
`[{"id": "entity_id", "type": "entity_type", "region": "entity_region", "total_received": 123.45, "regional_rank": 1}, ...]`

Constraints:
- You must use SQLite's CTEs (Common Table Expressions) or recursive CTEs for the graph traversal.
- You must use a Window Function (`RANK()` or `DENSE_RANK()`) for the ranking.
- Do not process the logic in Python; Python must only execute the query and dump the JSON.
- Use parameterized queries (`?` or named parameters) to prevent SQL injection and query plan caching issues.