You are an analyst at a mid-sized company. The HR department has provided you with two CSV files containing the organizational structure and department budget modifiers:

1. `/home/user/employees.csv`
   Columns: `id`, `name`, `manager_id`, `salary`, `dept_id`
   (Note: The CEO has an empty `manager_id`)

2. `/home/user/departments.csv`
   Columns: `dept_id`, `dept_name`, `budget_modifier`

Your task is to write a Python script at `/home/user/org_rollup.py` that calculates the total "adjusted budget" for any manager's entire organizational subtree (themselves, their direct reports, their reports' reports, etc.).

Requirements for `/home/user/org_rollup.py`:
- It must accept a single command-line argument: the `manager_id` (integer).
- It must use the built-in `sqlite3` and `csv` modules to load the two CSV files into an in-memory SQLite database (`:memory:`).
- It must use a single parameterized SQL query (using `?` for the parameter) that incorporates a `WITH RECURSIVE` Common Table Expression (CTE) to find the target employee and all their downstream reports.
- Within the same query, it should join the recursive results with the departments table to calculate the total adjusted budget, which is defined as `SUM(salary * budget_modifier)` for the entire subtree.
- It must print *only* the final aggregated sum to standard output, formatted as a float with exactly two decimal places (e.g., `123456.78`).

Do not use external libraries like `pandas`; rely purely on Python's standard library and SQLite's SQL engine to do the heavy lifting.