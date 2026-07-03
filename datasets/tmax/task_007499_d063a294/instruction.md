You are a database administrator tasked with optimizing a reporting pipeline. A previous script made dozens of separate queries to compute hierarchical metrics. Your task is to replace it with a single efficient SQLite query in a Python script, and validate the output against a strict schema.

I have provided an SQLite database at `/home/user/company.db`. It contains a single table:
`employees` (id INTEGER PRIMARY KEY, name TEXT, manager_id INTEGER, department TEXT, salary INTEGER)

Write a Python script at `/home/user/export_metrics.py` that connects to `/home/user/company.db` and performs the following:

1. Executes a single SQL query that:
   - Uses a Recursive CTE to determine the `hierarchy_level` for each employee. The top-level manager (where `manager_id` IS NULL) is level 0. Direct reports are level 1, and so on.
   - Uses Window Functions to calculate two additional columns:
     a) `dept_total_salary`: The total salary of all employees in the same department.
     b) `dept_salary_rank`: The rank of the employee's salary within their department (highest salary = 1, using the `RANK()` function).

2. Fetches the results (id, name, department, salary, hierarchy_level, dept_total_salary, dept_salary_rank).

3. Validates the extracted records against a JSON schema located at `/home/user/schema.json`. You may use the `jsonschema` library (you can install it via `pip install jsonschema --break-system-packages` if needed).

4. If all records pass validation, write the results as a JSON array of objects to `/home/user/metrics_output.json`. Each object should have the keys: `id`, `name`, `department`, `salary`, `hierarchy_level`, `dept_total_salary`, `dept_salary_rank`.

Ensure your Python script completely generates the `metrics_output.json` file when run.