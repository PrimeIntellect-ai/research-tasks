You are a database administrator tasked with consolidating organizational data from multiple sources to generate a cross-representation dependency report.

You have been provided with two data sources in `/home/user/data/`:
1. An SQLite database `/home/user/data/org.db` containing an `employees` table.
   Schema: `CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, manager_id INTEGER);`
   The `manager_id` references the `id` of the employee's direct manager.

2. A JSON document `/home/user/data/tasks.json` containing a highly nested list of projects and tasks. 
   Each task object has the following keys:
   - `id`: A string representing the task ID.
   - `assignee`: An integer representing the employee ID assigned to this task.
   - `subtasks`: A list of task objects (nested infinitely) representing sub-dependencies.

Your objective is to write a Python script `/home/user/generate_report.py` that accomplishes the following:
1. Uses a **Recursive CTE** (Common Table Expression) to query `org.db` and retrieve the complete hierarchical management chain (direct and indirect reports, at all depths) starting from the CEO (employee `id = 1`). Ensure the CEO is also included in this list.
2. Recursively parses `tasks.json` to find all tasks and subtasks at any depth.
3. Calculates the total number of tasks *directly assigned* to each employee found in the CEO's hierarchy. If an employee in the hierarchy has no tasks, their count should be 0. Do not include employees who are not in the CEO's hierarchy.
4. Writes the results to a CSV file located exactly at `/home/user/task_report.csv`.

The output CSV must have the exact header:
`employee_id,employee_name,total_tasks`

The rows in the CSV must be ordered by `total_tasks` in DESCENDING order. If there is a tie in `total_tasks`, order by `employee_id` in ASCENDING order.

Do not use external libraries other than the Python standard library (e.g., `sqlite3`, `json`, `csv`). You may run the script to generate the output file.