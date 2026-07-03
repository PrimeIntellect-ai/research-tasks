You are a database reliability engineer managing a complex backup system. Your team stores backup metadata in a SQLite database at `/home/user/backups.db`. The database tracks backup jobs and their dependency graph (e.g., incremental backups depending on previous backups).

A colleague wrote a Python script at `/home/user/buggy_export.py` to extract the dependency chain for a specific full backup (`DB_PROD_FULL`) and calculate the running total size of the backups in the chain over time. However, the script is currently running out of memory and returning incorrect results because the recursive SQL query contains an implicit cross join (missing join conditions) in its recursive step.

Your task is to:
1. Fix the SQL query in `/home/user/buggy_export.py`. The recursive CTE must correctly traverse the `backup_deps` table to find all descendants of the `DB_PROD_FULL` backup.
2. Maintain the window function that calculates the `running_total` of the `size` ordered by `created_at`.
3. Ensure the script exports the final results as a JSON array of objects to `/home/user/fixed_metrics.json`.
4. Each object in the exported JSON must have exactly the following keys: `id` (integer), `job_name` (string), `size` (integer), and `running_total` (integer).
5. Run the script to generate the output file.

Do not change the starting node (`DB_PROD_FULL`). Fix the joins in the recursive CTE so it properly links `backups`, `backup_chain`, and `backup_deps`.