You are a Database Reliability Engineer managing a backup infrastructure. The backup schedules and their dependencies are stored as a directed graph in an SQLite database located at `/home/user/backups.db`. 

Recently, queries resolving backup dependencies have been returning stale results and executing very slowly. We suspect a poorly designed or corrupted index on the dependency table, as well as a need to properly materialize the graph to understand the blast radius of failures.

Your tasks are as follows:

1. **Fix the Index Strategy:**
   - Inspect the schema of the `deps` table (which has columns `parent_id` and `child_id`).
   - Identify the existing poorly-designed index on the `deps` table that is causing inefficient lookups for finding children of a given parent.
   - Write the name of this bad index to `/home/user/bad_index.txt`.
   - Drop this bad index and create a new, optimal index named `idx_deps_optimal` on `deps(parent_id, child_id)`.

2. **Graph Analytics (Centrality) via Bash:**
   - Write a Bash script at `/home/user/analyze_graph.sh` that uses `sqlite3` to calculate the "out-degree" (number of direct child dependencies) for each job.
   - You MUST use a SQL Window Function (`RANK() OVER ...`) to rank the jobs by their `child_count` in descending order.
   - Have the script output the Top 3 jobs to `/home/user/top_jobs.csv` in the exact format: `rank,job_name,child_count`. (e.g., `1,SystemDB,5`).
   - Ensure the script is executable and run it to generate the CSV.

3. **Graph Materialization:**
   - The root of all backups is the job named `SystemDB`.
   - Use a Recursive CTE in `sqlite3` to traverse the dependency graph starting from `SystemDB` and find all downstream jobs.
   - Materialize the paths by concatenating the job names separated by `->` (e.g., `SystemDB->AppDB->UserDB`).
   - Save these paths to `/home/user/backup_paths.csv` (one path per line, order does not matter).

Ensure all requested output files (`bad_index.txt`, `analyze_graph.sh`, `top_jobs.csv`, `backup_paths.csv`) exist and have the correct permissions/formats.