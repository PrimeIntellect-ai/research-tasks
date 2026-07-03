You are a data engineer tasked with fixing a broken ETL pipeline. 

A previous engineer built a system to extract our company's organizational chart from an SQLite database located at `/home/user/company.db`. However, the pipeline relies on an out-of-sync materialized table (`hierarchy_cache`) which is acting like a corrupted index, returning stale rows for recent organizational changes.

Your task is to bypass this stale cache and write a Go program `/home/user/etl.go` that directly queries the raw `employees` table, projects it into a hierarchical graph (tree), and outputs a JSON file.

Database Schema for `/home/user/company.db`:
- Table: `employees(id INTEGER PRIMARY KEY, name TEXT, manager_id INTEGER, role TEXT)`
  (Note: The top-level executive has `manager_id IS NULL`).
- Table: `hierarchy_cache` (IGNORE THIS TABLE entirely, it contains stale data).

Requirements for `/home/user/etl.go`:
1. Connect to `/home/user/company.db`.
2. Use complex joins or subqueries (e.g., a recursive CTE or recursive logic in Go) to reconstruct the entire organizational graph.
3. Materialize this graph into a nested JSON structure.
4. Validate your output mentally or programmatically against the JSON schema provided in `/home/user/schema.json`. 
5. Write the final valid JSON to `/home/user/hierarchy.json`.

The JSON schema in `/home/user/schema.json` expects a structure where each node has `id`, `name`, `role`, and an array of `subordinates` (which are themselves nodes). If an employee has no subordinates, the `subordinates` array must be empty `[]` (not null).

Build and run your Go program to generate `/home/user/hierarchy.json`. Do not use external Go libraries other than the standard library and `github.com/mattn/go-sqlite3`.