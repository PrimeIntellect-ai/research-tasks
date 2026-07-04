You are acting as a technical assistant to a compliance officer auditing an organization's internal systems. 

The officer needs to identify anomalous access to highly sensitive records, but the initial query they tried was poorly constructed, causing the database to hang and block other transactions. 

Your task is to analyze the SQLite database schema at `/home/user/audit.db` and write a highly optimized Python script that retrieves the required compliance data using a single, efficient SQL query.

Here are the specific requirements for the data extraction:
1. Find all employees who accessed records with a `sensitivity_level` of 'CRITICAL'.
2. The access must have occurred strictly outside standard business hours (i.e., before '08:00:00' or strictly after '18:00:00' based on the time component of the access timestamp).
3. The employee must have accessed 'CRITICAL' records outside standard business hours MORE THAN 2 times in total.
4. Your query must utilize complex joins and group by aggregations to do this efficiently without resorting to Python-side data filtering. Let the database engine do the work.

Write a Python script at `/home/user/audit_extract.py` that:
- Connects to `/home/user/audit.db`.
- Executes your optimized query.
- Writes the results to a CSV file at `/home/user/flagged_employees.csv`.
- The CSV must have exactly three columns in this order: `emp_id`, `emp_name`, `access_count`.
- The CSV must include a header row with those exact column names.
- The results should be ordered by `access_count` in descending order, and then by `emp_id` in ascending order.

Ensure your Python script runs cleanly and generates the file in the exact format requested.