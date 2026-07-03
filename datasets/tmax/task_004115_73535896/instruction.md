You are a Database Reliability Engineer (DBRE) tasked with managing a complex backup catalog. We recently had a catastrophic failure, and the handover from the previous shift was left as an audio voice memo.

1. **Analyze the Handover:**
   An audio file is located at `/app/handover.wav`. Use any available command-line tools (like `ffmpeg`, Python, or a transcription tool you can install) to determine the exact affected database name and the critical failure timestamp mentioned in the recording.

2. **Understand the Backup Catalog:**
   You have a SQLite database at `/app/catalog.db` with the following schema:
   - `databases (name VARCHAR PRIMARY KEY)`
   - `dependencies (db_name VARCHAR, depends_on VARCHAR)` - Represents foreign key/logical dependencies. If A depends on B, B must be restored BEFORE A.
   - `backups (id INTEGER PRIMARY KEY, db_name VARCHAR, type VARCHAR, timestamp INTEGER, filepath VARCHAR)` - `type` is either 'F' (Full) or 'I' (Incremental).

3. **Build the Restoration Planner:**
   Write a Rust CLI application that calculates the optimal, exact sequence of backup files to restore. 
   - The program must be compiled to `/home/user/restore_planner`.
   - It must accept exactly two positional arguments: `<target_db_name>` and `<target_timestamp>`.
   - It must output a plain-text list of `filepath`s to standard output, one per line, representing the correct restoration sequence.
   
   **Restoration Logic:**
   - You must restore the `target_db_name` and *all* of its upstream dependencies (recursive).
   - The restoration order among databases must be a valid topological sort (dependencies restored before the databases that depend on them). Tie-break alphabetically by database name if multiple independent databases can be restored.
   - For each database, find the latest Full ('F') backup where `timestamp <= target_timestamp`.
   - Then, find all Incremental ('I') backups for that database where the timestamp is strictly greater than the Full backup's timestamp, and `<= target_timestamp`.
   - The files for a single database must be ordered chronologically (Full first, then Incrementals in ascending timestamp order).

Ensure your Rust program handles complex joins, recursive queries (or equivalent application-level graph projection), and window functions properly to resolve this. We will heavily test your compiled `/home/user/restore_planner` binary against many random combinations of databases and timestamps to ensure your logic is strictly equivalent to our internal oracle.