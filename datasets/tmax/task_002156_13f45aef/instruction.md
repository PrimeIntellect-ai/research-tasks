You are a Database Reliability Engineer. We have a backup dependency tracking system running on a stack of PostgreSQL and Redis. 

Currently, our `/app/backup_extractor.py` script is used to calculate the cascading restore chain when a specific backup job fails. It finds all downstream dependent jobs by traversing the dependency graph. However, the current implementation uses a naive Python loop (N+1 query pattern) to traverse the graph and fetch job details, which is horribly slow and takes over 15 seconds for deep dependency chains.

The services are pre-configured. You can start them using:
`bash /app/start_services.sh`
This will start PostgreSQL (port 5432) and Redis (port 6379), and populate the database with 20,000 backup jobs and their dependencies.

Database Schema (PostgreSQL):
- `backup_jobs` (id INT PRIMARY KEY, job_name VARCHAR, status VARCHAR, created_at TIMESTAMP)
- `job_dependencies` (parent_job_id INT, child_job_id INT)

Your task:
1. Rewrite `/app/backup_extractor.py` to be highly efficient. You must replace the Python-level N+1 graph traversal with a single optimized SQL query using a **Recursive CTE** to traverse the graph.
2. The query must also use a **Window Function** to filter out duplicate `job_name`s in the hierarchy, keeping only the record with the most recent `created_at` timestamp for each `job_name` in the restore chain.
3. The script must take a starting `job_id` as a command-line argument (e.g., `python /app/backup_extractor.py 500`).
4. The script must store the resulting list of dependent `job_id`s (ordered by `created_at` ASC) as a JSON array in Redis at the key `restore_chain:<starting_job_id>`.
5. The execution time of your script must be **less than 0.5 seconds**.

Do not change the database schema. Optimize the query and the Python code so that it executes quickly.