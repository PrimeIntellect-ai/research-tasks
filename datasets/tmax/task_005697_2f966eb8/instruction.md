You are a Database Reliability Engineer. We have a SQLite database at `/home/user/backup_metadata.db` that tracks our server hierarchy and backup history. 

Recently, an intern wrote a report generation script at `/home/user/generate_report.sh` that is meant to output the sizes of the latest successful backups for all our servers. However, it is currently producing a massive amount of incorrect data because the underlying SQL query contains an implicit cross join, lacks temporal filtering, and completely ignores the server dependency hierarchy.

Your task is to:

1. **Reverse Engineer & Fix**: Inspect the schema of `/home/user/backup_metadata.db`. You will find tables for `servers` and `backups`. Modify `/home/user/generate_report.sh` so that it queries the database correctly and outputs the results to `/home/user/final_report.csv`.

2. **Hierarchical Traversal & Windowing**: The fixed query executed by `/home/user/generate_report.sh` must:
   - Resolve the parent-child relationship in the `servers` table. Output the server's hostname and its parent's hostname. If the server has no parent, output 'ROOT' for the parent hostname.
   - Use a Window Function to select ONLY the most recent backup (by `timestamp`) that has a `status` of 'SUCCESS' for each server. 
   - The final CSV output (`/home/user/final_report.csv`) must contain exactly three columns: `hostname,parent_hostname,latest_backup_size_mb`.
   - Order the final CSV alphabetically by `hostname`.
   - Ensure the output has NO headers.

3. **Index Optimization**: The current database has no indexes other than primary keys. Write a separate Bash script at `/home/user/optimize.sh` that, when executed, adds a composite index named `idx_backups_latest` to the `backups` table. This index must be specifically designed to optimize the filtering and windowing operations on `server_id`, `status`, and `timestamp`.

Ensure both scripts (`generate_report.sh` and `optimize.sh`) are executable. You can test your scripts directly in the terminal to verify the output in `/home/user/final_report.csv`.