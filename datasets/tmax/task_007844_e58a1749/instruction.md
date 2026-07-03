You are a data engineer troubleshooting an ETL pipeline metadata analyzer. 

We store our ETL pipeline's dependency graph and execution statistics in a SQLite database located at `/home/user/pipeline.db`. 
A junior engineer wrote a Python script at `/home/user/analyze.py` to trace the dependency path starting from the `ingest` job down to the `report` job, and to calculate a rolling cumulative sum of execution times along that path.

However, the script is currently broken. It returns wildly incorrect, duplicated results because the SQL query inside contains an implicit cross join and lacks a proper recursive graph traversal. It also fails to correctly compute the cumulative execution time using analytical window functions.

Your task is to fix `/home/user/analyze.py` so that it correctly:
1. Uses a `WITH RECURSIVE` CTE to traverse the dependency graph (table `dependencies`) starting from `parent_id = 'ingest'` to find the direct lineage down to the `report` job.
2. Joins the traversal results with the `jobs` table to get the `exec_time_sec` for each job.
3. Uses a window function to compute the `cumulative_time` (the running total of `exec_time_sec` ordered by the step depth of the traversal, starting with step 0 for 'ingest').
4. Writes the results to `/home/user/pipeline_report.csv` with exactly the following columns: `job_id,step,exec_time_sec,cumulative_time`.

The database schema is as follows:
- `jobs` (job_id TEXT PRIMARY KEY, exec_time_sec INTEGER)
- `dependencies` (parent_id TEXT, child_id TEXT)

Run your fixed script to generate the output file. Ensure the CSV includes headers and exactly matches the required column names and values.