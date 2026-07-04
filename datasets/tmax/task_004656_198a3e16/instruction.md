You are a Database Reliability Engineer investigating backup performance and failures. You have been given an undocumented SQLite database located at `/home/user/backups.db` which contains historical backup execution data.

Your task is to analyze this database to extract performance metrics and trace failure dependencies. Since the database schema is completely undocumented, you will first need to reverse-engineer its structure.

Perform the following tasks:

1. **Top Longest Successful Backups**: 
   Find the top 2 longest-running `SUCCESS`ful backup jobs for each server using analytical window functions.
   Write the results to `/home/user/top_longest.csv`.
   - Format: `hostname,job_id,duration_sec` (no header row)
   - Sorting: alphabetical by `hostname` ascending, then by duration descending.

2. **Dependency Tracing**:
   Backup job `14` failed, and you need to find all upstream backup jobs that it depends on, either directly or indirectly (i.e., the entire dependency graph leading to job 14).
   Write the results to `/home/user/upstream_dependencies.txt`.
   - Format: A single line of comma-separated job IDs.
   - Sorting: strictly numerically ascending.

You may use any bash scripts or interactive `sqlite3` queries to achieve this. The final files must exactly match the specified formats.