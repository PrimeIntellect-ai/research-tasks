I am a researcher organizing a massive web of dataset derivations, and I need a tool to extract dataset lineage graphs. The data is currently stored in a local SQLite database at `/home/user/lineage.db`. 

I don't remember the exact schema, but it contains two tables: one for the datasets (with an ID, title, and format) and one for the relationships (edges) showing how datasets were derived from one another, including the operation type (like 'filter', 'join', etc.).

I need you to write a Go program located at `/home/user/export_lineage.go` that does the following:
1. Analyzes the schema of `/home/user/lineage.db` to understand the table and column names.
2. Accepts a command-line flag `-start` (an integer) representing the ID of the starting dataset.
3. Uses a parameterized recursive SQL query (CTE) to find the starting dataset and ALL of its downstream descendants (i.e., datasets derived from it, datasets derived from those, and so on).
4. Retrieves both the nodes (the datasets) and the edges (the derivation steps) for this specific subgraph.
5. Exports the result to a file named `/home/user/lineage_export.json` in the following precise JSON structure:

```json
{
  "nodes": [
    {"id": 1, "title": "Raw Sensor Data", "format": "csv"},
    {"id": 2, "title": "Cleaned Sensor Data", "format": "parquet"}
  ],
  "edges": [
    {"source": 1, "target": 2, "operation": "clean"}
  ]
}
```
*Note: The arrays can be in any order, but the keys must match exactly.*

To complete the task:
- Initialize a Go module in `/home/user/` if necessary and fetch the required SQLite driver (`github.com/mattn/go-sqlite3`).
- Write the Go code.
- Run your program with `-start 1` to generate `/home/user/lineage_export.json`.