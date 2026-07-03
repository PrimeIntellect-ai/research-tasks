You are a Database Reliability Engineer managing a backup snapshot of a service dependency graph. The backup is stored as an SQLite database located at `/home/user/graph_backup.db`. 

The database has the following schema:
- `nodes` (id INTEGER PRIMARY KEY, name TEXT, node_type TEXT, status TEXT)
- `edges` (source_id INTEGER, target_id INTEGER, relation TEXT)

Due to the size of the graph, querying reverse dependencies is currently slow. Your tasks are:

1. **Optimize the Database**: Connect to `/home/user/graph_backup.db` and create an index named `idx_edges_target` on the `target_id` column of the `edges` table.

2. **Extract a Subgraph**: Write a Python script at `/home/user/extract.py` that takes exactly two command-line arguments: `relation` and `target_node_type`. 
   - The script must connect to the database and find all source nodes that have an edge with the specified `relation` to a target node of the specified `target_node_type`.
   - **Constraint**: You must use a parameterized SQL query in your Python script to prevent SQL injection when passing the command-line arguments.
   - The query should join `nodes` (source) -> `edges` -> `nodes` (target).

3. **Format and Export**: The Python script must export the results to a JSON file located at `/home/user/results.json`.
   - The JSON file must contain a list of dictionaries, each with exactly two keys: `"source_name"` and `"source_status"`.
   - The list must be alphabetically sorted by `"source_name"`.
   - Ensure there are no duplicate entries in the output.

4. **Execution**: Run your script to find all source nodes that have a `"depends_on"` relation to a target node of type `"storage"`.
   ```bash
   python3 /home/user/extract.py depends_on storage
   ```

Complete these steps so that the index is created in the database and the exact JSON output is generated at `/home/user/results.json`.