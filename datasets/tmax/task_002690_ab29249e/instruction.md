You are a Database Reliability Engineer investigating performance issues with a backup management system. 

You have an SQLite database at `/home/user/backups.db` containing a table `backup_jobs`. This table tracks backup operations, where incremental backups point to their base backups via a `parent_id` column.

A colleague has written a recursive query to calculate the total size of each backup chain (the full backup plus all its incremental children). The query is saved at `/home/user/query.sql`. However, as the database grows, this query is becoming extremely slow because it requires full table scans during the recursive joins.

Your task is to write a Go program at `/home/user/optimize.go` that does the following:
1. Connects to `/home/user/backups.db` (you may install and use `github.com/mattn/go-sqlite3`).
2. Reads the query from `/home/user/query.sql`.
3. Executes an `EXPLAIN QUERY PLAN` on the query and saves the raw output rows (just the `detail` column from the explain plan, one per line) to `/home/user/plan_before.txt`.
4. Executes a SQL statement to create the optimal index on `backup_jobs` to speed up the recursive `parent_id` lookup.
5. Executes `EXPLAIN QUERY PLAN` again on the same query and saves the raw output rows (the `detail` column) to `/home/user/plan_after.txt`.
6. Executes the actual query and saves the aggregated results as a JSON array of objects to `/home/user/results.json`. The JSON should be formatted like: `[{"root_id": 1, "total_bytes": 10500}, ...]`.

You must execute your Go code to produce the required output files. You can verify your index strategy worked by ensuring `plan_after.txt` mentions a `SEARCH` using your new index instead of a `SCAN`.