I am a researcher organizing a large dataset of experimental sensor readings. I have a Python script at `/home/user/process_results.py` that processes results from a SQLite database located at `/home/user/sensor_data.db`. 

Currently, I am facing two major issues:
1. The script is extremely slow because the database lacks proper indexing.
2. I've been warned that the SQL queries inside the Python script are constructed unsafely and inefficiently using string formatting (f-strings and `.format()`) instead of parameterized queries.

Please perform the following steps to fix my result processing pipeline:

1. **Parameterize Queries:** Modify `/home/user/process_results.py`. Change all `cursor.execute()` calls to use proper SQLite parameterized queries (e.g., using `?` placeholders) instead of string formatting. Do not change the function signatures or the returned data formats.
2. **Design Index Strategy:** Analyze the `WHERE` and `ORDER BY` clauses of the queries in the script. Connect to `/home/user/sensor_data.db` and execute `CREATE INDEX` statements to create the optimal indexes that will speed up these specific queries. Name your indexes `idx_sensor_time` (for the sensor history query) and `idx_batch` (for the batch stats query).
3. **Verify Execution Plans:** To prove the new indexes are being used, manually run `EXPLAIN QUERY PLAN` for both parameterized queries (you can substitute dummy values like `'S-100'`, `'2023-01-01'`, `'2023-01-31'`, and `'B-52'` for the execution plan check). Save the exact console output of these `EXPLAIN QUERY PLAN` commands to `/home/user/query_plans.txt`. Format the file with the output of the first query's plan, a blank line, and then the output of the second query's plan.

The final state should have the Python script modified, the database containing the new indexes, and the `query_plans.txt` file confirming index usage.