You are a data analyst at a large corporation. You have been given a set of CSV files representing the company's organizational structure, project assignments, and employee timesheets. Your task is to calculate the total labor cost for each **Root Department** (a department with no parent) by rolling up the costs of all sub-departments, and output the result to a specific file.

You will find four CSV files in the `/home/user/data/` directory (you will need to assume these exist or explore them when you start):
1. `departments.csv` (columns: `dept_id`, `parent_dept_id`, `dept_name`)
2. `projects.csv` (columns: `project_id`, `dept_id`, `project_name`)
3. `employees.csv` (columns: `emp_id`, `hourly_rate`, `name`)
4. `timesheets.csv` (columns: `emp_id`, `project_id`, `hours`)

The labor cost for a timesheet entry is calculated as: `hours * hourly_rate`.
Each project belongs to a specific department. Departments are hierarchical; a department might have a `parent_dept_id` pointing to another department. If `parent_dept_id` is empty/null, it is a Root Department. 
The cost of a project should be attributed to its immediate department, and then rolled up the hierarchy to the ultimate Root Department.

Write a Python script (e.g., using `sqlite3` to load the CSVs into an in-memory database and using Recursive CTEs, or using `pandas`) to:
1. Parse the CSV files.
2. Resolve the hierarchical department structure to find the ultimate Root Department for every sub-department.
3. Calculate the total labor cost for each project based on the timesheets and employee rates.
4. Aggregate the total labor cost at the Root Department level.
5. Export the final aggregated data to a CSV file located at `/home/user/department_costs.csv`.

The output CSV must have exactly two columns: `root_dept_name` and `total_cost`.
The rows must be sorted by `total_cost` in descending order. Do not include quotes around the text. Use a comma as the delimiter. Include the header row.