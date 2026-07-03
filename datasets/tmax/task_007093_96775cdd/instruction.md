You are acting as a database administrator for a software analytics company. We have an SQLite database located at `/home/user/components.db` that contains a dependency graph of software components.

The database has two tables:
1. `nodes(id TEXT PRIMARY KEY, type TEXT, cost REAL)`
2. `edges(source TEXT, target TEXT)` - representing a directed dependency from `source` to `target`.

We frequently need to calculate the total downstream cost of specific components, grouped by their component type. Currently, this process is slow and not standardized.

Your task is to write a Python script at `/home/user/optimize_and_export.py` that does the following:
1. Connects to `/home/user/components.db`.
2. Creates the optimal index(es) on the `edges` table to speed up recursive forward-traversal queries (finding targets for a given source).
3. Uses a single SQL query with a Recursive CTE to find all downstream dependencies (transitive closure) starting from the node with id `'ROOT_01'`. The query should traverse from `source` to `target`.
4. Exclude the starting node `'ROOT_01'` from the aggregated results.
5. Aggregate the total `cost` of all discovered downstream dependencies, grouped by their `type`. Also count the total number of downstream nodes discovered.
6. Export the aggregated results to `/home/user/summary.json` with the exact following structure:
```json
{
  "total_downstream_nodes": <integer>,
  "cost_by_type": {
    "<type_1>": <float>,
    "<type_2>": <float>
  }
}
```

Ensure your Python script actually executes these steps when run. Run your script to produce the output file.