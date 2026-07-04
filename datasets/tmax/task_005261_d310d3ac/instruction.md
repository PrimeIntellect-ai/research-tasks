You are a data engineer building an ETL pipeline to analyze a hierarchical graph of system components.

I have an SQLite database located at `/home/user/graph.db` containing a single table `components` with the following schema:
`id` (INTEGER PRIMARY KEY), `parent_id` (INTEGER), `name` (TEXT), `base_cost` (INTEGER), and `type` (TEXT).

The `parent_id` creates a tree-like hierarchy (graph) of components. A previous script attempted to calculate the total cost of each component by joining the table to itself, but it used an implicit cross join and returned astronomically wrong results.

Your task is to write a single Bash script at `/home/user/generate_report.sh` that uses `sqlite3` to query `/home/user/graph.db` and accurately extracts the data into a JSON file at `/home/user/report.json`.

The query executed by your script must:
1. Use a **Recursive CTE** to calculate the `total_cost` for every component. A component's `total_cost` is its own `base_cost` PLUS the `base_cost` of ALL its descendants (children, grandchildren, etc.).
2. Use a **Window Function** to calculate a `cost_rank` for each component. The rank should order components by their `total_cost` in DESCENDING order, partitioned by their `type`.
3. Select the `id`, `name`, `type`, `total_cost`, and `cost_rank`.
4. Order the final results by `id` ASC.
5. Export the query result as a strictly valid JSON array of objects.

Output requirements:
- The output file must be saved to `/home/user/report.json`.
- The output must be a valid JSON array containing objects with the exact keys: `id`, `name`, `type`, `total_cost`, and `cost_rank`.

Ensure your script `/home/user/generate_report.sh` is executable (`chmod +x`). You can test it by running it and inspecting the resulting JSON file.