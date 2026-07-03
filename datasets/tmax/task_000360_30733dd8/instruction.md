You are a Database Reliability Engineer investigating a corrupted backup tracking database. 

We have a local SQLite database at `/home/user/backups.db` that tracks our incremental backup jobs. It contains two tables:
1. `jobs`: Columns are `id` (INTEGER PRIMARY KEY), `status` (TEXT), and `size_mb` (INTEGER).
2. `dependencies`: Columns are `parent_id` (INTEGER) and `child_id` (INTEGER). This represents the backup chain (a child incremental backup depends on its parent).

Due to a recent index corruption and application bug, the `dependencies` table contains circular references (cycles), which is causing our standard reporting tools to hang in infinite loops. 

Your task is to write a Python script (`/home/user/analyze_backups.py`) that calculates the total size of a specific backup chain while safely bypassing the corruption. 

Requirements for your script:
1. Connect to `/home/user/backups.db` using Python's built-in `sqlite3` module.
2. Traverse the dependency graph starting from the root backup job, which is `id = 1`. You need to find all jobs that are descendants of job `1` (including job `1` itself).
3. Safely handle the circular references so your traversal does not get stuck in an infinite loop. You may do this using SQLite's advanced CTE features or in Python application logic.
4. Filter the reachable jobs to only those where `status = 'SUCCESS'`.
5. Calculate the sum of `size_mb` for these successful, reachable unique jobs.
6. Write the final integer sum to a file located precisely at `/home/user/total_successful_backup_size.txt`.

Ensure your script runs successfully and writes only the final aggregated integer to the text file.