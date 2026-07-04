You are an ETL Data Engineer. We have an SQLite database containing our ETL job dependency graph, located at `/home/user/etl_graph.db`. The table `dependencies` has two columns: `source` (the job that must finish first) and `target` (the job that waits for the source).

Recently, our concurrent job orchestrator started deadlocking. We suspect there are cyclic dependencies in our ETL graph.

Your task is to write a Bash script named `/home/user/analyze_graph.sh` that uses the `sqlite3` command-line tool to query this database and extract two pieces of information:

1. **Root Jobs:** Find all jobs that have NO incoming dependencies (they never appear in the `target` column). Save these job names to `/home/user/roots.txt`, one per line, sorted alphabetically.
2. **Cyclic Jobs (Deadlocks):** Find all jobs that are part of a circular dependency chain (e.g., Job1 -> Job2 -> Job3 -> Job1). Save the names of all jobs involved in any cycle to `/home/user/cycles.txt`, one per line, sorted alphabetically. *Hint: You will likely need to use a Recursive CTE in your SQL query to traverse the graph and detect cycles.*

Ensure your Bash script is executable and performs both queries and writes the output files correctly. You may use intermediate temporary files if needed, but the final results must strictly be in the two text files specified above.