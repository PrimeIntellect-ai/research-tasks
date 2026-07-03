You are a data analyst stepping into a project left behind by a previous colleague. You have been given a script that is supposed to generate department metrics from two CSV files, but the output is completely wrong. 

In `/home/user/`, you will find three files:
1. `employees.csv` - Contains employee data (emp_id, name, dept_id, manager_id).
2. `departments.csv` - Contains department data (dept_id, dept_name).
3. `generate_summary.sh` - A bash script that uses `sqlite3` to calculate department sizes.

Currently, `generate_summary.sh` contains a SQL query with an implicit cross join that is resulting in massively inflated employee counts for every department.

Your task is to fix and extend this script to perform the following:
1. **Fix the Bug**: Correct the query in `generate_summary.sh` so it accurately counts the number of employees in each department.
2. **Graph Materialization & Projection**: We need to understand the reporting hierarchy. Extend the SQLite script to include a Recursive Common Table Expression (CTE) that calculates the "management depth" of every employee. An employee with a `NULL` manager_id is at depth 0. Someone reporting directly to them is at depth 1, and so on.
3. **Cross-Query Aggregation**: Chain these computations together to calculate both the accurate employee count AND the average management depth of employees for each department.
4. **Output Generation**: The final output of the script must write to `/home/user/dept_metrics.json`. The JSON should be an array of objects, each containing:
   - `department`: The name of the department (string)
   - `employee_count`: The correct number of employees (integer)
   - `avg_depth`: The average management depth of employees in that department (float, rounded to 1 decimal place if necessary, but standard SQLite float output is fine).

The JSON output should be ordered alphabetically by department name. Ensure you only use standard tools (like `sqlite3` and `jq` or `awk`) to construct the parameterized query pipeline within your bash script. Run your script to generate the final `dept_metrics.json` file.