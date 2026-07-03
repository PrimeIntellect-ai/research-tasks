You are a data engineer building an ETL pipeline to analyze system architecture dependencies. 

You have been provided with a SQLite database at `/home/user/system.db` containing two tables:
1. `services` (id INTEGER, name TEXT)
2. `dependencies` (service_id INTEGER, depends_on_id INTEGER)

Your objective is to identify all "hidden" 2-hop dependencies and materialize them into a JSON graph projection. A "hidden" 2-hop dependency occurs when Service A depends on Service B, and Service B depends on Service C, but Service A does NOT directly depend on Service C.

Perform the following tasks:
1. Write a SQL query (saved as `/home/user/query.sql`) that extracts these hidden 2-hop dependencies. The query must return exactly two columns: `source` (the name of Service A) and `target` (the name of Service C). 
2. Write a Go program (saved as `/home/user/build_graph.go`) that reads tab-separated values (the output of your SQL query) from Standard Input (stdin). The Go program must materialize this data into a JSON array of objects, where each object represents a directed edge in the graph.
3. Write a bash script (saved as `/home/user/run_etl.sh`) that chains these tools together: it should execute the SQL query against `system.db` using the `sqlite3` CLI tool, pipe the output directly into your Go program, and redirect the final JSON output to `/home/user/graph_projection.json`.

Constraints and Output Format:
- The final JSON array in `/home/user/graph_projection.json` must have objects with exactly two keys: `"source"` and `"target"`.
- The array must be deduplicated (if there are multiple 2-hop paths between A and C, only list A -> C once).
- The array must be sorted alphabetically by `source`, and then by `target`.
- Do not use third-party Go libraries; use only the standard library.

Example JSON output format:
```json
[
  {
    "source": "api_gateway",
    "target": "database"
  }
]
```

Ensure that running `bash /home/user/run_etl.sh` successfully generates the correct `/home/user/graph_projection.json` file.