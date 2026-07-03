You are a data engineer tasked with building a specific ETL transformation step. 

You have been provided with an SQLite database at `/home/user/company.db` containing three tables:
1. `employees` - columns: `emp_id` (INTEGER), `name` (TEXT), `manager_id` (INTEGER, foreign key to emp_id)
2. `projects` - columns: `project_id` (INTEGER), `project_name` (TEXT)
3. `timesheets` - columns: `emp_id` (INTEGER), `project_id` (INTEGER), `hours` (INTEGER)

Your task is to write a Python script at `/home/user/etl.py` that queries this database to calculate the total time spent on every project by each manager's *entire organizational downline* (which includes the manager themselves, their direct reports, their reports' reports, and so on recursively).

The script must:
1. Identify all employees who are managers (an employee is a manager if their `emp_id` appears as a `manager_id` for at least one other employee).
2. For each manager, use a recursive query or logic to find all employees in their downline.
3. Aggregate the total hours spent on each project by all members of that manager's downline.
4. Output the results to a CSV file at `/home/user/manager_project_hours.csv`.

The output CSV must exactly match this format (including headers):
```csv
manager_name,project_name,total_hours
```
Sort the CSV rows alphabetically by `manager_name` (ascending), and then by `project_name` (ascending).
Do not include rows where `total_hours` is 0 or NULL. Do not include employees who are not managers.