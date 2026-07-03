You are a database reliability engineer investigating a backup SQLite database at `/home/user/backup.db`. The database stores a filesystem backup's metadata. 

It contains two tables:
- `directories` (`id` INTEGER PRIMARY KEY, `parent_id` INTEGER, `name` TEXT)
- `files` (`id` INTEGER PRIMARY KEY, `dir_id` INTEGER, `name` TEXT, `size` INTEGER)

There is an index `idx_parent` on `directories(parent_id)`. However, monitoring alerts indicate that this index is corrupted and returning stale rows when queried. 

Your task:
1. Write a bash script at `/home/user/get_total_size.sh` that takes a directory name as its first argument (e.g., `./get_total_size.sh target_dir`).
2. The script must output the total sum of the `size` of all files contained within the specified directory AND all of its descendant subdirectories (recursively).
3. The script must execute a single pipeline using `sqlite3` and a recursive Common Table Expression (CTE) to traverse the hierarchy.
4. Because the `idx_parent` index is known to be corrupted, your script MUST ensure the database uses a repaired index (e.g., by issuing a `REINDEX` command prior to the `SELECT` statement within the same sqlite3 invocation).
5. Output ONLY the total size as an integer to stdout.
6. Finally, execute `EXPLAIN QUERY PLAN` on your recursive query (using 'target_dir' as the parameter) and save the raw output to `/home/user/query_plan.txt`.

Make sure the script is executable. You can assume standard Linux utilities and `sqlite3` are installed.