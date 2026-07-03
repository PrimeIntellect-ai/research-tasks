You are a Database Administrator troubleshooting a graph processing issue on a Linux server.

Developers have reported that queries on the workflow hierarchy in `/home/user/workflow.db` are returning stale or missing rows. You suspect an index corruption issue on the SQLite database.

Your task is to write a single Bash script at `/home/user/analyze.sh` that performs the following steps:
1. Rebuilds all indices in the `/home/user/workflow.db` database to fix the corruption.
2. Uses a single SQLite invocation within the script to execute a recursive hierarchical query.
3. The query must start at the root node (`id = 1`) and find all descendants in the `nodes` table (which has columns `id`, `parent_id`, and `cost`).
4. The query must calculate two analytical columns:
   - `depth`: The distance from the root (the root node `id = 1` has a depth of 0).
   - `cost_rank`: A ranking of nodes *within the same depth level* based on their `cost` in descending order (highest cost gets rank 1). You must use a window function for this.
5. Order the final query results by `depth` ascending, then by `cost_rank` ascending.
6. The script must output the final result in JSON format to `/home/user/report.json`. The output should be a valid JSON array of objects, with each object containing the keys: `id`, `parent_id`, `cost`, `depth`, and `cost_rank`.

Ensure your script is executable and completely self-contained. The database already exists.