You are a data engineer working on an ETL pipeline execution engine. We use a SQLite database to track a directed acyclic graph (DAG) of ETL tasks. To prevent deadlocks during concurrent pipeline runs, we need to extract a materialized execution plan based on the task dependency hierarchy.

A SQLite database is located at `/home/user/etl_tasks.db`. It contains a table named `tasks` with the following schema:
`id (TEXT), parent_id (TEXT), status (TEXT), exec_time (INTEGER)`

Your task is to write a Python script at `/home/user/materialize_graph.py` that queries this database and generates a specific paginated view of the execution plan.

The script must perform the following:
1. Connect to `/home/user/etl_tasks.db`.
2. Use a Recursive CTE to traverse the task hierarchy, starting from the task where `id = 'ROOT'`. The `ROOT` task has a hierarchy depth of 0. Children of `ROOT` have depth 1, and so on.
3. Completely filter out any task (and thus entirely prune its downstream descendants) if the task's `status` is `'FAILED'`. (Assume the `ROOT` task is always `'SUCCESS'`).
4. Sort the resulting materialized graph of tasks by:
   - `depth` in Ascending order (level 0 first)
   - `exec_time` in Descending order (longest tasks at the same depth first)
   - `id` in Ascending order (alphabetical tie-breaker)
5. Paginate the results: Extract exactly "Page 2" of the results, assuming a page size of exactly 5 records (i.e., skip the first 5 records and return the next 5).
6. Write the resulting 5 records to `/home/user/paginated_tasks.csv`. The CSV should have no header row, and the columns must be exactly: `id,depth,parent_id`.

Example row format in CSV:
`TASK_X,3,TASK_W`

Do not use third-party libraries like `pandas` or `sqlalchemy`; rely strictly on the standard library `sqlite3` and `csv` modules. Write the file and exit successfully.