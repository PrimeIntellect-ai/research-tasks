You are a data engineer tasked with building an ETL pipeline module to analyze organizational asset distribution. 

I have a SQLite database located at `/home/user/company_data.db` which contains three tables: `employees`, `departments`, and `assets`. You need to inspect the schema of this database to understand the relationships between these tables.

Your objective is to write a Python script at `/home/user/etl_hierarchy.py` that extracts the organizational hierarchy under a specific manager and aggregates the total cost of assets held by each person in that hierarchy.

The script must meet the following requirements:
1. It must accept a command-line argument `--manager-name` (e.g., `python /home/user/etl_hierarchy.py --manager-name "Alice Smith"`). Use parameterized queries to prevent SQL injection when using this argument.
2. It must use a **Recursive CTE** (Common Table Expression) to traverse the employee hierarchy starting from the specified manager down to all direct and indirect reports. The manager themselves is at `level 0`, their direct reports are at `level 1`, their reports' reports are at `level 2`, and so on.
3. For each employee in that specific hierarchy, calculate the total cost of assets assigned to them. If an employee has no assets, their total cost should be `0`.
4. The script must output the final pipeline results to a JSON file located at `/home/user/hierarchy_cost.json`.
5. The JSON file must contain a single array of objects, where each object has exactly these keys:
   - `employee_name` (string): The name of the employee.
   - `level` (integer): The depth in the hierarchy relative to the root manager (root is 0).
   - `total_asset_cost` (float or integer): The sum of the cost of all assets assigned to this employee.
6. The JSON array must be sorted by `level` in ascending order, and then by `employee_name` in alphabetical ascending order for ties.

You may install any Python packages you need (like `sqlite3`, though it is built-in). 
Do not modify the database. Only read from it. Once your script is written, execute it for the manager `"Alice Smith"` to generate the output file.