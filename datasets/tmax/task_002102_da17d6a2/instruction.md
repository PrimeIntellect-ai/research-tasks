You are a data engineer tasked with repairing and completing an ETL pipeline. 

We have an SQLite database at `/home/user/source.db` containing an event log of graph edge mutations. The table schema is:
`events (id INTEGER PRIMARY KEY, source_node INTEGER, target_node INTEGER, event_time DATETIME, action TEXT)`
The `action` column contains either `'ADD'` or `'REMOVE'`. 

There are two major issues you need to fix:
1. **Database Repair & Optimization:** The database contains an index named `idx_corrupt_source` that is known to return stale or corrupted pages. Drop this index. Then, design and create a new covering index named `idx_events_optimized` that will optimally support the analytical query you need to write next.
2. **Rust ETL Pipeline:** Create a Rust project at `/home/user/etl_project`. Write a program that reads from `/home/user/source.db` and materializes the current state of the graph.
   - Use a **Window Function** in your SQL to determine the latest state of each edge. An edge currently exists if its most recent event (ordered by `event_time` DESC, then `id` DESC) has the action `'ADD'`.
   - Your Rust program must use **parameterized queries** and **pagination** (fetching in chunks of exactly 50 rows at a time using `LIMIT` and `OFFSET`) to process the valid edges.
   - Materialize the final projected graph by writing it to `/home/user/active_graph.json`. The JSON format must be an object where each key is a `source_node` (as a string) and its value is an array of active `target_node`s (integers), **sorted in ascending order**. Only include source nodes that have at least one active target node.

Requirements:
- Ensure your Rust project compiles successfully using standard Cargo commands.
- You must execute your Rust program so that `/home/user/active_graph.json` is generated.
- Ensure the new index is physically present in the SQLite database.
- Use `rusqlite` and `serde_json` in your Rust project.