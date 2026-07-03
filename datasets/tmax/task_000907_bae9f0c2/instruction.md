You are a Database Reliability Engineer responding to an incident involving a corrupted backup of a specialized file storage system. 

We have an SQLite database backup located at `/home/user/backup.db`. The database contains a single table `fs_nodes` representing a file system hierarchy. Due to a known bug in our old storage engine, the index `idx_stale_size` on this table is corrupted and causes queries to return stale, duplicate, or missing rows if the query optimizer uses it.

Your task is to write a C program `/home/user/analyze_backup.c` that connects to this SQLite database, safely bypasses or removes the corrupted index, and computes storage analytics using advanced SQL.

The table schema is:
`fs_nodes(id INTEGER PRIMARY KEY, parent_id INTEGER, name TEXT, size INTEGER)`
(If `size` is 0 or NULL, it's a directory. `parent_id` is NULL for the root).

Your C program must:
1. Include the SQLite3 header (`sqlite3.h`) and link against the sqlite3 library (`-lsqlite3`).
2. Ensure the corrupted index `idx_stale_size` is not used (e.g., by dropping it before running your main query).
3. Execute a single query (using `WITH RECURSIVE` and window functions) that:
   - Calculates the **total recursive size** of each node (the size of the node itself plus the total sizes of all its descendants).
   - Assigns a **rank** to each node based on its total recursive size in descending order (largest total size gets rank 1). If there is a tie, order by `id` ascending.
4. Output the results to a JSONLines file at `/home/user/analytics.jsonl`. Each line must represent a node in the following exact JSON format:
   `{"id": <node_id>, "name": "<node_name>", "total_size": <calculated_total_size>, "rank": <calculated_rank>}`

Compile your program to `/home/user/analyze_backup` and run it to produce the `analytics.jsonl` file.

Constraints:
- Use standard C.
- You must write the logic using SQL CTEs (Recursive) and Window Functions (`RANK() OVER ...`) executed via the SQLite C API. 
- Ensure your JSON output strictly matches the requested keys and types.