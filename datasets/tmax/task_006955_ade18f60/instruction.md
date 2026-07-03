You are a data analyst tasked with analyzing a company's organizational structure and compensation data. 

You have been provided with a CSV file at `/home/user/employees.csv` containing the following columns:
`emp_id,name,manager_id,salary,department`

Your goal is to write a Bash script at `/home/user/analyze.sh` that processes this data to generate a new CSV file. Because the dataset represents a hierarchy (a tree graph) and requires complex analytical aggregations, you must use `sqlite3` within your Bash script to perform the calculations.

Your Bash script should:
1. Create an in-memory SQLite database (or temporary file) and import the `employees.csv` data.
2. Use a recursive query (Recursive CTE) to compute the `management_level` of each employee. The CEO (who has an empty/null `manager_id`) is at level 0. Direct reports to the CEO are at level 1, their direct reports are level 2, and so on. (This satisfies a graph traversal/shortest path computation).
3. Use Window Functions to calculate:
   - `dept_avg_salary`: The average salary of all employees in the same department, rounded to the nearest whole integer.
   - `salary_rank_in_dept`: The rank of the employee's salary within their department (highest salary gets rank 1).
4. Export the results to a comma-separated file at `/home/user/results.csv`.

The output CSV MUST contain a header row and have the exact following columns:
`emp_id,name,department,salary,management_level,dept_avg_salary,salary_rank_in_dept`

The rows in `/home/user/results.csv` must be ordered by:
1. `department` (ascending, alphabetically)
2. `salary_rank_in_dept` (ascending)

Make sure your script is executable. You can run `sqlite3` directly from your bash script using a Here-Document (<<EOF) or by passing a string.