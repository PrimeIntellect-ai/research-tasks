You are a Database Reliability Engineer. We have an SQLite database containing metadata for our backup systems located at `/home/user/backup_catalog.db`. The system tracks full and incremental backups, which form a hierarchical dependency tree.

The database has a single table:
`backups` (
    `backup_id` TEXT PRIMARY KEY,
    `parent_id` TEXT, -- References backup_id. NULL for full backups.
    `backup_type` TEXT, -- 'full' or 'incremental'
    `status` TEXT, -- 'success' or 'failed'
    `size_bytes` INTEGER
)

Your task is to analyze these backup chains and optimize the querying process:

1. **Optimize the Schema**: The current database has no secondary indexes. Design and create the most efficient index(es) on the `backups` table to speed up hierarchical traversals (finding children of a given parent, filtering by status). Apply this index directly to `/home/user/backup_catalog.db`.

2. **Calculate Chain Sizes**: Write a Python script `/home/user/analyze_backups.py` that uses a **Recursive CTE** (Common Table Expression) to calculate the total size of each successful backup chain. 
   - A backup chain starts with a 'full' backup (`parent_id` IS NULL and `status` = 'success').
   - It includes all connected 'incremental' descendants that also have `status` = 'success'. 
   - If a backup in the chain failed, it and all of its descendants are excluded from the chain.
   - Sum the `size_bytes` for the full backup and all its valid descendants.

3. **Outputs**:
   - Execute your Python script to generate a JSON file at `/home/user/chain_sizes.json` containing a dictionary mapping the `backup_id` of each full backup to its total calculated chain size (integer).
   - Generate the SQLite query execution plan for your optimized Recursive CTE query using `EXPLAIN QUERY PLAN`. Save the output text to `/home/user/query_plan.txt`.

Ensure your script connects to `/home/user/backup_catalog.db` and performs these operations efficiently.