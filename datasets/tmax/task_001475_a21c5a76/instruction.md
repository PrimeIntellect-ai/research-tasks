You are a data engineer troubleshooting and optimizing an ETL pipeline dependency graph. 

The dependency graph is stored in a SQLite database at `/home/user/etl_graph.db`.
It has two tables:
- `tasks` (`id` INTEGER PRIMARY KEY, `name` TEXT)
- `dependencies` (`source_id` INTEGER, `target_id` INTEGER)

Your task is to:
1. **Optimize the database**: The queries traversing the graph from a source to its targets are slow on large datasets because there are no indexes on the `dependencies` table. Create an index named `idx_dep_source` on the appropriate column(s) in `dependencies` to optimize querying targets for a given source.
2. **Write a traversal script**: Create a bash script at `/home/user/find_downstream.sh` that takes exactly one argument (a task name). 
   - The script must use `sqlite3` to execute a single SQL query (using a Recursive CTE) to find all downstream tasks (direct and indirect) that depend on the given task.
   - The script must construct the query safely to handle the input parameter.
   - The output of the script must be a simple list of downstream task names, one per line, sorted alphabetically. Do not include the original task name in the output.
3. **Extract Query Plan**: Run the `EXPLAIN QUERY PLAN` command for your recursive CTE query (hardcoding the starting task name as 'extract_users') and save the raw output to `/home/user/query_plan.txt`. This is to verify that your index is being used.

Ensure your script is executable (`chmod +x /home/user/find_downstream.sh`). Do not install any additional packages; use standard bash, coreutils, and `sqlite3`.