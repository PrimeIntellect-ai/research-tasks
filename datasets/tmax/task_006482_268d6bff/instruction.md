You are an AI assistant helping a data researcher analyze a complex dataset provenance network. The researcher has a large number of datasets that are derived from one another over time. 

You have been provided with two CSV files in your home directory (`/home/user/`):
1. `datasets.csv`: Contains metadata about each dataset. (Columns: `id`, `name`, `size_mb`)
2. `derivations.csv`: Contains the directed edges representing how datasets are derived from one another. (Columns: `source_id`, `target_id`, `processing_time_mins`)

Your task is to organize this data into a SQLite database, optimize it for graph traversal, and then write a Bash script to perform a cross-query aggregation summarizing the shortest derivation paths.

Perform the following steps:

**Phase 1: Database Setup and Index Strategy**
1. Write a bash script named `/home/user/init_db.sh` that creates a SQLite database at `/home/user/provenance.db`.
2. The script must import `datasets.csv` into a table named `datasets` and `derivations.csv` into a table named `derivations`.
3. The script must create optimal indexes on the `derivations` table to ensure fast graph traversal (specifically indexing the columns used for joining source and target IDs).

**Phase 2: Graph Traversal & Aggregation**
1. Write a bash script named `/home/user/analyze_provenance.sh` that executes a SQL query against `/home/user/provenance.db` using the `sqlite3` command-line tool.
2. The query must use a Recursive Common Table Expression (CTE) to traverse the derivation graph starting from the root dataset (`id = 1`). Depth at the root is 0, and total processing time is 0.
3. For every dataset reachable from the root, determine the **shortest total processing time** to reach it. If there are multiple paths to the same dataset, keep only the one with the minimum accumulated `processing_time_mins` from the root. Also, record the `depth` (number of hops) of that optimal path. (If multiple paths tie for the shortest processing time, keep the one with the smallest depth).
4. Aggregate the results by `depth`. For each depth level, calculate:
   - `total_size_mb`: The sum of `size_mb` of all datasets at that optimal depth.
   - `avg_processing_time`: The average of the minimum total processing times for datasets at that depth, rounded to 1 decimal place.
5. The script must output the final aggregated results to `/home/user/provenance_summary.csv` with the exact header `depth,total_size_mb,avg_processing_time`.

Ensure your scripts are executable. The final output must be exactly formatted as a standard CSV file.