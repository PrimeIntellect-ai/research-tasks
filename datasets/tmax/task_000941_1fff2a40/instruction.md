You are a Database Reliability Engineer (DBRE) tasked with analyzing a fragmented backup catalog. 

The metadata for all database backups is stored in an SQLite database located at `/home/user/backup_catalog.db`. Due to recent migrations, the database contains a mix of relational data, hierarchical (graph-like) parent-child backup chains, and document-based (JSON) configuration records.

Here is the schema of the database:
- Table `jobs`:
  - `id` (INTEGER PRIMARY KEY)
  - `parent_id` (INTEGER, NULL if it's a root/full backup, or references the `id` of its immediate parent backup)
  - `size_bytes` (INTEGER)
  - `status` (TEXT)
  - `start_time` (TIMESTAMP)
- Table `configs`:
  - `job_id` (INTEGER PRIMARY KEY)
  - `settings` (TEXT, contains a JSON string with configuration parameters)

Your task is to write a Python script that analyzes this SQLite database and generates a specific paginated CSV report of "long term" backup chains. 

Follow these specific processing requirements:
1. **Filtering (Cross-Representation):** Parse the JSON `settings` column in the `configs` table. You must only process backup chains where the **root** backup job (the job where `parent_id` is NULL) has `"retention_policy": "long_term"` in its JSON settings. Ignore all chains where the root job does not have this exact key-value pair.
2. **Graph Mapping & Analytical Aggregation:** For each valid root job, reconstruct its entire incremental backup chain (the root job, its children, its children's children, etc.). Calculate:
   - `root_job_id`: The ID of the root backup.
   - `total_chain_size_bytes`: The sum of `size_bytes` for the root job AND all its recursive descendants.
   - `num_incrementals`: The total count of descendants (excluding the root job itself).
   - `avg_incremental_size_bytes`: The average size of the descendants in bytes. If there are no incrementals, this should be `0.00`. Round this value to exactly 2 decimal places.
3. **Sorting & Pagination:** Sort the resulting valid chains by `total_chain_size_bytes` in descending order. If there is a tie, sort by `root_job_id` in ascending order. From this sorted list, implement pagination with a page size of 2. You need to extract exactly **Page 2** (meaning the 3rd and 4th items in the sorted list, 1-indexed).
4. **Output:** Write the paginated results to a CSV file at `/home/user/long_term_backup_report.csv`. The CSV must have exactly the following headers in this order: `root_job_id,total_chain_size_bytes,num_incrementals,avg_incremental_size_bytes`.

You may create any intermediate scripts or files to accomplish this. Do not use external Python libraries requiring `pip install` (only use standard library modules like `sqlite3`, `json`, `csv`). Ensure the final CSV file exists at the exact path specified.