You are a database administrator tasked with optimizing queries and cleaning up data discrepancies in a graph database system.

We are migrating our edge data from a NoSQL JSON document format to a relational SQLite database. During the migration, a corrupted process resulted in "stale" or orphaned edges in the SQLite database that do not exist in the source-of-truth JSON file. These stale edges are causing recursive graph traversals to return incorrect paths, and the current SQLite queries are performing poorly due to a lack of indexes.

You have been provided a pre-initialized Rust project at `/home/user/graph_project/` with `rusqlite` and `serde_json` dependencies included in the `Cargo.toml`. 

Your tasks are to:
1. Write a Rust program in `/home/user/graph_project/src/main.rs` that:
   - Connects to the SQLite database located at `/home/user/data/graph.db`.
   - Reads the source-of-truth JSON file at `/home/user/data/truth_edges.json`.
   - Compares the `edges` table in the database (which has columns `id`, `source`, `target`) with the JSON array (which contains objects with `id`, `source`, `target`).
   - Identifies the `id`s of the "stale" edges present in the SQLite database but missing from the JSON file.
   - Writes the IDs of these stale edges to `/home/user/stale_edges.txt`, one ID per line, sorted in ascending order.
2. Compile and run your Rust program to generate the `/home/user/stale_edges.txt` file.
3. Create a SQL script at `/home/user/optimize.sql` containing exactly two SQL statements (separated by a semicolon):
   - A `DELETE` statement that removes the stale edges from the `edges` table.
   - A `CREATE INDEX` statement that creates an index named `idx_edges_src_tgt` on the `source` and `target` columns (in that order) of the `edges` table to optimize future graph traversal queries.

Make sure your Rust code correctly maps the document representation to the relational data. All output files must be placed exactly at the paths specified.