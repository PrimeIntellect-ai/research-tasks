You are a database administrator tasked with optimizing a graph projection query. 

Currently, a developer is using a slow, iterative Bash script to traverse a hierarchy of tasks in an SQLite database, calculating cumulative durations and ranks. This iterative approach is causing long read-locks and poor performance. You need to replace it with a single, highly optimized SQL query using recursive Common Table Expressions (CTEs) and Window functions.

The database is located at `/home/user/tasks.db`. It contains a single table:
`tasks (id INTEGER PRIMARY KEY, parent_id INTEGER, name TEXT, duration INTEGER)`

Your goal is to write a Bash script at `/home/user/run_query.sh` that connects to the SQLite database and exports a materialized view of the task graph to a CSV file at `/home/user/materialized_graph.csv`.

The output CSV must strictly adhere to the following schema and rules:
1. Include a header row: `id,root_id,depth,path_duration,rank_in_root`
2. `id`: The task's ID.
3. `root_id`: The ID of the top-most parent task (where `parent_id` is NULL) for this branch.
4. `depth`: The number of edges from the root to this task (root has depth 0).
5. `path_duration`: The sum of the `duration` of all tasks in the path from the root down to (and including) this task.
6. `rank_in_root`: The rank of this task compared to all other tasks sharing the same `root_id`, based on `path_duration` in descending order. If there is a tie, order by `id` in ascending order. Use the standard RANK() window function logic (1, 2, 2, 4...).
7. The final CSV output must be ordered by `id` ascending.

Requirements:
- Your script `/home/user/run_query.sh` must be executable (`chmod +x`).
- It must produce exactly the CSV described above using a single `sqlite3` invocation.
- Do not use any temporary tables; accomplish this entirely through a recursive query and window functions.