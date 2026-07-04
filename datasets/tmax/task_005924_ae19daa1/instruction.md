You are a database administrator tasked with optimizing a graph traversal query and implementing a data pipeline in Rust.

We have a SQLite database located at `/home/user/graph_tool/graph.db` containing a single table:
`CREATE TABLE edges (source TEXT, target TEXT);`

This table represents a directed graph. Your objectives are:

1. **Index Strategy**: The database currently has no indexes. Identify the optimal index to speed up forward graph traversal (finding targets for a given source) and create this index in the database.
2. **Recursive Graph Traversal**: Write a Rust program in the pre-existing Cargo project at `/home/user/graph_tool/` that connects to `graph.db`. Use a Recursive Common Table Expression (CTE) in SQL to compute the shortest path from the node named `"START"` to the node named `"END"`. 
3. **Output Schema Validation**: The Rust program must execute the query, extract the shortest path, and write the output to `/home/user/graph_tool/output.json` exactly matching this JSON schema:
```json
{
  "path": ["START", "node1", "node2", "END"],
  "hops": 3
}
```
(`hops` is the number of edges traversed. If the path has 4 nodes, hops is 3).

**Requirements**:
- The Cargo project at `/home/user/graph_tool/` has already been created with `rusqlite` and `serde_json` dependencies. You just need to modify `src/main.rs` and run it.
- Your SQL query *must* use a recursive CTE (`WITH RECURSIVE`) to find the path.
- Produce the final valid JSON file at `/home/user/graph_tool/output.json`.
- Do not modify the existing data in the `edges` table.