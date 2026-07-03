You are acting as a Database Administrator. We have an SQLite database located at `/home/user/company.db` containing a large table called `employees`. 

Currently, our application is experiencing severe performance issues when trying to render the organizational chart for specific departments. The system uses a recursive query to find all direct and indirect reports for a given manager, but it is extremely slow. 

Your task is to analyze the schema, write the correct recursive query, analyze its execution plan, optimize the database, and export the results.

Perform the following steps exactly as specified:

1. **Write the Recursive Query:** Formulate an SQLite recursive Common Table Expression (CTE) to find the employee with `id = 42` and all of their direct and indirect reports. The query should return all columns from the `employees` table.
2. **Analyze the Unoptimized Plan:** Using Python (`sqlite3` module), execute an `EXPLAIN QUERY PLAN` for your recursive query *before* making any database schema changes. Save the raw text output (the `detail` column of the explain plan) to a file named `/home/user/plan_before.txt`, with each step on a new line.
3. **Optimize:** Analyze the query plan and identify the missing index that would prevent full table scans during the recursive steps. Create this index in the database. Name the index `idx_manager`.
4. **Analyze the Optimized Plan:** Run `EXPLAIN QUERY PLAN` again for the exact same recursive CTE. Save the raw text output to a file named `/home/user/plan_after.txt`.
5. **Export Data:** Execute the recursive query (now optimized) and export the results to a CSV file located at `/home/user/reports.csv`. The CSV should include a header row with the exact column names from the `employees` table, and the rows should be sorted by `id` in ascending order. 

Ensure all output files are placed exactly at the paths specified. Write a Python script to perform these steps, or do them interactively via the SQLite CLI and shell commands, but Python is recommended for formatting the outputs.