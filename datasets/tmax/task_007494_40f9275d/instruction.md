You are a Database Reliability Engineer (DBRE) investigating a complex backup restoration chain. 

We store all our backup metadata in a SQLite database located at `/home/user/backup_metadata.db`. Because we use incremental backups, any given backup might depend on a previous incremental backup, forming a dependency graph that eventually traces back to a full backup.

The database has a single table:
`backups (id INTEGER PRIMARY KEY, server_name TEXT, backup_type TEXT, parent_id INTEGER, size_bytes INTEGER, created_at DATETIME)`
- `backup_type` is either 'FULL' or 'INC' (incremental).
- `parent_id` is the ID of the backup this backup immediately depends on (NULL for 'FULL' backups).

Your task is to write a single-file Rust program `/home/user/get_chain.rs` that resolves the restoration chain for a specific backup using a recursive Common Table Expression (CTE) to traverse the graph. 

The Rust script must:
1. Use the `rusqlite` crate to connect to `/home/user/backup_metadata.db`.
2. Accept a single target `backup_id` as a command-line argument.
3. Execute a **parameterized query** (to prevent SQL injection) containing a recursive CTE that finds the target backup and traverses *up* the `parent_id` chain until it reaches the root 'FULL' backup.
4. Sort the resulting chain chronologically by `created_at` ASC (so the FULL backup is first, followed by the sequence of incrementals).
5. Print the results to standard output in the format `id,size_bytes` (one per line).

To complete the task:
1. Initialize a new Rust project or use `rustc` (with `rusqlite` available) to compile `/home/user/get_chain.rs`. You can create a Cargo project at `/home/user/backup_tool` to manage dependencies easily.
2. Run your compiled program for backup ID `15` and redirect the output to `/home/user/chain_15.log`.

Ensure that the output log contains only the requested comma-separated values.