You are a data analyst given two CSV files representing an organization's structure. You need to reverse engineer the reporting hierarchy, query the data, apply pagination and filtering, and export the results.

The files are located at:
- `/home/user/employees.csv` (Columns: `id`, `name`, `department`, `salary`, `manager_id`)
- `/home/user/departments.csv` (Columns: `dept_id`, `dept_name`, `parent_dept_id`)

Write a Python script at `/home/user/analyze.py` that does the following:
1. Creates an in-memory SQLite database and loads the data from the two CSV files.
2. Constructs a recursive CTE (Common Table Expression) to find all direct and indirect reports of the employee with `id = 1` (Alice, the CEO). 
   - Direct reports to `id = 1` should have a `depth` of 1.
   - Their direct reports should have a `depth` of 2, and so on.
3. Joins the results with the `departments` table so that the output includes the department's string name (`dept_name`) rather than the department ID.
4. Filters the hierarchical result set to only include employees with a `salary > 50000`.
5. Sorts the results first by `depth` (ascending), then by `salary` (descending), and finally by `name` (ascending).
6. Applies pagination to the sorted results to retrieve **Page 2**, assuming a **Page Size of 5** (i.e., you should retrieve the 6th through 10th records of the sorted result set).
7. Exports the paginated result to a JSON file at `/home/user/page2.json`. The file should contain a JSON array of objects with exactly these keys: `id`, `name`, `dept_name`, `salary`, `depth`.
8. Runs SQLite's `EXPLAIN QUERY PLAN` on your final SELECT query and saves the string output (the `detail` column or equivalent textual representation of the plan) into `/home/user/query_plan.txt`.

Run your script to produce the required output files. Ensure the JSON strictly matches the key names and expected types (e.g. integers for id, salary, and depth).