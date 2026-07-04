You are a Database Reliability Engineer. We have a backup metadata tracking system backed by an SQLite database located at `/home/user/backup_meta.db`. 

There is a reporting script at `/home/user/report.py` that generates a CSV report of backup sizes. However, there are three major issues:

1. **Incorrect Results (Implicit Cross Join):** The current SQL query in the script is producing massive, incorrect backup sizes because of an implicit cross join between the `storage_nodes` and `backups` tables. 
2. **Missing Analytics:** Management wants the report to include a rolling average. You must modify the query to return `cluster_name`, `backup_id`, `size_bytes`, and a new column `rolling_avg_size`. The `rolling_avg_size` should be the average `size_bytes` of the current backup and up to 2 preceding successful backups *for that specific cluster*, ordered by `timestamp` ascending. Use a SQL window function.
3. **Missing Index:** The query is slow on our production system. Create a composite index named `idx_backup_perf` in the SQLite database to optimize joining `backups` to `storage_nodes` and filtering by `status = 'SUCCESS'`.

Additionally, we track incremental backups as a graph (each incremental backup points to its parent via `parent_backup_id`). You need to find the length (number of nodes) of the longest continuous chain of backups (A chain is a sequence of backups linked by `parent_backup_id`, starting from a FULL backup and following through its descendants). 
Write the integer length of this longest chain to `/home/user/longest_chain.txt`.

**Action Items:**
1. Fix the SQL query in `/home/user/report.py` to remove the cross join and add the `rolling_avg_size` window function. Ensure it filters for `status = 'SUCCESS'`.
2. Run the updated script and save its output to `/home/user/report_output.csv`. Ensure the output has the CSV header: `cluster_name,backup_id,size_bytes,rolling_avg_size`. Round `rolling_avg_size` to 2 decimal places in Python or SQL.
3. Connect to `/home/user/backup_meta.db` and create the index `idx_backup_perf`.
4. Determine the longest backup chain and write the integer count to `/home/user/longest_chain.txt`.