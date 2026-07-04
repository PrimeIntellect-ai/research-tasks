You are helping a researcher organize an academic dataset using a Rust tool. The dataset is stored in a SQLite database at `/home/user/citations.db`, which represents a graph of research papers.

The database has two tables:
- `papers(id INTEGER PRIMARY KEY, title TEXT)`
- `citations(source_id INTEGER, target_id INTEGER)`

There is a Rust project at `/home/user/dataset_manager`. It is supposed to perform two tasks, but both are currently incomplete or broken:

1. **Shortest Path Computation:** The `shortest_path` function in `src/main.rs` needs to be implemented. It should use a **Recursive CTE (Common Table Expression)** to find the shortest citation path (degrees of separation) between a `source_id` and a `target_id`. The traversal is directed (from `source_id` to `target_id`).
2. **Concurrency Deadlock:** The `run_concurrent_updates` function spawns two threads to process datasets. Currently, it often deadlocks or hits a "database is locked" error because SQLite's default journal mode doesn't handle concurrent readers and writers well. You need to fix this by modifying the database connection setup in the Rust code to use `PRAGMA journal_mode = WAL;` and adding a proper index strategy (an index on `citations(source_id, target_id)`) to optimize the graph traversal.

**Your objectives:**
1. Fix the deadlock issue in `/home/user/dataset_manager/src/main.rs` by setting the journal mode to WAL upon connection.
2. Complete the `shortest_path` function by writing an efficient recursive CTE in SQLite using `rusqlite`.
3. Create an index `idx_citations_source_target` on `citations(source_id, target_id)` directly in the database to speed up recursive traversals.
4. Run the compiled Rust program to find the shortest path from paper ID `10` to paper ID `42`. Save the standard output (just the integer representing the shortest path length) to `/home/user/path_result.txt`.
5. Run the concurrency test and save its output to `/home/user/concurrency_result.txt`.

Use the following commands to execute the Rust program once fixed:
- `cd /home/user/dataset_manager && cargo run -- path 10 42 > /home/user/path_result.txt`
- `cd /home/user/dataset_manager && cargo run -- test-concurrency > /home/user/concurrency_result.txt`