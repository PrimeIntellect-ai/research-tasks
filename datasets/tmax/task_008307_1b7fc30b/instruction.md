You are an AI assistant helping a researcher organize and process a dataset stored in a SQLite database. 

The database `/home/user/research.db` contains a knowledge graph of concepts and their temporal metrics. It has three tables:
- `nodes` (`id` TEXT PRIMARY KEY, `type` TEXT)
- `edges` (`source` TEXT, `target` TEXT, `relation` TEXT)
- `metrics` (`node_id` TEXT, `score` REAL, `recorded_at` DATETIME)

Recently, the database suffered a partial corruption. The index `idx_metrics_node` on the `metrics` table is completely corrupted and returns stale or missing rows if the SQLite query planner decides to use it. 

Your task is to write a Go program at `/home/user/process.go` that does the following:
1. Connects to `/home/user/research.db` (you may use `github.com/mattn/go-sqlite3` and initialize a module in `/home/user`).
2. Bypasses the corrupted index. You MUST either execute `DROP INDEX IF EXISTS idx_metrics_node;` before querying, or use the `NOT INDEXED` clause in your `SELECT` statements.
3. Performs a query to find all nodes that are targeted by a `depends_on` relation originating from the node with `id = 'ROOT'`.
4. For each of these target nodes, retrieves their `metrics` and calculates the cumulative sum of their `score` ordered chronologically by `recorded_at`. You must compute this using a SQL Window Function (`SUM(...) OVER (...)`).
5. Implements a schema validation/filtering step in Go: completely discard any resulting record where the calculated cumulative score is strictly less than `0.0`.
6. Writes the final filtered records to `/home/user/results.json` as a cleanly formatted JSON array of objects. 

The JSON objects must strictly follow this schema:
```json
[
  {
    "node_id": "string",
    "recorded_at": "YYYY-MM-DD",
    "cumulative_score": 12.5
  }
]
```
The output array must be sorted alphabetically by `node_id` ascending, and then by `recorded_at` ascending.

Complete the Go script, ensure it compiles, and execute it so that `/home/user/results.json` is generated successfully.