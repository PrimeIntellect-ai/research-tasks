You are a data analyst tasked with processing several CSV files that represent a company's organizational knowledge graph. You need to identify "cross-departmental" project assignments and calculate the hierarchical management depth of the involved employees. 

You have been provided with four CSV files in `/home/user/`:
1. `employees.csv`: `id,name,manager_id,dept_id` (If `manager_id` is empty, the employee is the CEO).
2. `departments.csv`: `id,name`
3. `projects.csv`: `id,name,dept_id` (The department that owns the project).
4. `assignments.csv`: `emp_id,project_id`

Your task is to write a Bash script named `/home/user/run_analysis.sh` that does the following:
1. Imports these CSV files into a new SQLite database at `/home/user/company.db`.
2. Creates appropriate indexes on the tables to optimize join and lookup operations.
3. Uses a recursive SQL query (CTE) to calculate the "management depth" of every employee (CEO has depth 0, direct reports to CEO have depth 1, their reports have depth 2, etc.).
4. Finds all "cross-departmental anomalies" — instances where an employee is assigned to a project that is owned by a *different* department than the employee's own department.
5. Exports the results to a JSON file at `/home/user/cross_dept_analysis.json`.

The final JSON file must be a strictly formatted JSON array of objects, containing exactly these keys:
- `employee`: The employee's name (string)
- `employee_dept`: The name of the employee's department (string)
- `project`: The project's name (string)
- `project_dept`: The name of the department that owns the project (string)
- `management_depth`: The calculated management depth of the employee (integer)

Sort the JSON array alphabetically by the `employee` name, then by `project` name. 
Ensure your script `/home/user/run_analysis.sh` is executable and runs without user intervention.